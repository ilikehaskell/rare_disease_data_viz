import streamlit as st

from ..data_store import vaccine_df

def get_groups(st=st, key = 0):
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
    
    groups_exp = st.expander('Age & special groups', expanded = True)

    age_st, age_end = groups_exp.select_slider(
        'Select age ranges', 
        options=age_groups, 
        value = ("Age0_4", "Age80+",),
        key = key
        )
    groups = age_groups[age_groups.index(age_st): age_groups.index(age_end)+1]
    special_groups = [special_age_group  for special_age_group in special_age_groups if groups_exp.checkbox(special_age_group, key=key)]

    return groups, special_groups
