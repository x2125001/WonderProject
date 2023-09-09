import json
#import multiprocessing
from selenium import webdriver
import pickle
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from sqlalchemy import create_engine
def Scrape(dao,url):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        wd=webdriver.Chrome(options=options)
        wd.maximize_window()
        wd.get(url)
        DAO=dao
        try:
           WebDriverWait(wd, timeout=40).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.mb-7")))
        except TimeoutException:
           print(url)
        try:status=wd.find_element(By.CSS_SELECTOR,"div[style='column-gap: 8px;']").get_property("innerText")
        except:status=None
        try:task_title=wd.find_element(By.CSS_SELECTOR,"div.ant-form-item-control-input textarea#Task\ Form\ \(update\)_name").get_property("textContent")
        except:task_title=None
        try:due_date=wd.find_element(By.CSS_SELECTOR,"span.anticon-calendar[role='img'][aria-label='calendar']+span").get_property("innerText")
        except:due_date=None
        try:wd.find_element(By.CSS_SELECTOR,"div.mb-7 button strong").click()
        except:pass
        try:task_description=wd.find_element(By.CSS_SELECTOR,"div.mb-7").get_property("innerText")
        except:task_description=None
        task_activities=wd.find_elements(By.CSS_SELECTOR,"div.ant-timeline-item-content div.ant-row.ant-row-middle[role='row']")
        activities=[]
        time_stamps=[]
        try:bounties=wd.find_element(By.CSS_SELECTOR,"span.ant-tag[style='background-color: white; color: black; min-width: 0px; overflow: hidden; text-overflow: ellipsis;']").get_property("innerText")
        except: bounties=None
      
         
        try:reviwers=wd.find_element(By.CSS_SELECTOR,"div.ant-row.ant-form-item:has( label[for='Task Form (update)_ownerIds'])").find_element(By.CSS_SELECTOR,"div:nth-child(2)").get_property("innerText")   
        except:reviwers=None 
        try:priority=wd.find_element(By.CSS_SELECTOR,"div.ant-row.ant-form-item:has( label[for='Task Form (update)_priority'])").find_element(By.CSS_SELECTOR,"div:nth-child(2)").get_property("innerText")
        except:priority=None  
        try:activity_comments=[i.text for i in wd.find_elements(By.CSS_SELECTOR,"div.ant-timeline-item-content div.ProseMirror[role='textbox'][contenteditable='false'] > p")]
        except:activity_comments=None
        for activity in task_activities:
                                 #print(activity.text+"/")
            try:activities.append(activity.find_element(By.CLASS_NAME,"ant-typography").get_property("innerText"))
            except:pass
            try:time_stamps.append(activity.find_element(By.CLASS_NAME,"ant-typography-secondary").get_property("innerText"))
            except:pass
        try:subtasks=[i.get_property("innerText") for i in wd.find_elements(By.CSS_SELECTOR,"td.ant-table-cell.w-full > div.ant-typography")]
        except:subtasks=None 
        try:subtasks_id=[i.get_attribute("data-row-key") for i in wd.find_elements(By.CSS_SELECTOR,"tbody.ant-table-tbody > tr[data-row-key][index]")]
        except:subtasks_id=None
        try: tags=[i.find_element(By.CSS_SELECTOR,"span.ant-tag").get_property("innerText") for i in wd.find_elements(By.CSS_SELECTOR,"div.ant-select-selection-overflow-item > span")]
        except:tags=None
        data={"due_date":due_date,"activity_comments":activity_comments,"link":url,"status":status,"tags":tags,"subtasks_id":subtasks_id,"reviewers":reviwers,"DAO":DAO,"time_stamps":time_stamps,"activities": activities,"subtasks":subtasks,"priority":priority,"task_title":task_title,"task_description":task_description,"subtasks":subtasks,"bounties":bounties}
 
       
       
        df=pd.DataFrame.from_records([data])
        engine = create_engine("postgresql+psycopg2://postgres:Xw21872802?@localhost/wonders")
        with engine.begin() as connection:
               df.to_sql('lasts', con=connection, if_exists='append')
        wd.close()
        print("success")
if __name__ == '__main__':
     with open('id.pickle', 'rb') as handle:
                  id= pickle.load(handle)
    
               
     for dao, links in id.items():
         for link in links:
                  Scrape(dao,link)
     