#from sqlalchemy import create_engine
import numpy as  np   
import datetime
import numpy as np
from datetime import datetime as dt
import pathlib
#import plotly.io as pio
import streamlit as st
import pandas as pd
from utilis import *
#engine = create_engine("postgresql+psycopg2://postgres:Xw21872802?@localhost/wonders")
#query='select year,month,count(year) as number_of_tasks,dao,status,priority from new_full group by year,dao,status,month,priority;'
#SQL_Query = pd.read_sql(query, engine)
#data=pd.DataFrame(SQL_Query)]


data=pd.read_csv(r'C:\Users\x2125\Desktop\Wonders\WonderProject\full.csv',low_memory=False)
Tasks_Completed=data['status'].value_counts()['DONE']
Tasks_TODO=data['status'].value_counts()['TODO']
Tasks_INPROGRESS=data['status'].value_counts()['IN_PROGRESS']
Tasks_IN_REVIEW=data['status'].value_counts()['IN_REVIEW']
data['month_year']=data['creat'].apply(pd.to_datetime).dt.to_period('M')
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(
    label="Tasks completed ✅",
    value=Tasks_Completed,
    delta=round(100) - 10,
)
with kpi2:
    st.metric(
    label="Tasks In_Review ❓",
    value=Tasks_IN_REVIEW,
    delta=round(100) - 10,
)

with kpi3:
    st.metric(
    label="Tasks In_Progress 🏃‍♂️",
    value=Tasks_INPROGRESS,
    delta=round(100) - 10,
)
fig=go.Figure()
status=data['status'].unique().tolist()
list=['DONE','TODO','IN_PROGRESS','IN_REVIEW']
time=[i for i in data['month_year'].sort_values().unique()]
for j in list:
    k=[]
    for i in data['month_year'].sort_values().unique():  
           k.append(data[(data['status']==j) & (data['month_year']==i)]['id'].count())              
    fig.add_trace(go.Bar(x=data['month_year'].sort_values().unique(),y=k,marker_color='crimson'))                        
           
#fig.update_layout(barmode='stack', xaxis={'categoryorder':'category ascending'})
st.title('Tasks by status')
st.write(fig)   
    



 


