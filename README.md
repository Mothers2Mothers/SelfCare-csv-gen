# Self-Care File Processing App

This Streamlit application processes DHIS2 self-care CSV files and produces a cleaned, scored, and aggregated output file for reporting.

## What this app does
- Accepts a DHIS2 CSV export
- Maps self-care responses to numeric scores
- Aggregates scores by domain:
  - Physical
  - Emotional
  - Spiritual
  - Professional
  - Personal/Social
  - Financial
  - Psychological
- Filters records by the current reporting quarter
- Outputs a processed CSV file ready for analysis

## How to use the app
1. Open the app link in your browser
2. Upload the DHIS2 CSV file
3. Wait for processing to finish
4. Download the processed file

## Notes
- If the app seems slow at first, please wait a few seconds (the app may be waking up)
- If you encounter errors, contact the app owner

## Supported file format
- Input: CSV
- Output: CSV