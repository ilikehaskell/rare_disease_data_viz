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

def vaccine_widget():
    # st.write(vaccine_df.head())


    countries = sorted(list(set(vaccine_df.ReportingCountry)))
    romania_index = countries.index('RO')
    country = st.selectbox('Country', options=countries, index=romania_index)
    country_df = vaccine_df[vaccine_df.ReportingCountry == country]
    country_df

    denominator_group_dict = country_df.groupby('TargetGroup').first().Denominator.fillna(0).to_dict()
    
    groups, special_groups = get_groups(country, country_df)

    population_considered = sum(denominator_group_dict[group] for group in groups+special_groups if group in denominator_group_dict)

    f"""Vaccines used in {country}: {", ". join(set(country_df.Vaccine))}"""
    f"""Vaccines not used in {country}: {", ". join(set(vaccine_df.Vaccine) - set(country_df.Vaccine))}"""

    country_df = country_df.rename(columns={'YearWeekISO':'YW'})


    r_df = country_df[["YW", "FirstDose", "SecondDose", "NumberDosesReceived", "Vaccine"]]
    r_df['FullVaccine'] = r_df.apply(lambda row: row.FirstDose if row.Vaccine=='JANSS' else row.SecondDose, axis=1)
    


    # r_df = r_df[vaccine_df.ReportingCountry == country]
    


    all_df = country_df[country_df.TargetGroup == 'ALL']
    all_df = all_df.fillna(0)
    all_df = all_df.pivot_table(
        values = ["NumberDosesReceived"],
        index="YW",
        columns=["Vaccine"],
        aggfunc=np.sum
        )

    r_df = r_df[country_df.TargetGroup.isin(groups+special_groups)]
    r_df = r_df.fillna(0)
    r_df = r_df.pivot_table(
        values = ["FullVaccine"],
        index="YW",
        columns=["Vaccine"],
        aggfunc=np.sum
        )

    r_df = pd.concat([r_df, all_df[['NumberDosesReceived']] ], axis=1, join='inner')
    r_df = r_df.fillna(0)
    r_df = r_df.cumsum()
    r_df = r_df.fillna(0)

    r_df['TotalFullVaccine'] = r_df.FullVaccine.sum(axis=1)
    r_df['FullVaccinePercentage'] = r_df.TotalFullVaccine / population_considered
    cucu = pd.DataFrame([[1.0,2],[3,4]], columns=['u','b'])
    "cuc"
    st.write(
        pd.DataFrame(r_df.NumberDosesReceived[['AZ', 'COM']]),
        pd.concat([r_df.NumberDosesReceived['AZ'], r_df.NumberDosesReceived['COM']], axis=1)
        
    )
    
    
    st.line_chart(cucu)
    st.line_chart(pd.concat([r_df.NumberDosesReceived[col_name] for col_name in r_df.NumberDosesReceived.columns], axis=1))
    # concat trick needed because of strange Altair+Streamlit+Pandas pivoted DF interaction resulting in
    # ValueError: variable encoding field is specified without a type; the type cannot be inferred because it does not match any column in the data.
    st.line_chart(pd.concat([r_df.FullVaccine[col_name] for col_name in r_df.FullVaccine.columns], axis=1))
    st.line_chart(r_df[['FullVaccinePercentage', 'TotalFullVaccine']])
    

def variants_widget():
    st.write(variants_df.head())
    country_df = variants_df[variants_df.country == "Romania"]


def notification_rate_widget():
    st.write(notification_rate_df.head())
    country_df = notification_rate_df[notification_rate_df.country == "Romania"]
    country_df


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






if __name__ == '__main__':
    main()