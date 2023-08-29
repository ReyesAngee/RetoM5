import streamlit as st 
import pandas as pd 


st.title('Streamlit con cache')
DATA_URL = ('Employees.csv')

@st.cache
def load_data(nrows):
    Employees = pd.read_csv(DATA_URL, nrows=nrows)
    return Employees   

data_load_state = st.text('Loading data...')
Employees = load_data(500)
data_load_state.text('Done ! using cache...')

st.dataframe(Employees)


