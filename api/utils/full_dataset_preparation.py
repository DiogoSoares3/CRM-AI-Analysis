import os
import random
from datetime import date, datetime

import fireducks.pandas as pd
from sqlalchemy import select
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.utils import summary_data_from_transaction_data
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from models.accounts_model import AccountsSourceModel
from models.products_model import ProductsSourceModel
from models.sales_pipeline_model import SalesPipelineSourceModel
from models.sales_teams_model import SalesTeamsSourceModel
from utils.export_models import export_beta_geo_fitter, export_gamma_gamma_fitter



def full_dataset_preparation(session, deal_stage: str = 'Won', today_date: date = datetime(2018,1,1)):
    accounts_df = load_accounts_data(session)
    products_df = load_products_data(session)
    sales_pipeline_df = load_sales_pipeline_data(session)
    sales_teams_df = load_sales_teams_data(session)
    
    dataframes = [accounts_df, products_df, sales_pipeline_df, sales_teams_df]
    
    filtered_dataframes = []
    for i, raw_df in enumerate(dataframes):
        if 'id' in raw_df.columns:
            raw_df = filtered_dataframes.append(raw_df.drop(columns=['id']))
        else:
            filtered_dataframes.append(raw_df)

    accounts_df, products_df, sales_pipeline_df, sales_teams_df = filtered_dataframes
    
    sales_pipeline_df.loc[sales_pipeline_df['product'] == 'GTXPro', 'product'] = 'GTX Pro'
    
    df = (pd.merge(
            pd.merge(
                pd.merge(
                    sales_pipeline_df, accounts_df, on='account', how='inner'
                    ),
                products_df, on='product', how='inner'
                ),
            sales_teams_df, on='sales_agent', how='inner'
            )
        )

    df = make_preprocessing(df)
    
    if deal_stage == 'Won':
        df = make_won_pre_feature_engineering(df)
    else:
        raise NotImplementedError('Only "Won" deal stage analysis are implemented by now.')
    
    df = make_filter_by_deal_stage(df, deal_stage)
    rfm = make_rfm_enrichment(df, today_date)
    rfm = expand_rfm_features(rfm)

    summary, bgf = fit_predict_bg_nbd_model(df, today_date)
    summary, ggf = fit_predict_gamma_gamma_model(summary)
    summary = make_cltv_predictions(summary, bgf, ggf)
    
    summary_to_merge, rfm_to_merge = drop_duplicate_columns_for_merge(summary, rfm)

    return summary_to_merge, rfm_to_merge, df


def drop_duplicate_columns_for_merge(summary: pd.DataFrame, rfm: pd.DataFrame):    
    summary = summary.drop(columns=['frequency', 'recency', 'monetary_value'])
    summary.reset_index(inplace=True)

    rfm = rfm.drop(columns=['product', 'revenue', 'Months_Since_Start', 'office_location'])

    return summary, rfm


def make_cltv_predictions(summary: pd.DataFrame, bgf: BetaGeoFitter, ggf: GammaGammaFitter):
    summary['Predicted_Year_CLTV'] = ggf.customer_lifetime_value(
        bgf,
        summary['frequency'],
        summary['recency'],
        summary['T'],
        summary['monetary_value'],
        time=12,  # Monthly
        discount_rate=0.01,  # Monthly discount
    )

    summary['Predicted_Year_CLTV'].sort_values(ascending = False)
    summary['Predicted_CLTV_Segment'] = pd.qcut(summary['Predicted_Year_CLTV'], q=3, labels=['Low', 'Medium', 'High'])

    return summary


def fit_predict_gamma_gamma_model(summary: pd.DataFrame):
    ggf = GammaGammaFitter(penalizer_coef=0.05)
    ggf.fit(summary['frequency'], summary['monetary_value'])

    summary['expected_average_profit'] = ggf.conditional_expected_average_profit(
        summary['frequency'], summary['monetary_value']
    )
    
    export_gamma_gamma_fitter(ggf)
    
    return summary, ggf
    

