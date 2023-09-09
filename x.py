import pandas as pd
from sqlalchemy import create_engine
pdd=pd.read_csv('data.csv')
engine = create_engine("postgresql+psycopg2://postgres:Xw21872802?@localhost/wonders")
with engine.begin() as connection:
        pdd.to_sql('data', con=connection, if_exists='append')