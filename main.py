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
from flask import Flask, render_template, request, jsonify
import os
import streamlit as st
import time 


app = Flask(__name__)


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
    temperature=0.8,
    max_output_tokens=8192,
    google_api_key=os.getenv("GOOGLE_API_KEY")  
)


def clean_query(query):
    """
    Clean the SQL query by removing any Markdown or unnecessary formatting.
    """
    # Remove Markdown code block syntax if present
    clean_query = query.replace("```sql", "").replace("```", "").strip()
    return clean_query



# def preprocess_answer(answer):
#     pattern = r'\*\*(.*?)\*\*'
#     answer = re.sub(pattern, r'<b>\1</b>', answer)
#     answer = answer.replace('* ', '● ')
#     return answer

def preprocess_answer(answer):
    # Convert bold text marked with '**text**' to HTML <b> tags
    answer = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', answer)
    
    # Convert list items marked with '* ' to bullet points
    answer = re.sub(r'\*\s+', '● ', answer)
    
    # Ensure proper spacing after bullet points
    answer = re.sub(r'●\s+', '● ', answer)
    
    # Convert newlines to HTML <br> tags for proper line breaks
    answer = answer.replace('\n', '<br>')
    
    return answer




embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")


# Define a static table name
DEFAULT_TABLE_NAME = "waterdata"


def get_response(llm,embeddings,question):
   
   
   # Use the static table name
    table_id = DEFAULT_TABLE_NAME
   
   
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
    
    
    #  Clean the SQL query
    query = clean_query(query)
       

    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open('queries.txt', 'a') as file:
        file.write(f"\n\n--- Entry Logged at {timestamp} ---\n")
        file.write(f"Question: {question}\n")
        file.write(f"SQL Query: {query}\n") 
    
    
 
    execute_query = QuerySQLDataBaseTool(db=db)
    
    start_time = time.time()
    result = execute_query.invoke(query)
    execution_time = time.time() - start_time
        
    
    # If result is empty or None, return a default response
    if not result:
        return "No data found for your query."
    
 
    prompt = PromptTemplate.from_template(template=answer_prompt)
 
    rephrase_answer = prompt | llm | StrOutputParser()
 
    answer = rephrase_answer.invoke({'input':question,'query':query,'result':result})
    
    
    # Log the final response
    log_entry(question, query, result, answer)
    
    # answer = chain.invoke({'input': question, 'table': table_id})
    return answer, result, execution_time


@app.route('/history')
def history():
    with open('queries.txt', 'r') as file:
        history = file.read()
    return render_template('history.html', history=history)



def main():
    
    st.set_page_config(page_title="Water Data Query System", layout="wide")
    
     # Welcome Message and Instructions
    st.title("Water Data Query System")
    
    st.markdown("""
        This tool allows you to query water-related data from our database. Simply enter your query in natural language,
        and the system will generate the corresponding SQL query and return the results.
    """)
    
    
    # Custom CSS for styling the interface
    st.markdown(
        """
        <style>
        /* Customize input box */
        .stTextInput > div > div > input {
            padding: 10px;
            font-size: 18px;
            border-radius: 10px;
            border: 1px solid #ccc;
        }

        /* Customize submit button */
        .stButton > button {
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            border-radius: 5px;
            border: none;
        }

        /* Customize spinner */
        .stSpinner {
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Message bubbles for user and response */
        .user-bubble {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }

        .response-bubble {
            background-color: #f1f1f1;
            color: black;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html = True
    )


    # Input box for user query
    user_input = st.text_input("Enter your query:")

    
    if st.button("Submit"):
        
        st.markdown(f"<div class='user-bubble'>{user_input}</div>", unsafe_allow_html=True)

        with st.spinner("Processing..."):
            time.sleep(2)
            response, result, execution_time = get_response(llm, embeddings, user_input)
        
        # Process the response using preprocess_answer
        processed_response = preprocess_answer(response)        
        
        # Display the response
        st.markdown(f"<div class='response-bubble'>{processed_response}</div>", unsafe_allow_html=True)
        st.markdown(f"**Query Execution Time:** {execution_time:.2f} seconds")
        
        # Download Option for Results
        st.download_button("Download Results", processed_response, file_name="query_results.txt")

        # Feedback Mechanism
        st.markdown("### Was this response helpful?")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Yes"):
                st.session_state.feedback_message = "Thank you for your feedback!"
        
        with col2:
            if st.button("No"):
                st.session_state.feedback_message = "We appreciate your feedback and will work on improving the responses."

        if 'feedback_message' in st.session_state:
            st.info(st.session_state.feedback_message)


# Run the main function when the script is executed
if __name__ == "__main__":
    main()

# def main():
#     """
#     Main function to interact with the user, take their query, and provide an answer.
#     """
#     while True:
#         question = input("Please enter your question (or type 'exit' to quit): ")
#         if question.lower() == 'exit':
#             print("Exiting the query system. Goodbye!")
#             break
        
#         response = get_response(llm,embeddings,question)
#         print(f"\nResponse:\n{response}\n")

# if __name__ == "__main__":
#     main()

# @app.route('/')
# def home():
#     return render_template('chat.html')

# @app.route('/ask', methods=['POST'])
# def ask():
#     data = request.json
#     question = data['question']
#     table_id = data['table_id']
    
#     try:
#         response = get_response(llm, embeddings, question, table_id)
#         return jsonify({"response": response})
#     except Exception as e:
#         return jsonify({"error": str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)