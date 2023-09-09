import re
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import matplotlib.colors as mcolors
from sklearn.manifold import TSNE
from gensim.utils import tokenize
from nltk.stem import *
import nltk
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import streamlit as st
import plotly.express as px
import numpy as  np   
import datetime
import numpy as np
from datetime import datetime as dt
from nltk.corpus import stopwords 
import pandas as pd 
import matplotlib.pyplot as plt
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stop_words.update(['p','e','b','f','c','xc','pm','h','x','n','de','que'])
stemmer = PorterStemmer()
data=pd.read_csv(r'C:\Users\x2125\Desktop\Wonders\WonderProject\data.csv')
data.head()
data.description=data.description.apply(lambda x:re.sub('https\S+|[^ 0-9a-zA-Z]+','',str(x)))
data=data.drop_duplicates(subset=['description'])
tasks=data.description.tolist()
docs_titles=[] 
tasks=[[k.lower() for k in list(tokenize(i)) if k.lower() not in stop_words] for i in tasks]
docs = [
    [token for token in doc if token.lower() not in stop_words] for doc in tasks
]
doc=[]
for i in docs:
     for j in i:
           if j not in doc:
                 doc.append(j)
doc = [stemmer.stem(plural) for plural in doc]
words=' '.join(doc)
wc = WordCloud(
        background_color="white",
        stopwords=STOPWORDS,
        max_words=1000,
        max_font_size=90,
        random_state=42,
        contour_width=1,
        contour_color="#119DFF",
    )
wc.generate(words)

    # create wordcloud shape from image
fig = plt.figure(figsize=[8, 8])
ax = plt.imshow(wc.recolor(), interpolation="bilinear")

st.pyplot(fig)

from gensim.corpora import Dictionary
from gensim.models import LdaModel
from sklearn.manifold import TSNE
dictionary = Dictionary(docs)

# Filter out words that occur less than 20 documents, or more than 50% of the documents.
dictionary.filter_extremes(no_below=20, no_above=0.5)

# Bag-of-words representation of the documents.
corpus = [dictionary.doc2bow(doc) for doc in docs]


# ========== LDA - train our model with Gensim ==========

# Set training parameters.
num_topics = 6
chunksize = 2000
passes = 20
iterations = 400
eval_every = None  # Don't evaluate model perplexity, takes too much time.

# Make a index to word dictionary.
temp = dictionary[0]  # This is only to "load" the dictionary.
id2word = dictionary.id2token

lda = LdaModel(
    corpus=corpus,
    id2word=id2word,
    chunksize=chunksize,
    alpha="auto",
    eta="auto",
    iterations=iterations,
    num_topics=num_topics,
    passes=passes,
    eval_every=eval_every,
)

top_topics = lda.top_topics(corpus)  # , num_words=20)
lda_vals = list()
for d in corpus:
    topics_tup = lda.get_document_topics(
        d
    )  # This should be a N by K matrix where N = corpus size, K = 
    #print(topics_tup)
    temp_dict = {i: 0 for i in range(num_topics)}
    for t in topics_tup:
        temp_dict[t[0]] = t[1]
    lda_vals.append(temp_dict)
lda_df = pd.DataFrame(lda_vals)
lda_arr = lda_df.values
index=[i[0] for i in lda.print_topics(-1)]
lda_topics = {i[0]: i[1].split(" + ") for i in lda.print_topics(-1)}
topics_txt = [lda_topics[i] for i in range(num_topics)]
topics_txt = [[j.split("*")[1].replace('"', "") for j in i] for i in topics_txt]
topics_txt = ["; ".join(i) for i in topics_txt]
pds=pd.DataFrame(topics_txt,index=index)
pds=pds.style.set_caption('Top six topics')
st.write(pds)
lda_df = lda_df.assign(topic_id=[str(lda_arr[i].argmax()) for i in range(len(lda_arr))])
lda_df = lda_df.assign(
    topic_txt=[topics_txt[lda_arr[i].argmax()] for i in range(len(lda_arr))]
)
lda_df = lda_df.assign(
    topics=["Topic: " + str(lda_arr[i].argmax()) for i in range(len(lda_arr))]
)
docs_titles=data.name.tolist()
lda_df = lda_df.assign(title=docs_titles) 
#lda_df = lda_df.assign(filename=filenames)
tsne_embeds = TSNE(
        n_components=2,
        perplexity=10,
        n_iter=350,
        n_iter_without_progress=100,
        learning_rate=500,
        random_state=42,
    ).fit_transform(lda_arr)
lda_df = pd.concat([lda_df, pd.DataFrame(tsne_embeds, columns=["x", "y"])], axis=1)

    # Visualise the t-SNE topics
topic_ids = "Topic: " + lda_df["topic_id"].astype(str).values
fig = px.scatter(
        lda_df,
        title="t-SNE plot, perplexity: " + str(10),
        x="x",
        y="y",
        color=topic_ids,
        color_discrete_sequence=px.colors.qualitative.Light24,
        hover_name="title",
        hover_data=["topic_txt"],
        template="plotly_white",
    )
st.write(fig)

#st.write(data)