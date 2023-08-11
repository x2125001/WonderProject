""" 
helo world in the streamlite 


"""
import streamlit as st
st.title('Welcome to Wonders')

import numpy as  np   
import datetime
import numpy as np
from datetime import datetime as dt
import pathlib
#import plotly.io as pio
import streamlit as st
import pandas as pd
from utilis import *
from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://postgres:Xw21872802?@localhost/wonders")
query='select * from data'
SQL_Query = pd.read_sql(query, engine)
data=pd.DataFrame(SQL_Query)
q="select year,month,id,name,case when counts<=1 then '<=1' \
when 2<=counts and counts<=5 then '2-5' when 6<=counts and counts<=10 then '6-10' when counts>10 then '>10'  \
end As bins from data  group by year, month,id,name,counts order by year,month, counts;"
C="select * from duration"
competion=pd.DataFrame(pd.read_sql(C, engine))
bin=pd.DataFrame(pd.read_sql(q, engine))
#data=pd.read_csv(r'C:\Users\x2125\Desktop\Wonders\WonderProject\full.csv',low_memory=False)
#Tasks_Completed=data['status'].value_counts()['DONE']
#Tasks_TODO=data['status'].value_counts()['TODO']
#Tasks_INPROGRESS=data['status'].value_counts()['IN_PROGRESS']
#Tasks_IN_REVIEW=data['status'].value_counts()['IN_REVIEW']
data['month_year']=pd.to_datetime(data['timestamp']).dt.strftime('%Y-%m')
kpi1, kpi2, kpi3,kpi4,kpi5 = st.columns(5)
with kpi1:
    st.metric(
    label="Applied Tasks",
    value='93%',
    delta=None
)
    


with kpi2:
    st.metric(
    label="Tasks completed ✅",
    value='72%',
    delta=None
)
with kpi3:
    st.metric(
    label="Tasks In_Review ❓",
    value='2%',
    delta=None
)

with kpi4:
    st.metric(
    label="Tasks In_Progress 🏃‍♂️",
    value='6%',
    delta=None
)
with kpi5:
    st.metric(
    label="Tasks To_Do",
    value='20%',
    delta=None
)


column1,column2,column3=st.columns(3)
with column1:
 st.metric(
    label=":green[Average Task Completion Time]",
    value=str(round(competion[competion['duration']>0]['duration'].mean(),2))+' '+'days',
    delta=None)
with column2:
  st.metric(
    label=":blue[Median Task Completion Time]",
    value=str(round(competion[competion['duration']>0]['duration'].median(),2))+' '+'days',
    delta=None)
with column3:
  st.metric(
    label=":blue[Median Task Completion Time]",
    value=str(round(competion[competion['duration']>0]['duration'].median(),2))+' '+'days',
    delta=None)
#st.write(data)
fig=go.Figure()
#st.write(data)
colors = ['lightslategray','lightgreen','crimson','orange']
#for j 
import plotly.graph_objects as go
a=[]
fig=go.Figure()
priorities=list(data['priority'].unique())
priorities.remove('NONE')
for j in priorities:
           a.append(data[data['priority']==j]['id'].nunique())        
fig.add_trace(go.Bar(x=priorities,y=a,marker_color=colors))  
st.title('Task By Priority') 
st.write(fig)
data=data[(data['priority']!='NONE')&(data['status_current'].isin(['DONE','TODO','IN_PROGRESS','IN_REVIEW']))]
z=[]
for i in priorities:
     p=[]
     for j in data['status_current'].unique():
                    p.append(data[(data['priority']==i)&(data['status_current']==j)]['id'].nunique())
     z.append(p)          
 
#st.write(z)
fig = go.Figure()
fig.add_trace(go.Heatmap(
                    z=z,x=priorities,
        y=data['status_current'].unique(),colorscale='Viridis'))
st.title('Task By Priority and Status') 
st.write(fig)