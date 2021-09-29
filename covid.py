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



def vaccine_widget():
    # st.write(vaccine_df.head())
    ro_df = vaccine_df[vaccine_df.ReportingCountry == "RO"]
    ro_df
    # f"""Age groups vaccinated in Romania:\n
    #     { ", ".join(set(ro_df.TargetGroup))}"""
    # f"""Age groups not yet vaccinated in Romania:\n
    #     { ", ".join(set(vaccine_df.TargetGroup) - set(ro_df.TargetGroup))}"""
    # f"""Vaccines used in Romania: {", ". join(set(ro_df.Vaccine))}"""
    # f"""Vaccines not used in Romania: {", ". join(set(vaccine_df.Vaccine) - set(ro_df.Vaccine))}"""



    r_df = vaccine_df[["YearWeekISO", "FirstDose", "SecondDose", "NumberDosesReceived", "Vaccine"]]
    r_df = r_df.rename(columns={'YearWeekISO':'YW'})
    r_df['FullVaccine'] = r_df.apply(lambda row: row.FirstDose if row.Vaccine=='JANSS' else row.SecondDose, axis=1)
    r_df = r_df[vaccine_df.ReportingCountry == "RO"]
    r_df = r_df[["YW", "Vaccine","FullVaccine", "NumberDosesReceived"]]

    r_df = r_df.pivot_table(
        values = ["FullVaccine", "NumberDosesReceived"],
        index="YW",
        columns=["Vaccine"],
        aggfunc=np.sum
        )
    r_df = r_df.fillna(0)
    
    # r_df = r_df.cumsum()
    r_df


    
    

def variants_widget():
    st.write(variants_df.head())
    ro_df = variants_df[variants_df.country == "Romania"]
    st.write(
        variants_df.ReportingCountry
    )
    

def notification_rate_widget():
    st.write(notification_rate_df.head())
    ro_df = notification_rate_df[notification_rate_df.country == "Romania"]
    ro_df


vaccine_df = get_vaccine_df()
variants_df = get_variants_df()
notification_rate_df = get_notification_rate_df()

def main():
    d = st.sidebar.radio("Data", "vaccine variants notification_rate".split())
    if d == 'vaccine':
        vaccine_widget()
    if d == 'variants':
        variants_widget()
    if d == 'notification_rate':
        notification_rate_widget()







if __name__ == '__main__':
    main()