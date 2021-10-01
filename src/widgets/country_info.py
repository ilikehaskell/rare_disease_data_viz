import streamlit as st

from ..data_store import vaccine_df

def get_country_info(country, country_df, st=st, key = 0):
    st.write(
        f"""Age groups vaccinated in {country}:\n
        { ", ".join(set(country_df.TargetGroup))}"""
    )
    st.write(
        f"""Age groups not yet vaccinated in {country}:\n
        { ", ".join(set(vaccine_df.TargetGroup) - set(country_df.TargetGroup))}"""
    )
    st.write(
        f"""Vaccines used in {country}: {", ". join(set(country_df.Vaccine))}"""
    )
    st.write(
        f"""Vaccines not used in {country}: {", ". join(set(vaccine_df.Vaccine) - set(country_df.Vaccine))}"""
    )