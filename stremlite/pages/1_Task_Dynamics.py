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

fig=go.Figure()
list=['done','todo','in_progress','in_review']
data=data[data['status'].str.lower().isin(list)]
list=['done','todo','in_progress','in_review']
time=[i for i in data['month_year'].sort_values().unique()]
for j in list:
    k=[]
    for i in data['month_year'].sort_values().unique():  
           k.append(data[(data['status'].str.lower()==j) & (data['month_year']==i)]['id'].count())              
    fig.add_trace(go.Bar(x=data['month_year'].sort_values().unique(),y=k,name=j.upper()))                        
           
fig.update_layout(barmode='group', xaxis={'categoryorder':'category ascending'})

st.title('Tasks Dynamics by Month')
bin['date'] = pd.to_datetime(bin[['year', 'month']].assign(DAY=1)).dt.strftime('%Y-%m')
st.write(fig)   
#data.groupby(['month_year,id'])   
fig=go.Figure()
for j in bin['bins'].unique():
    k=[]
    for i in bin['date'].sort_values().unique():  
           k.append(bin[(bin['bins']==j) & (bin['date']==i)]['id'].count())              
    fig.add_trace(go.Bar(x=bin['date'].sort_values().unique(),y=k,name='User participation '+j.upper()))                      
           
fig.update_layout(barmode='group', xaxis={'categoryorder':'category ascending'},yaxis_title="Number of Taks")
st.title('User Participation By months')
st.write(fig)
#st.write(competion)
competion=competion[competion['duration']>0][competion['priority']!='NONE']
fig=go.Figure()
for i in competion['priority'].unique():
   fig.add_trace(go.Histogram(x=competion[competion['priority']==i]['duration'],bingroup=1,name=i)) 

#competion['duration']=competion['duration'].apply(pd.to_datetime)
           
fig.update_layout(barmode='group', xaxis={'categoryorder':'category ascending'},xaxis_title="Days")
st.title('Task Completion Time')    
st.write(fig)

 


