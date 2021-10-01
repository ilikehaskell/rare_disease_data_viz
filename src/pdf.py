import streamlit as st

def get_vaccine_pdf(st):
    st.markdown("""
        <embed src="https://www.ecdc.europa.eu/sites/default/files/documents/Variable_Dictionary_VaccineTracker-20-08-2021.pdf" width="800" height="400">
        """, unsafe_allow_html=True)

def get_notification_pdf(st):
    st.markdown("""
        <embed src="https://www.ecdc.europa.eu/sites/default/files/documents/2021-01-13_Variable_Dictionary_and_Disclaimer_national_weekly_data.pdf" width="800" height="400">
        """, unsafe_allow_html=True)
