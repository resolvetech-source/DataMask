import pandas as pd
import os
import PyPDF2


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
  pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
  text = ''
  for page_num in range(pdf_reader.numPages):
    if page.extract_text():
        page = pdf_reader.getPage(page_num)
        text += page.extract_text()
  return text