import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY =  os.getenv("API_KEY")
def generating_masking_prompt(role, text):
  prompt = f"""
  You are an AI assistant for data privacy. Detect and mask sensitive data based on the user's role.
  **User Role:** {role}
  **Step 1 - Identify Role:**  
  - Analyze the document and infer the user's role selected (e.g., HR, IT, Manager, Legal, Finance, etc.). 
  - Maybe for HR role, you can revel employee email id, phone number.
  - If the role is not clear, make an educated guess based on the text.  
  - Use the role to determine the masking rules for sensitive data.
  - Mask the sensitive data using * using length of string.
  - Based on the role, generate an **appropriate policies** that alings with its responsibilities.
  - The policy should be professional, relavant, and aliagn with the role.
  - Ensure the policy covers key aspects like compliance, ethical considerations, and data handling.


  **Input Document:**
  {text}

  **Masked Output:**
  (Censor the sensitive data according to the role.)
  """
  return prompt
  

def generate_masked_text(role, text):
  prompt = generating_masking_prompt(role, text)
  genai.configure(api_key=API_KEY)
  model = genai.GenerativeModel("gemini-1.5-pro-002")
  response = model.generate_content(prompt)
  return response.text