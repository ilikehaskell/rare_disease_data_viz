import streamlit as st
import pandas as pd
import numpy as np


from data_store import vaccine_df, variants_df, notification_rate_df

from widgets.vaccine_widget import vaccine_widget
from widgets.variants_widget import variants_widget
from widgets.notification_rate_widget import notification_rate_widget

def get_vaccine_pdf(st):
    st.markdown("""
        <embed src="https://www.ecdc.europa.eu/sites/default/files/documents/Variable_Dictionary_VaccineTracker-20-08-2021.pdf" width="800" height="400">
        """, unsafe_allow_html=True)

def get_notification_pdf(st):
    st.markdown("""
        <embed src="https://www.ecdc.europa.eu/sites/default/files/documents/2021-01-13_Variable_Dictionary_and_Disclaimer_national_weekly_data.pdf" width="800" height="400">
        """, unsafe_allow_html=True)


def main():
    pdf_container = st.container()
    d = st.sidebar.radio("Data", "vaccine variants notification_rate".split())
    if d == 'vaccine':
        vaccine_widget()
    if d == 'variants':
        variants_widget()
    if d == 'notification_rate':
        notification_rate_widget()

    if st.sidebar.checkbox('View Vaccine PDF'):
        get_vaccine_pdf(pdf_container)
    if st.sidebar.checkbox('View Notification PDF'):
        get_notification_pdf(pdf_container)





if __name__ == '__main__':
    main()