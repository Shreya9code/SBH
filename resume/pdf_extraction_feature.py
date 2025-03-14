import os
import streamlit as st
from PyPDF2 import PdfReader
import re
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ✅ Function: Extract text from PDF
def extract_text_from_pdf(pdf_file):
    """Extracts text from a given PDF file."""
    with pdfplumber.open(pdf_file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    # Remove extra spaces and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text
    '''try:
        reader = PdfReader(pdf_file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None'''

# ✅ Function: Split extracted text into smaller chunks
def split_text(text):
    """Splits extracted text into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(text)
