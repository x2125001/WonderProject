# WonderProject
<h1 align="center">Welcome to the Wonder Project 👋</h1>
<p align="center">
  <img src="https://dework.xyz/board.jpeg" />
</p>
<h1 align="center"> Description </h1>
In this Project, over 40k tasks from Dework, the web3-platform are scrapped and analyzed. Specifically, data extraction, ingestion, cleaning & wrangling, KPI analysis, visualization, topic modeling, and bounty regression are implemented. The scrapping tasks are implemented by the selenium libarary. However, for completness, the scrapy implementation or the requests post method are also possible.
For Visualization please run the following command under the directory of stremlite:

```sh
streamlit run KPIs.py
```
<p align="center">
  <img src="https://github.com/x2125001/WonderProject/blob/1070631df9a564a6f674a655367716b484226610/pp.png" />
</p>

The results of topic modelling, using the LDA from gensim package will have the yield the following six distinct topics, visualized by the TSNE embeddings 
<p align="center">
  <img src="https://github.com/x2125001/WonderProject/blob/93c36db8fa9a284ac16db6278a8c75b5de6669aa/e.PNG" />
</p>

<h1 align="center"> 🚀 Bounty Regression </h1>
On top of the features of dao, priority, task status, all categorical, the text features from the task description are added. Feature engineering is implemented. Here specifically, the sentence embedding model is utilized and numerical features are extracted per sentence. Then the PCA dimensional reduction is implemented. Notice that the PCA was fitted on the training data only then used to transform the test feature embeddings. This restriction is necessary to avoid the 'cheating' and so to really test the model out. 
The below table reports the R-square metric each for the models trained. StackingRegressor is trained as an ensemble of all other models, namely Knn,Ridge, SVM, xgb,and randomforest. 

Fitted models | boosting_regressor | RandomForest | KNeighborsRegressor | StackingRegressor | Ridge | xgb
--- | --- | --- | --- |--- |--- |--- 
R-square |  | 0.234 | 0.3086 | 0.3587 | 0.1540 | 0.2134

The best model saved from the  stackingRegressor is deployed using the fast API, which is then integrated into the streamlit in the page of Bounty Regression, where the user can specify the levels of task priority and task status and then get the model predicted average bounty

Thanks very much for the interests.



