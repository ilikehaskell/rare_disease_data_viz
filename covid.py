from tokenize import group
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


def get_groups(country, country_df, st=st):
    age_groups = [
        "Age0_4",
        "Age5_9",
        "Age10_14",
        "Age15_17",
        "Age18_24",
        "Age25_49",
        "Age50_59",
        "Age60_69",
        "Age70_79",
        "Age80+",
        ]
    special_age_groups = [
        "HCW",
        "LTCF",
        "AgeUNK",
        ]
    
    groups_exp = st.expander('Age & special groups')

    age_st, age_end = groups_exp.select_slider(
        'Select age ranges', 
        options=age_groups, 
        value = ("Age0_4", "Age80+",)
        )
    groups = age_groups[age_groups.index(age_st): age_groups.index(age_end)+1]
    special_groups = [special_age_group  for special_age_group in special_age_groups if groups_exp.checkbox(special_age_group)]

    groups_exp.write(
        f"""Age groups vaccinated in {country}:\n
        { ", ".join(set(country_df.TargetGroup))}"""
    )
    groups_exp.write(
        f"""Age groups not yet vaccinated in {country}:\n
        { ", ".join(set(vaccine_df.TargetGroup) - set(country_df.TargetGroup))}"""
    )

    return groups, special_groups

# @st.cache(allow_output_mutation=True)
def get_vaccine_pdf(st):
    st.markdown("""
        <embed src="https://www.ecdc.europa.eu/sites/default/files/documents/Variable_Dictionary_VaccineTracker-20-08-2021.pdf" width="800" height="400">
        """, unsafe_allow_html=True)

def get_notification_pdf(st):
    st.markdown("""
        <embed src="https://www.ecdc.europa.eu/sites/default/files/documents/2021-01-13_Variable_Dictionary_and_Disclaimer_national_weekly_data.pdf" width="800" height="400">
        """, unsafe_allow_html=True)
    

def vaccine_widget():
    # st.write(vaccine_df.head())


    countries = sorted(list(set(vaccine_df.ReportingCountry)))
    romania_index = countries.index('RO')
    country = st.selectbox('Country', options=countries, index=romania_index)
    country_df = vaccine_df[vaccine_df.ReportingCountry == country]

    denominator_group_dict = country_df.groupby('TargetGroup').first().Denominator.fillna(0).to_dict()
    
    groups, special_groups = get_groups(country, country_df)

    population_considered = sum(denominator_group_dict[group] for group in groups+special_groups if group in denominator_group_dict)

    f"""Vaccines used in {country}: {", ". join(set(country_df.Vaccine))}"""
    f"""Vaccines not used in {country}: {", ". join(set(vaccine_df.Vaccine) - set(country_df.Vaccine))}"""

    country_df = country_df.rename(columns={'YearWeekISO':'YW'})


    full_vaccine_df = country_df[["YW", "FirstDose", "SecondDose", "NumberDosesReceived", "Vaccine"]]
    full_vaccine_df['FullVaccine'] = full_vaccine_df.apply(lambda row: row.FirstDose if row.Vaccine=='JANSS' else row.SecondDose, axis=1)
    

    all_df = country_df[country_df.TargetGroup == 'ALL']
    all_df = all_df.fillna(0)
    all_df = all_df.pivot_table(
        values = ["NumberDosesReceived"],
        index="YW",
        columns=["Vaccine"],
        aggfunc=np.sum
        )

    full_vaccine_df = full_vaccine_df[country_df.TargetGroup.isin(groups+special_groups)]
    full_vaccine_df = full_vaccine_df.fillna(0)
    full_vaccine_df = full_vaccine_df.pivot_table(
        values = ["FullVaccine"],
        index="YW",
        columns=["Vaccine"],
        aggfunc=np.sum
        )

    full_df = pd.concat([full_vaccine_df, all_df[['NumberDosesReceived']] ], axis=1, join='inner')
    full_df = full_df.fillna(0)
    full_df = full_df.cumsum()
    full_df = full_df.fillna(0)

    full_df['TotalFullVaccine'] = full_df.FullVaccine.sum(axis=1)
    full_df['FullVaccinePercentage'] = full_df.TotalFullVaccine / population_considered
    
    st.header('Number of doses received')
    st.line_chart(pd.concat([full_df.NumberDosesReceived[col_name] for col_name in full_df.NumberDosesReceived.columns], axis=1))
    # concat trick needed because of strange Altair+Streamlit+Pandas pivoted DF interaction resulting in
    # ValueError: variable encoding field is specified without a type; the type cannot be inferred because it does not match any column in the data.

    full_df.FullVaccine

    st.header('Number of doses received')
    st.line_chart(pd.concat([full_df.FullVaccine[col_name] for col_name in full_df.FullVaccine.columns], axis=1))

    st.header('Percentage of fully vaccinated')
    st.line_chart(full_df['FullVaccinePercentage'])

    st.header('Number of fully vaccinated')
    st.line_chart(full_df['TotalFullVaccine'])

def variants_widget():
    st.write(variants_df.head())
    country_df = variants_df[variants_df.country == "Romania"]


def notification_rate_widget():
    countries = sorted(list(set(notification_rate_df.country)))
    romania_index = countries.index('Romania')
    country = st.selectbox('Country', options=countries, index=romania_index)

    country_df = notification_rate_df[notification_rate_df.country == country]
    country_df = country_df.rename(columns={'year_week': 'YW'})
    country_df = country_df.set_index('YW')
    country_df
    cd_df = pd.concat( [country_df[country_df.indicator == 'cases'].rate_14_day.rename('cases'), country_df[country_df.indicator == 'deaths'].rate_14_day.rename('deaths')], axis=1)
    st.line_chart(cd_df)
    st.line_chart(cd_df.deaths/cd_df.cases*100)

    # st.line_chart()



vaccine_df = get_vaccine_df()
variants_df = get_variants_df()
notification_rate_df = get_notification_rate_df()

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