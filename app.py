import streamlit as st
import os
import sqlite3
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Setup the modern Gemini Client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
    # Using 'gemini-3-flash-preview' or 'gemini-2.5-flash'
    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents=[prompt, question]
    )
    return response.text.strip()

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.close()
    return rows

# The prompt instructions for the AI
prompt = """
You are an expert in converting English questions to SQL queries!
The database name is STUDENT and has columns: NAME, CLASS, SECTION, MARKS.

Example: "How many students are there?" -> SELECT COUNT(*) FROM STUDENT;
Example: "Show Data Science students" -> SELECT * FROM STUDENT WHERE CLASS='Data Science';

IMPORTANT: Do not include any formatting like ```sql or the word 'sql' in the output.
"""

# Streamlit Interface
st.set_page_config(page_title="Text-to-SQL AI")
st.header("Gemini 3.0 SQL Assistant")

user_question = st.text_input("Ask a question about your students:", key="input")
if st.button("Generate Query"):
    if user_question:
        try:
            sql_query = get_gemini_response(user_question, prompt)
            st.info(f"Generated SQL: {sql_query}")
            
            data = read_sql_query(sql_query, "student.db")
            st.subheader("Query Results:")
            for row in data:
                st.write(row)
        except Exception as e:
            st.error(f"Error: {e}")