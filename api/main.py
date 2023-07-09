from fastapi import FastAPI 
from pydantic import BaseModel 
from model.model import preprocessing_prediction
from model.model import _version_ as model_version 

app=FastAPI()
class TextIn(BaseModel):
    text:str
class prediction(BaseModel):
    bounty:float
@app.get("/")
def home():
    return {"health_check":"OK","model_version":model_version}
@app.post("/predict",response_model=prediction)
def predict(payload:TextIn):
    bounty=preprocessing_prediction(payload.text)
    return {"bounty":bounty}
      