def fit_predict_bg_nbd_model(df, today_date: date = datetime(2018,1,1)):
    summary = summary_data_from_transaction_data(
        df,
        customer_id_col='account',
        datetime_col='close_date',
        monetary_value_col='close_value',
        observation_period_end=today_date,
    )
    
    bgf = BetaGeoFitter(penalizer_coef=0.005)
    bgf.fit(summary['frequency'], summary['recency'], summary['T'])
    
    summary['prob_alive'] = bgf.conditional_probability_alive(
    summary['frequency'], summary['recency'], summary['T']
    )

    summary['expected_purchases_day'] = bgf.conditional_expected_number_of_purchases_up_to_time(
        1, summary['frequency'], summary['recency'], summary['T']
    )

    summary['expected_purchases_week'] = bgf.conditional_expected_number_of_purchases_up_to_time(
        7, summary['frequency'], summary['recency'], summary['T']
    )

    summary['expected_purchases_monthly'] = bgf.conditional_expected_number_of_purchases_up_to_time(
        30, summary['frequency'], summary['recency'], summary['T']
    )

    summary['expected_purchases_bimonthly'] = bgf.conditional_expected_number_of_purchases_up_to_time(
        61, summary['frequency'], summary['recency'], summary['T']
    )

    summary['expected_purchases_trimester'] = bgf.conditional_expected_number_of_purchases_up_to_time(
        92, summary['frequency'], summary['recency'], summary['T']
    )

    summary['expected_purchases_half_year'] = bgf.conditional_expected_number_of_purchases_up_to_time(
        182, summary['frequency'], summary['recency'], summary['T']
    )

    summary['expected_purchases_year'] = bgf.conditional_expected_number_of_purchases_up_to_time(
        365, summary['frequency'], summary['recency'], summary['T']
    )
    
    export_beta_geo_fitter(bgf)
    
    return summary, bgf


def make_rfm_enrichment(df, today_date: date):
    rfm = df.groupby('account').agg({
        'close_date': ['min', 'max', lambda x: (today_date - x.max()).days],
        'account': 'count',
        'close_value': 'sum',
        'office_location': 'first',
        'product': 'first',
        'revenue': 'first',
    })
    
    accounts = rfm.index
    rfm = rfm.reset_index(drop=True)
    rfm.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in rfm.columns]

    rfm.rename(columns={
        'close_date_min': 'first_purchase',
        'close_date_max': 'last_purchase',
        'close_date_<lambda_0>': 'Recency',
        'account_count': 'Frequency',
        'close_value_sum': 'Monetary',
        'office_location_first': 'office_location',
        'product_first': 'product',
        'revenue_first': 'revenue'
    }, inplace=True)
    
    rfm['account'] = accounts
    
    rfm['R_Score'] = pd.cut(rfm['Recency'], bins=4, labels=[4, 3, 2, 1])
    rfm['F_Score'] = pd.cut(rfm['Frequency'], bins=4, labels=[1, 2, 3, 4])
    rfm['M_Score'] = pd.cut(rfm['Monetary'], bins=4, labels=[1, 2, 3, 4])
    rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    
    return rfm


