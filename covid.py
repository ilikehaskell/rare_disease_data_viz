import streamlit as st
st.set_page_config(layout="wide")

from src.widgets.vaccine_widget import vaccine_widget
from src.widgets.variants_widget import variants_widget
from src.widgets.notification_rate_widget import notification_rate_widget

from src.pdf import get_notification_pdf, get_vaccine_pdf
from src.widgets.age_groups import get_groups

def main():
    pdf_container = st.container()

    columns = st.sidebar.slider('Display on columns', 1, 4, 1)

    d = st.sidebar.radio("Data", "vaccine variants notification_rate".split())

    if d == 'vaccine':
        ggroups = get_groups()
        
        for column_idx, column in enumerate(st.columns(columns)):
            with column:
                vaccine_widget(*ggroups, key = column_idx)


    for column_idx, column in enumerate(st.columns(columns)):
        # st.write(column)
        
        if d == 'variants':
            with column:
                variants_widget(key = column_idx)
        if d == 'notification_rate':
            with column:
                notification_rate_widget(key = column_idx)

    if st.sidebar.checkbox('View Vaccine PDF'):
        get_vaccine_pdf(pdf_container)
    if st.sidebar.checkbox('View Notification PDF'):
        get_notification_pdf(pdf_container)



if __name__ == '__main__':
    main()