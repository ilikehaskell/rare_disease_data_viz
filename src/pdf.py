import streamlit as st


pdf_markdown = """
        <embed src="%s" width="900" height="400">
        """

def get_vaccine_pdf(st=st):
    st.markdown(pdf_markdown % "https://www.ecdc.europa.eu/sites/default/files/documents/Variable_Dictionary_VaccineTracker-20-08-2021.pdf", 
    unsafe_allow_html=True)

def get_notification_pdf(st=st):
    st.markdown(pdf_markdown % "https://www.ecdc.europa.eu/sites/default/files/documents/2021-01-13_Variable_Dictionary_and_Disclaimer_national_weekly_data.pdf", 
    unsafe_allow_html=True)