def expand_rfm_features(rfm: pd.DataFrame):
    custom_segment_map = {
        '111': 'Dormant',
        r'11[2-3]': 'Inactive Low Spenders',
        r'12[1-3]': 'Rare Low Spenders',
        r'13[1-3]': 'Occasional Low Spenders',
        '411': 'New Enthusiasts',
        r'41[2-3]': 'New Potential Customers',
        '412': 'New Interested Parties',
        r'3[1-2]1': 'Disinterested Customers',
        r'31[2-3]': 'Rarely Interested Customers',
        '322': 'Stable Customers',
        r'32[3-4]': 'Consistent Buyers',
        r'42[2-3]': 'Moderately Engaged Customers',
        r'43[1-3]': 'Growing Engagement',
        '421': 'Beginning Customers',
        '432': 'Future Big Customers',
        r'44[2-3]': 'Loyal Customers',
        '444': 'Champions',
        r'4[2-3]4': 'Balanced High Value Customers',
        r'[3-4][3-4]1': 'High Value, Rare Buyers',
        r'[2-4][2-3][2-3]': 'Balanced Customers',
        # r'.*': 'Other'
    }
    
    rfm['RFM_Custom_Segment'] = rfm['RFM_Score'].replace(custom_segment_map, regex = True)
    
    discount_rate = 0.01 # Monthy inflation (simulation)
    rfm['Months_Since_Start'] = ((rfm['last_purchase'] - rfm['first_purchase'].min()).dt.days / 30).astype(int)
    rfm['Actual_CLTV'] = rfm['Monetary'] / ((1 + discount_rate) ** rfm['Months_Since_Start'])
    
    rfm['RF_Ratio'] = rfm['Recency'] / (rfm['Frequency'] + 1)
    rfm['ATV'] = rfm['Monetary'] / rfm['Frequency']
    
    scaler = MinMaxScaler()
    rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

    rfm['engagement_score'] = rfm_scaled[:, 1] * 0.4 + rfm_scaled[:, 2] * 0.4 - rfm_scaled[:, 0] * 0.2
    
    return rfm


def make_filter_by_deal_stage(df: pd.DataFrame, deal_stage: str):
    deal_stage_df = df[df['deal_stage'] == deal_stage]
    return deal_stage_df


def make_preprocessing(df: pd.DataFrame):
    df['engage_date'] = pd.to_datetime(df['engage_date'])
    df['close_date'] = pd.to_datetime(df['close_date'])
    df['close_value'] = df['close_value'].astype(float)
    df['revenue'] = df['revenue'].astype(float)
    df['employees'] = df['employees'].astype(int)
    df['sales_price'] = df['sales_price'].astype(float)
    
    return df


def make_won_pre_feature_engineering(df: pd.DataFrame):
    won_lost_deal_stage_df = df[(df['deal_stage'] == 'Won') | (df['deal_stage'] == 'Lost')]

    total_opportunities = won_lost_deal_stage_df.groupby('sales_agent')['opportunity_id'].count()
    won_opportunities = won_lost_deal_stage_df[won_lost_deal_stage_df['deal_stage'] == 'Won'].groupby('sales_agent')['opportunity_id'].count()

    close_rate = (won_opportunities / total_opportunities).fillna(0) * 100

    df['sales_cycle_duration'] = (df['close_date'] - df['engage_date']).dt.days
    df['agent_close_rate'] = df['sales_agent'].map(close_rate)
    df['opportunities_per_account'] = df.groupby('account')['opportunity_id'].transform('count')
    df['opportunities_per_sales_agent'] = df.groupby('sales_agent')['opportunity_id'].transform('count')

    return df


def load_sales_pipeline_data(session):
    query = select(SalesPipelineSourceModel)
    results = session.execute(query).all()

    data = [
        {column: getattr(row, column) for column in row.__table__.columns.keys()}
        for (row,) in results
    ]

    df = pd.DataFrame(data)
    return df


def load_sales_teams_data(session):
    query = select(SalesTeamsSourceModel)
    results = session.execute(query).all()

    data = [
        {column: getattr(row, column) for column in row.__table__.columns.keys()}
        for (row,) in results
    ]

    df = pd.DataFrame(data)
    return df


def load_products_data(session):
    query = select(ProductsSourceModel)
    results = session.execute(query).all()

    data = [
        {column: getattr(row, column) for column in row.__table__.columns.keys()}
        for (row,) in results
    ]

    df = pd.DataFrame(data)
    return df


def load_accounts_data(session):
    query = select(AccountsSourceModel)
    results = session.execute(query).all()

    data = [
        {column: getattr(row, column) for column in row.__table__.columns.keys()}
        for (row,) in results
    ]

    df = pd.DataFrame(data)
    return df

