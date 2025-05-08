
import pandas as pd
import os
from dotenv import load_dotenv
from typing import Any
from utils import call_qwen,fetch_tables, api_calling

load_dotenv()

API_KEY =  os.getenv("API_KEY")
def generating_sql_query(user_query):
  
  tables, table_columns = fetch_tables()
  print(tables)
  #Convert table names into a string for AI reference
  table_list_user =", ".join(tables)
  print(table_list_user)
  schema_info = "\n".join(
    f"- {table}: {', '.join(cols)}" for table, cols in table_columns.items()
  )
  prompt = f"""
  You are an intelligent AI SQL assistant. Your task is to translate the user query into a valid SQL query for an SQLite database.

  **User Query:** {user_query}
  
  **Database Information:**
  - Available tables: {table_list_user}

  **Database Schema:**
   {schema_info}

  **Instructions:**
  - Only use columns that exist in the schema.
  - Avoid using any non-existent columns or tables.
  - Ensure the query is valid for SQLite.
  - Add filters like WHERE conditions if appropriate.
  - Do not use markdown formatting or SQL tags.

  **Final SQL Query:**
  """
  sql_query = generate_sql_query_using_prompt(prompt,table_list_user)
  return sql_query

def generating_masking_prompt(role, column_names, records):
    record_details = ""
    for record in records:
        record_details += "\n".join([f"{col}: {val}" for col, val in zip(column_names, record)])
        record_details += "\n\n"

    prompt = f"""
  You are an AI assistant specializing in **data masking and role-based access control**.

  Your task is to:
  1. Mask sensitive employee information based on the user's role.
  2. Explain why each field was masked (if it was).

  ### Masking Rules:
  - Aadhaar number, phone number, and personal email should be **masked** for all roles **except** HR and Legal.
  - Office email should be **masked** only for role = "General".
  - Use asterisks `*` for masking, keeping the same number of characters as the original value.
  - Never remove fields — always show them (masked or not).

  ---

  ### Input
  **User Role:** {role}

  **Record(s):**
  {record_details}

  ---

  ### Output Format:
  - Masked Record:
      field_name: value_or_masked_value
      ...
  - Explanation:
      field_name: reason_if_masked

  Only return the output in the format shown above. Do not add any code or markdown.
    """

    return prompt


def generating_masking_prompt(role, column_names, records,masked_output=None):
  record_details = ""
  for record in records:
      record_details += "\n".join([f"{col}: {val}" for col, val in zip(column_names, record)])
      record_details += "\n\n"

  prompt = f"""
  You are an AI assistant for data privacy. Detect and mask sensitive data based on the user's role.
  **User Role:** {role}
  **Step 1 - Identify Role:**  
  - Analyze the record infer the user's role selected (e.g., HR, IT, Manager, Legal, Finance, etc.). 
  - The office email address should be visible to all role except General but the personal email address should be masked to all Role.
  - Mask the sensitive data using * using length of string.
  - Use the role to determine the masking rules for sensitive data.
  - If the role is not clear, make an educated guess based on the text.  
 
  **Input Document:**
  {records}

  **Context:**
  {record_details}

  **Masked Output:**
  (Censor the sensitive data according to the role.)

  **Step 2 - {role} Policy:**  
  - Explain why each field was masked (mention the field name) without showing the data.
  - Explain why it was important to mask the data. 
  - Use role-based access logic.
  - Use bullet points.
  """
  # """
  # prompt2 = f"""
  #   You are an AI assistant for data privacy
  #   Based on **role-based access control**, explain why certain fields were masked.
  #   **User Role:** {role}
  #   **Masked Output (already generated):**
  #   {masked_output if masked_output else "None provided"}
  #   **Step 2 - Generate Policy Explanation:**
  #   - Explain why masking is required for each type, considering privacy and access control.
  #   - Please dont show the data while explaining.
  #   - Use bullet points and mention specific field names.
  #   - Keep the explanation practical and not generic.

  #   **Context:**
  #   {record_details}

  #   Example Output:
  #   - **Bank Account**: Masked because this role doesn't require access to financial data.
  #   - **Aadhar Card**: Masked due to privacy laws restricting exposure of national ID numbers.
  #   - **Phone Number**: Only HR is allowed to see employee contact details.

  
  return prompt

def generate_sql_query_using_prompt(prompt, tables):
  
  model = api_calling(API_KEY)
  response = model.generate_content(prompt)
  print(response)
  sql_query = response.text.strip()
  return sql_query

# def generate_sql_query_using_prompt(prompt, tables):
  
#   sql_query = call_qwen(prompt)
#   queries = [q.strip() for q in sql_query.split(';') if q.strip()]
#   if not queries:
#     raise ValueError("No valid SQL query generated by Qwen.")
#   return queries[0]

# def generate_masked_and_policy_text(role,columns_names, records):

#   response = generating_masking_prompt(role, columns_names,records)
#   masked_text = call_qwen(response)
#   return masked_text

def generate_masked_and_policy_text(role,columns_names, records):

  masked_output = generating_masking_prompt(role, columns_names,records)
  model = api_calling(API_KEY)

  response1 = model.generate_content(masked_output)
  masked_text =response1.text

  # response2 = model.generate_content(policy_prompt)
  # policy_text = response2.text

  return masked_text
