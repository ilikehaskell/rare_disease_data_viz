import streamlit as st
import pandas as pd

from ..data_store import notification_rate_df

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