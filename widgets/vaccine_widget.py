import streamlit as st
import pandas as pd
import numpy as np

from data_store import vaccine_df
from plot_utils import plotable

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





def vaccine_widget():
    # st.write(vaccine_df.head())


    countries = sorted(list(set(vaccine_df.ReportingCountry)))
    romania_index = countries.index('RO')
    country = st.selectbox('Country', options=countries, index=romania_index)
    country_df = vaccine_df[vaccine_df.ReportingCountry == country]

    denominator_group_dict = country_df.groupby('TargetGroup').first().Denominator.fillna(0).to_dict()
    
    groups, special_groups = get_groups(country, country_df)

    population_considered = sum(denominator_group_dict[group] for group in groups+special_groups if group in denominator_group_dict)
    country_population = country_df.groupby('ReportingCountry').first().Population[0]


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
    full_df['FullVaccinePercentageFromGroups'] = full_df.TotalFullVaccine / population_considered
    full_df['FullVaccinePercentage'] = full_df.TotalFullVaccine / country_population
    st.header(country_population)
    st.header('Number of doses received')
    st.line_chart(
        plotable(full_df.NumberDosesReceived)
        )
    
    full_df.FullVaccine



    st.header('Number of doses received')
    st.line_chart(
        plotable(full_df.FullVaccine)
        )

    st.header('Percentage of fully vaccinated from selected groups')
    full_df
    fff = full_df[['FullVaccinePercentage', 'FullVaccinePercentageFromGroups', 'TotalFullVaccine']]
    plotable(fff)
    st.line_chart(plotable(fff))
    st.line_chart(full_df['FullVaccinePercentage'])

    st.header('Number of fully vaccinated')
    st.line_chart(full_df['TotalFullVaccine'])