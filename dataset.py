import streamlit as st 
import pandas as pd 
@st.cache

names_link = 'dataset.csv'
names_data = pd.read_csv(names_link)
st.title ("Read CSV")

st.dataframe(names_data)
