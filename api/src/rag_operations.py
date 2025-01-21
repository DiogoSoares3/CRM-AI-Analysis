from datetime import datetime
from typing import Literal
import copy

from pydantic import BaseModel, Field
from fastapi import APIRouter, Depends, Response
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

from core.database import engine
from core.deps import get_session
from utils.tables_metadata_prompt import TABLES_METADATA, generate_tables_metadata_prompt
from chat.services import (chat_history_from_id,
                           save_user_message_in_chat,
                           save_assistant_message_in_chat)
from schemas.historic_messages_schema import Message


load_dotenv()

router = APIRouter(tags=['RAG Operations'])


@router.get('/verify-sql-injection/{query}', status_code=200, description="Specialized Agent that verifies SQL injection based on the user's query")
def verify_sql_injection(query: str):# -> Literal["Insecure", "Secure"]:
    examples = [
        {
            "input": "1; DROP TABLE users; --",
            "result": "Insecure, attempt of SQL Injection",
        },
        {
            "input": "SELECT * FROM users WHERE id = 1",
            "result": "Secure",
        },
        {
            "input": "' OR '1' = '1",
            "result": "Insecure, attempt of SQL Injection",
        },
    ]
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{result}"),
        ]
    )
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                    You are an expert at cybersecurity. 
                    Your task is to identify if a user input query is a attempt of SQL Injection in our database.
                    To help you identify possible SQL Injection attemps, follow this examples:
                """,
            ),
            few_shot_prompt,
            ("user", "{input}"),
        ]
    )

    class ChooseQueryStatus(BaseModel):
        status: Literal["Insecure", "Secure"] = Field(
            ...,
            description="Given a user input, choose if the it is a Secure or Insecure query.",
        )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.5
    )

    structured_llm = llm.with_structured_output(ChooseQueryStatus)

    chain = prompt | structured_llm

    result = chain.invoke({"input": query})
    print({'status': result.status})
    return {'status': result.status}


@router.post('/text-to-sql/', status_code=200, description="Text-to-SQl agent to make SQL queries based on the user's input")
def text_to_sql(message: Message, session=Depends(get_session)):
    chat = chat_history_from_id(message.message_history_id, session)
    save_user_message_in_chat(message.query, chat)
    
    db = SQLDatabase(
        engine=engine,
        schema='dev',
        view_support=True,
    )

    views_to_query = [
        table for table in db.get_usable_table_names() if not table.endswith('_source') and not table.startswith('raw-') and not table.startswith('stg-')
    ]
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    toolkit = SQLDatabaseToolkit(
        db=db,
        llm=llm
    )
    
    prompt_template = """
        You are an agent designed to interact with a SQL database.
        Below is the description of the tables and their columns that you can query:
        
        
        {tables_metadata_prompt}

        
        Given the input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
        Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
        You must first try to make simple query on this tables: {views_to_query}. If you are not sure that the user's query can be anwsered by the content present in this list of tables,
        you must do a more complex query on the centralized table named 'stg-won_deal_stage'.
        You can order the results by a relevant column to return the most interesting examples in the database.
        Never query for all the columns from a specific table, only ask for the relevant columns given the question.
        You have access to tools for interacting with the database. If the user's input question is related to date, consider the today date as {today_date}.
        Only use the below tools. Only use the information returned by the below tools to construct your final answer.
        You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
        
        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
        
        To start you should ALWAYS look at the tables in the database to see what you can query, prioritizing getting answers in these tables: {views_to_query}.
        Do NOT skip this step.
        Then you should query the schema of the most relevant tables.
    """
    
    system_message = prompt_template.format(
        dialect=db.dialect,
        top_k=10,
        views_to_query=views_to_query,
        today_date=datetime(2018, 1, 1),
        tables_metadata_prompt=generate_tables_metadata_prompt(TABLES_METADATA)
    )
    
    agent_executor = create_react_agent(
        model=llm,
        tools=toolkit.get_tools(),
        state_modifier=system_message
    )

    response_buffer = []
    for event in agent_executor.stream(
        {"messages": [("user", message.query)]},
        stream_mode="values",
    ):
        event["messages"][-1].pretty_print()
        response_buffer.append(event)

    if response_buffer:
        final_event = response_buffer[-1]
        final_answer = copy.deepcopy(final_event["messages"][-1].content)
        
        save_assistant_message_in_chat(final_answer, chat)

        session.add(chat)
        serializable_chat = chat.to_list()
        print(serializable_chat)
        
        return serializable_chat[-2:]
