import pandas as pd
from tabula import read_pdf
import re
import json
from langchain_community.llms import Ollama
from docx import Document
import json
import re

import os
from scripts.pdfFile import pdf_data_extraction
from scripts.excel import excel_data_extraction
from scripts.docxFile import docs_data_extraction

def main(inputfile_path):
    # Get the file extension
    _, file_extension = os.path.splitext(inputfile_path)

    # Call the appropriate function based on the file extension
    if file_extension.lower() == '.pdf':
        # Call function to extract data from PDF
        print("\n\nData Extraction Started")
        pdf_data_extraction(inputfile_path)
    elif file_extension.lower() == '.xlsx':
        # Call function to extract data from Excel
        print("\n\nData Extraction Started")
        excel_data_extraction(inputfile_path)
    elif file_extension.lower() == '.docx':
        # Call function to extract data from DOCX
        print("\n\nData Extraction Started")
        docs_data_extraction(inputfile_path)
    else:
        print("Unsupported file format. Please provide a .pdf, .xlsx, or .docx file.")

# Example usage
if __name__ == "__main__":
    input_file = r"inputs\RFP3.docx"  # Replace with the actual path to the input file
    main(input_file)


