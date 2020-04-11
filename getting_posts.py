import requests
import pandas as pd
from datetime import datetime
import numpy as np

url = "https://reddit.com/r/programming/.json?limit=100"

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:66.0) Gecko/20100101 Firefox/66.0"}
REDDIT_ROOT_URL = "https://reddit.com"

def get_with_headers(url):
    return requests.get(url, headers=headers)


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

posts = get_subreddit_posts(url)
df_posts = pd.DataFrame(posts)
last_value= df_posts.name[99]


url= "{}&after={}".format(url,last_value)

posts= get_subreddit_posts(url)
df_posts_2 = pd.DataFrame(posts)
last_value= df_posts_2.name[99]


url = "{}&after={}".format(url,last_value)

posts = get_subreddit_posts(url)
df_posts_3 = pd.DataFrame(posts)
last_value= df_posts_3.name[99]


url = "{}&after={}".format(url,last_value)

posts = get_subreddit_posts(url)
df_posts_4 = pd.DataFrame(posts)
last_value= df_posts_4.name[99]


url = "{}&after={}".format(url,last_value)

posts = get_subreddit_posts(url)
df_posts_5 = pd.DataFrame(posts)
last_value= df_posts_5.name[99]


url = "{}&after={}".format(url,last_value)

posts = get_subreddit_posts(url)
df_posts_6 = pd.DataFrame(posts)
last_value= df_posts_6.name[99]


url = "{}&after={}".format(url,last_value)

posts = get_subreddit_posts(url)
df_posts_7 = pd.DataFrame(posts)
last_value= df_posts_7.name[99]


url = "{}&after={}".format(url,last_value)

posts = get_subreddit_posts(url)
df_posts_8 = pd.DataFrame(posts)
last_value= df_posts_8.name[99]


url = "{}&after={}".format(url,last_value)

posts = get_subreddit_posts(url)
df_posts_9 = pd.DataFrame(posts)


all_posts = pd.concat([df_posts,df_posts_2,df_posts_3,df_posts_4,df_posts_5,df_posts_6,df_posts_7,df_posts_8,df_posts_9])
all_posts["created_utc"] = all_posts["created_utc"].apply(datetime.fromtimestamp)
all_posts.rename(columns={'created_utc':'date_hour'},inplace=True)
all_posts['date'] = [d.date() for d in all_posts['date_hour']]
all_posts['time'] = [d.time() for d in all_posts['date_hour']]

all_posts.to_csv('reddit_posts.csv')