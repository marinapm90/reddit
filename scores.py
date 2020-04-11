import requests
import pandas as pd
from datetime import datetime
import numpy as np

all_posts = pd.read_csv('./reddit_posts.csv')

all_posts_score = all_posts[['date', 'score','weekday']].copy()

unique = all_posts_score.date.unique().tolist()
unique_df = pd.DataFrame(unique,columns =['date'])
unique_df['weekday'] = [d.weekday() for d in unique_df['date']]
repeated = unique_df.weekday.value_counts()
repeated = repeated.to_dict()


repeated_df = pd.DataFrame.from_dict(repeated, orient='index')
score_per_day = all_posts_score.groupby(by='weekday').agg({'score':['sum']})


posts_per_day = all_posts_score.weekday.value_counts().to_frame()


result = pd.concat([posts_per_day, repeated_df,score_per_day], axis=1, sort=False)
result.rename(columns ={0:'repeated_weekday'},inplace=True)


result['posts_per_day']= result.weekday/result.repeated_weekday
result['score_per_day']= result['score', 'sum']/result.repeated_weekday
result = result.sort_values(['posts_per_day'], ascending = False)
result.reset_index(inplace=True)


result['index'] = result['index'].replace(0,'Monday').replace(1,'Tuesday').replace(2,'Wednesday').replace(3,'Thursday').replace(4,'Friday').replace(5,'Saturday').replace(6,'Sunday')
result.rename = result.rename(columns = {'index':'day'}, inplace = True)


result.drop(['weekday', 'repeated_weekday', ('score', 'sum')], axis=1,inplace=True)


result = result.sort_values(['score_per_day'], ascending = False)
print(result)

