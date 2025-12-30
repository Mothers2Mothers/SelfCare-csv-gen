import streamlit as st
from utils.do import run_pipeline

# path = r"C:\Users\Siphiwe Themba\Desktop\code\files\2025 Self-Care Outputs (Q2).xlsx"
# path2 = r"C:\Users\Siphiwe Themba\Desktop\code\files\DHIS2 events (Q3).csv"

st.title('Selfcare File Processing Pipeline')

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    output_file = run_pipeline(uploaded_file)

    st.download_button(label="Download Processed File",
                       data=output_file,
                       file_name=f"processed_selfcare_{curr}.csv",
                       mime="text/csv")
    