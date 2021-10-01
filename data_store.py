import streamlit as st
import pandas as pd
import numpy as np

@st.cache(allow_output_mutation=True)
def get_vaccine_df():
    vaccine_data = "https://opendata.ecdc.europa.eu/covid19/vaccine_tracker/csv/data.csv"
    return pd.read_csv(vaccine_data)

@st.cache(allow_output_mutation=True)
def get_variants_df():
    variants_data = "https://opendata.ecdc.europa.eu/covid19/virusvariant/csv/data.csv"
    return pd.read_csv(variants_data)

@st.cache(allow_output_mutation=True)
def get_notification_rate_df():
    notification_rate_data = "https://opendata.ecdc.europa.eu/covid19/nationalcasedeath/csv/data.csv"
    return pd.read_csv(notification_rate_data)



vaccine_df = get_vaccine_df()
variants_df = get_variants_df()
notification_rate_df = get_notification_rate_df()