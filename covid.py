import streamlit as st

from src.widgets.vaccine_widget import vaccine_widget
from src.widgets.variants_widget import variants_widget
from src.widgets.notification_rate_widget import notification_rate_widget

from src.pdf import get_notification_pdf, get_vaccine_pdf

def main():
    pdf_container = st.container()

    columns = st.sidebar.slider('Display on columns', 1, 4, 1)

    d = st.sidebar.radio("Data", "vaccine variants notification_rate".split())

    for column in st.columns(columns):
        with column:
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