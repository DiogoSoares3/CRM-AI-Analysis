from typing import List, ClassVar
import subprocess
import os
import uuid

import fireducks.pandas as pd
from fastapi import APIRouter, Depends, Response
from sqlalchemy import MetaData, Table, Column, String, inspect, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv

from core.database import engine
from core.deps import get_session
from core.configs import settings
from shared.contracts.user_input_contract import UserInput
from utils.full_dataset_preparation import full_dataset_preparation
from schemas.sales_pipeline_schema import SalesPipelineSourceSchema
from models.sales_pipeline_model import SalesPipelineSourceModel


load_dotenv()

router = APIRouter()


@router.post('/run-dbt/', status_code=200, description='Run DBT models for data transformation and agregation')
def run_dbt():
    original_dir = os.getcwd()
    try:
        dbt_path = os.getenv("DBT_PATH")
        if not dbt_path:
            raise ValueError("DBT_PATH environment variable is not set.")

        os.chdir(dbt_path)

        result = subprocess.run(
            ["dbt", "run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        print("DBT Run Output:")
        print(result.stdout)

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except subprocess.CalledProcessError as e:
        print("Error occurred while running dbt:")
        print(e.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        os.chdir(original_dir)


@router.post('/create-run-won-stage-data/', status_code=200, description='Insert data to Postgres database given a user input.')
def create_run_won_stage_data(db = Depends(get_session)):
    try:
        model_predictions_summary, customers_rfm_features, general_enriched_dataset = full_dataset_preparation(db)
        all_dataframes = [model_predictions_summary, customers_rfm_features, general_enriched_dataset]
        dataframe_names = ['model_predictions_summary', 'customers_rfm_features', 'general_enriched_dataset'] 

        for df, name in zip(all_dataframes, dataframe_names):
            table_name = f"{name}_source"

            with engine.connect() as conn:
                try:
                    conn.execution_options(isolation_level="AUTOCOMMIT").execute(
                        text(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
                    )
                    print(f"Table {table_name} successfully removed.")
                except ProgrammingError as e:
                    print(f"Error trying to remove the table {table_name}: {e}")

            df.to_sql(
                table_name,
                con=engine,
                index=False,
                if_exists="replace"
            )

        # Creating or updating the database views of medallion architecture
        run_dbt()

    except Exception as e:
        db.rollback()
        raise e

    return Response(status_code=200)


@router.post('/insert-won-stage-data/', status_code=200, description='Insert data to Postgres database given a user input.', response_model=SalesPipelineSourceSchema)
def insert_won_stage_data(data: UserInput, session = Depends(get_session)):
    if data.unknow_customer:
        raise NotImplementedError('Unknown Customers are not yet implemented')

    new_oportunity = SalesPipelineSourceModel(
                            opportunity_id=str(uuid.uuid4()),
                            sales_agent=data.sales_agent,
                            product=data.product,
                            account=data.account,
                            deal_stage=data.deal_stage,
                            engage_date=str(data.engage_date),
                            close_date=str(data.close_date),
                            close_value=str(data.close_value)
                    )

    try:
        session.add(new_oportunity)
        session.commit()

        create_run_won_stage_data(session)

    except Exception as e:
        session.rollback()
        raise e

    return new_oportunity


@router.post('/insert-init-data/', status_code=200, description='Insert data to Postgres database given a source directory containing JSON or CSV files.')
async def insert_init_data(session = Depends(get_session)):    
    with engine.connect() as conn:
        create_schema_query = text(f"CREATE SCHEMA IF NOT EXISTS dev;")
        conn.execute(create_schema_query)
        conn.commit()
        print(f"Schema 'dev' create or retrieved.")

        data_dir = os.path.join(settings.PROJECT_PATH, 'data')
        for file_name in os.listdir(data_dir):
            if file_name.endswith('.csv'):
                file_path = os.path.join(data_dir, file_name)

                if file_name.endswith('.csv'):
                    df = pd.read_csv(file_path)

                raw_table_name = os.path.splitext(os.path.basename(file_path))[0]
                table_name = raw_table_name + '_source'

                inspector = inspect(engine)
                if not inspector.has_table(table_name, schema='dev'):
                    if raw_table_name == 'sales_pipeline':
                        id_column = 'opportunity_id'
                    else:
                        df['id'] = [str(uuid.uuid4()) for _ in range(len(df))]
                        id_column = 'id'

                    metadata = MetaData(schema='dev')
                    columns = [Column(id_column, String, primary_key=True)] + [
                        Column(col, String) for col in df.columns if col != id_column
                    ]

                    table = Table(table_name, metadata, *columns, extend_existing=False)
                    metadata.create_all(engine)

                    rows_to_insert = df.to_dict(orient='records')
                    
                    try:
                        session.execute(table.insert().values(rows_to_insert))
                        session.commit()

                    except Exception as e:
                        session.rollback()
                        raise e
        
        # Just to create the processed data when the API starts up
        create_run_won_stage_data(session)

    return Response(status_code=200)
