import requests
import pandas as pd
from datetime import datetime
import numpy as np
from functools import lru_cache

url = "https://reddit.com/r/programming/.json?limit=100"

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:66.0) Gecko/20100101 Firefox/66.0"}
REDDIT_ROOT_URL = "https://reddit.com"

def get_with_headers(url):
    return requests.get(url, headers=headers)

@lru_cache(maxsize=32)
def get_subreddit_posts(subreddit_url):
    print(f"Getting posts from {url}...")
    response = get_with_headers(url)
    raw_posts = response.json()['data']['children']

    posts = []
    for raw_post in raw_posts:
        post = {}
        raw_post = raw_post['data']
        post['name'] = raw_post['name']
        post['title'] = raw_post['title']
        post['score'] = raw_post['score']
        post['url'] = REDDIT_ROOT_URL + raw_post['permalink']
        post['created_utc'] = raw_post['created_utc']
        post['num_comments'] = raw_post['num_comments']
        
        posts.append(post)

    return posts


# Getting the first 100 posts.

posts = get_subreddit_posts(url)
df_posts = pd.DataFrame(posts)
last_value= df_posts.name[99]


url= "{}&after={}".format(url,last_value)

# Getting the following 100 posts.

posts= get_subreddit_posts(url)
df_posts_2 = pd.DataFrame(posts)
last_value= df_posts_2.name[99]


url = "{}&after={}".format(url,last_value)


# Getting the following 100 posts.

posts = get_subreddit_posts(url)
df_posts_3 = pd.DataFrame(posts)
last_value= df_posts_3.name[99]


url = "{}&after={}".format(url,last_value)

# Getting the following 100 posts.

posts = get_subreddit_posts(url)
df_posts_4 = pd.DataFrame(posts)
last_value= df_posts_4.name[99]


url = "{}&after={}".format(url,last_value)


# Getting the following 100 posts.

posts = get_subreddit_posts(url)
df_posts_5 = pd.DataFrame(posts)
last_value= df_posts_5.name[99]


url = "{}&after={}".format(url,last_value)

# Getting the following 100 posts.

posts = get_subreddit_posts(url)
df_posts_6 = pd.DataFrame(posts)
last_value= df_posts_6.name[99]


url = "{}&after={}".format(url,last_value)

# Getting the following 100 posts.

posts = get_subreddit_posts(url)
df_posts_7 = pd.DataFrame(posts)
last_value= df_posts_7.name[99]


url = "{}&after={}".format(url,last_value)

# Getting the following 100 posts.

posts = get_subreddit_posts(url)
df_posts_8 = pd.DataFrame(posts)
last_value= df_posts_8.name[99]


url = "{}&after={}".format(url,last_value)

# Getting the last 100 posts.

posts = get_subreddit_posts(url)
df_posts_9 = pd.DataFrame(posts)

# Concatenate all the datasets into one.

all_posts = pd.concat([df_posts,df_posts_2,df_posts_3,df_posts_4,df_posts_5,df_posts_6,df_posts_7,df_posts_8,df_posts_9])

# Changing date time from utc to something readable.

all_posts["created_utc"] = all_posts["created_utc"].apply(datetime.fromtimestamp)
all_posts.rename(columns={'created_utc':'date_hour'},inplace=True)

# Splitting the column into date and time.

all_posts['date'] = [d.date() for d in all_posts['date_hour']]
all_posts['time'] = [d.time() for d in all_posts['date_hour']]

# Adding weekday.

all_posts['weekday'] = [d.weekday() for d in all_posts['date']]


# Creating a copy with only the important columns.

all_posts_score = all_posts[['date', 'score','weekday']].copy()

# Some weekdays are repeated several times.

unique = all_posts_score.date.unique().tolist()
unique_df = pd.DataFrame(unique,columns =['date'])
unique_df['weekday'] = [d.weekday() for d in unique_df['date']]
repeated = unique_df.weekday.value_counts()
repeated = repeated.to_dict()

# Creating a data frame with the number of times a weekday is repeated.

repeated_df = pd.DataFrame.from_dict(repeated, orient='index')

# Creating a data frame with the sum of total score per weekday.

score_per_day = all_posts_score.groupby(by='weekday').agg({'score':['sum']})
posts_per_day = all_posts_score.weekday.value_counts().to_frame()

# Concatenate both data frames into one.

result = pd.concat([posts_per_day, repeated_df,score_per_day], axis=1, sort=False)
result.rename(columns ={0:'repeated_weekday'},inplace=True)


# Divide the columns "weekday" and "score" by "repeated_weekday" to have the number of posts and the score per day.

result['posts_per_day']= result.weekday/result.repeated_weekday
result['score_per_day']= result['score', 'sum']/result.repeated_weekday
result = result.sort_values(['posts_per_day'], ascending = False)
result.reset_index(inplace=True)

# Replacing numbers per days.

result['index'] = result['index'].replace(0,'Monday').replace(1,'Tuesday').replace(2,'Wednesday').replace(3,'Thursday').replace(4,'Friday').replace(5,'Saturday').replace(6,'Sunday')
result.rename = result.rename(columns = {'index':'day'}, inplace = True)


# Dropping useless columns.

result.drop(['weekday', 'repeated_weekday', ('score', 'sum')], axis=1,inplace=True)


result_score = result.sort_values(['score_per_day'], ascending = False)
result_score.reset_index(inplace=True)
print("===========================================================")
print(result)
print("===========================================================")
print(result.day[0] + " is the day that most posts are published.")
highest_score = result_score.day[0]
print("Posts publised on {} are those with highest scores.".format(highest_score))