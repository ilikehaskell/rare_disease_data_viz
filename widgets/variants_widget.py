import streamlit as st
import pandas as pd

from data_store import variants_df

def variants_widget():
    st.write(variants_df.head())
    country_df = variants_df[variants_df.country == "Romania"]
