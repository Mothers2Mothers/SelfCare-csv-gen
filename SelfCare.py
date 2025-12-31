import datetime
import streamlit as st
from utils.do import run_pipeline

curr = datetime.datetime.now()

st.title('Selfcare File Processing Pipeline')

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    output_file = run_pipeline(uploaded_file, curr)

    st.download_button(label="Download Processed File",
                       data=output_file,
                       file_name=f"processed_selfcare_{curr}.csv",
                       mime="text/csv")
    