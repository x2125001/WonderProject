import streamlit as st 
import re
from gensim.utils import tokenize
import nltk
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import numpy as  np   
import datetime
import numpy as np
from datetime import datetime as dt
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
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
data=data.drop(columns=['year','month'])
data['createdat']=data['createdat'].apply(pd.to_datetime)
data['year_month']=data['createdat'].dt.strftime('%Y-%m')
data.groupby(['year_month','dao'])['id'].nunique()
data=pd.DataFrame(data.groupby(['year_month','dao'])['id'].nunique())
data.reset_index(inplace=True)
#data.groupby(['year','month'])['dao'].nunique()
data=pd.DataFrame(data.groupby(['year_month'])['dao'].nunique())
data.reset_index(inplace=True)
fig=go.Figure()
fig.add_trace(go.Bar(x=data['year_month'].sort_values().unique(),y=data['dao'],marker_color='blue'))
st.title('Numbers of Active DAOs by Month')
st.write(fig)
data=pd.DataFrame(SQL_Query)
data=data[data['status']=='DONE']
data['year_month']=data['timestamp'].apply(pd.to_datetime).dt.strftime('%Y-%m')
#st.write(data)
data=data.groupby(['year_month','dao'])['dao'].value_counts().groupby(level=0, group_keys=False).head(3)
data=data.reset_index()
data=pd.DataFrame(data)
#data=data.groupby(['year_month','dao'])
#st.write(data.apply(lambda x: x.nlargest(2, 'id')))
data.reset_index(drop=True,inplace=True)
names=data['dao'].unique().tolist()
#data=pd.DataFrame(data.groupby(['year_month','dao'])['id'])
fig=go.Figure()
for value in names:
    i=data[data['dao']==value]
    fig.add_trace(go.Bar(name=value,x=i['year_month'].sort_values().unique(),y=i['count'],width=40))
st.title('Top three daos with most completed tasks by month')
st.write(fig)