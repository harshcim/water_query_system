import requests
# from flask import Flask, request, jsonify
import pandas as pd
import logging
import datetime
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import TextLoader
from langchain_community.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAI
from langchain.prompts import PromptTemplate
import mysql.connector
import warnings
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import re
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.vectorstores import FAISS
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from packages.prompts import examples,sys_prompt,answer_prompt



# Global variables for reuse
load_dotenv()

logging.basicConfig(filename='Automation_Query_System_Update.log', level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')



# Defining file path for query logs
# QUERY_LOG_FILE = 'queries_with_timestamps.txt'



def log_entry(question, query, result, response):
    
    """
    Log the question, query, and result with formatted timestamp.
    """
    entry = f"\n\n--- Entry Logged at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n"
    entry += f"\nQuestion Asked: {question}\n"
    entry += f"\nQuery Generated: {query}\n"
    entry += f"\nLLM Output: {result}\n"
    entry += f"\nLLM Output: {response}\n"
    entry += "--- End of Entry ---\n\n"
    logging.info(entry)
    
    
# def log_query_with_timestamp(question, query):
#     """
#     Log the SQL query with a timestamp and the corresponding question.
#     """
#     timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     log_entry = f"[{timestamp}] Question: {question}\nSQL Query: {query}\n\n"
    
#     with open(QUERY_LOG_FILE, 'a') as file:
#         file.write(log_entry)
    
    

db = SQLDatabase.from_uri("mysql+pymysql://root:Cimcon%40123@127.0.0.1:3306/test_database")

print("Database connection established.")

greetings = ["hello", "hi", "hey", "howdy", "greetings", "yo", "sup", "hiya", "hola", "bonjour", "ciao", "salut", "hallo", 
             "namaste", "konichiwa", "salaam", "aloha", "hail", "what's up", "good day", "morning", "afternoon", "evening", 
             "night", "good morning", "good afternoon", "good evening", "good night", "how's it going", "how are you", "how's everything", 
             "what's happening", "what's new", "what's going on", "how's life", "long time no see", "nice to see you", "pleased to meet you",
             "how's your day", "how's your day going", "how's your morning", "how's your afternoon", "how's your evening", "how's your night", 
             "how's your weekend", "hope you're well", "hope you're doing well", "hope you're having a good day", "hope you're having a good morning",
             "hope you're having a good afternoon", "hope you're having a good evening", "hope you're having a good night", "good to see you", 
             "good to see you again", "nice to meet you", "it's nice to meet you", "it's a pleasure to meet you", "pleased to make your acquaintance"]


# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.5, max_output_tokens=8192)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.5,
    max_output_tokens=8192,
    google_api_key=os.getenv("GOOGLE_API_KEY")  
)


embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")


def get_response(llm,embeddings,question,table_id):
   
    example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")
 
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        embeddings,
        FAISS,
        k=7,
        input_keys=["input"],
    )
 
    few_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=sys_prompt,
        suffix="User input: {input}\nSQL query: ",
        input_variables=["input", "table"],
    )
 
    query_chain = few_prompt | llm | StrOutputParser()
 
    query = query_chain.invoke({'input':question,'table':table_id})
       
    
    # with open('queries.txt', 'a') as file:
    #         file.write(question + '\n')    
    #         file.write(query+ '\n\n')
    
    # Log the question and query to 'queries.txt' with timestamps
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open('queries.txt', 'a') as file:
        file.write(f"\n\n--- Entry Logged at {timestamp} ---\n")
        file.write(f"Question: {question}\n")
        file.write(f"SQL Query: {query}\n") 
    
    
 
    execute_query = QuerySQLDataBaseTool(db=db)
    result = execute_query.invoke(query)
 
    prompt = PromptTemplate.from_template(template=answer_prompt)
 
    rephrase_answer = prompt | llm | StrOutputParser()
 
    answer = rephrase_answer.invoke({'input':question,'query':query,'result':result})
 
    # answer = chain.invoke({'input': question, 'table': table_id})
    return answer




def main():
    """
    Main function to interact with the user, take their query, and provide an answer.
    """
    while True:
        question = input("Please enter your question (or type 'exit' to quit): ")
        if question.lower() == 'exit':
            print("Exiting the query system. Goodbye!")
            break
        
        table_id = input("Please enter the table name: ")
        response = get_response(llm,embeddings,question, table_id)
        print(f"\nResponse:\n{response}\n")

if __name__ == "__main__":
    main()

