from sqlalchemy import create_engine
import streamlit as st
import pandas as pd
from utilis import *
engine = create_engine("postgresql+psycopg2://postgres:Xw21872802?@localhost/wonders")

query='select year,month,count(year) as number_of_tasks,dao,status,priority from new_full group by year,dao,status,month,priority;'
SQL_Query = pd.read_sql(query, engine)
data=pd.DataFrame(SQL_Query)
st.title('Wonder Project')

left_column, right_column=st.columns([4,1])
with st.sidebar:
    st.title('Data Visualization')
with left_column:
     st.write(data)
with right_column:
     st.metric('Toatl number of tasks',data['number_of_tasks'].sum())
st.header('Visulization')
st.write(TEXTS['title'])
selected_year=st.multiselect('select a year to inspect',data['year'].unique(),data['year'].unique())


st.bar_chart(data,x='status',y='number_of_tasks')


