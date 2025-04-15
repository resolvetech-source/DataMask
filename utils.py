import pandas as pd
import os
import PyPDF2
import sqlite3
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import json
import re
load_dotenv()

DB_PATH = os.getenv("DB_PATH")
CONNECTION = sqlite3.connect(DB_PATH)
def extract_text_from_file(uploaded_file):
  if uploaded_file.name.endswith('.txt'):
    return uploaded_file.read().decode("utf-8")
  elif uploaded_file.name.endswith('.csv'):
    df = pd.read_csv(uploaded_file)
    return df.to_string(index=False)
  elif uploaded_file.name.endswith('.pdf'):
    return extract_text_from_pdf(uploaded_file)
  return ""

def extract_text_from_pdf(uploaded_file):
  pdf_reader = PyPDF2.PdfReader(uploaded_file)
  text = ''
  for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    extracted_text = page.extract_text()
    if extracted_text:
        text += extracted_text
  return text

def fetch_tables():
  connection = sqlite3.connect(DB_PATH)
  cursor = connection.cursor()
  cursor.execute("Select name from sqlite_master WHERE type= 'table';")
  tables = [row[0] for row in cursor.fetchall()]
  table_columns = {}
  for table in tables:
    cursor.execute(f"PRAGMA table_info({table});")
    columns = [row[1] for row in cursor.fetchall()]
    table_columns[table] = columns
  connection.close()
  return  tables, table_columns

def fetch_employee_details(sql_query):
  connection = sqlite3.connect(DB_PATH)
  cursor = connection.cursor()
  cursor.execute(sql_query)
  records = cursor.fetchall()
  column_names = [description[0] for description in cursor.description]
  connection.close()
  return column_names,records

# def api_calling(api_key):
#   genai.configure(api_key  =api_key)

#   model = genai.GenerativeModel("gemini-1.5-pro-002")
#   return model

def call_qwen(prompt):
  url = "http://localhost:8000/completion"
  headers = {"Content-Type": "application/json"}
  data = {
    "prompt": prompt,
    "temperature": 0.3,
    "max_token": 2048
  }
  try:
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    content =  result.get("content", "").strip()
    return content
  except requests.exceptions.RequestException as e:
      print("Error calling Qwen API:", e)
      return "Error: Qwen server not available."
