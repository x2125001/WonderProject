#!pip install -U scikit-learn
import pickle
import pandas as pd
import re 
from pathlib import Path 
_version_='0.01'
#BASE_DIR=Path(_file_).resolve(strict=True).parent
with open(r'C:\Users\x2125\Desktop\Wonders\WonderProject\api\model\trained_pipeline_0.01.pkl','rb') as f:
    model=pickle.load(f)
def preprocessing_prediction(instance):
    data=pd.read_csv(r'C:\Users\x2125\Desktop\full.csv')
    data=data.drop(columns=['rewards'],axis=1)
    data=data.dropna(subset=['reward'])
    data=data[data['reward']>0]
    data=data[data['status'].isin(['DONE','TODO','IN_REVIEW','IN_PROGESS'])]
    data['description']=data['description'].fillna('None')
    instance=data[data['id']==instance]
    instance['description']=instance['description'].apply(lambda x:re.sub('[^a-zA-Z ]','',x))            
    instance['description']=instance['description'].apply(lambda x:re.sub('(https\S+)','',x))
    pred=model.predict(instance)
    return pred

