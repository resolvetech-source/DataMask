import google.generativeai as genai
import pandas as pd


API_KEY = "AIzaSyABiZeC91TuBFvvXr3G3tQLUlTHqX8Es8o"


def get_masking_rules(role):
  masking_df = pd.DataFrame({
    "Role" : ['HR','IT','Manager','Finance','Legal'],
    "Masked columns":[
        ["Aadhar Card", "Bank Account", "PAN Card", "IFSC Code"], # For HR
        ["Aadhar Card", "Bank Account", "PAN Card", "IFSC Code"], # IT
        ["Aadhar Card", "Bank Account", "PAN Card", "IFSC Code"], #Manager
        ["No Masking required"], # Finance
        ["No Masking required"] # Legal
      ]
  })
  row = masking_df[masking_df['Role'] == role]

  if not row.empty:
    return row["Masked columns"].values[0]
  
def generating_masking_prompt(role, text):
  masking_rules = get_masking_rules(role)
  print(masking_rules)
  if role == "HR":
    masking_instruction = "Partially mask the fields (show last 4 digits)."

  else:
    masking_instruction = "Full mask the fields with the help of length of string replace it with * and dont show salary"

  # create a dynamic masking rule string
  masking_rule_str = ', '.join(masking_rules)
  # Generate prompt dynamically
  prompt = f"""
  You are an AI assistant that masks sentitive information from text.
  **User Role:** {role}
  **Masking Rules:** {masking_rule_str}
  **Masking Instruction:** {masking_instruction}

  **Input Document:**
  {text}

  **Masked Output:**
  """
  return prompt


def generate_masked_text(role, text):
  prompt = generating_masking_prompt(role, text)
  genai.configure(api_key=API_KEY)
  model = genai.GenerativeModel("gemini-1.5-pro")
  response = model.generate_content(prompt)
  return response.text