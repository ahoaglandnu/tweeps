import tweepy
import time
import datetime
import pandas as pd   

# Fill in your info
access_token = ' '
access_token_secret = ' '
consumer_key = ' '
consumer_secret = ' '

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# This will show you if you are hit with a rate status limit
data = api.rate_limit_status()
print(data['resources']['followers']['/followers/ids'])
print(data['resources']['friends']['/friends/ids'])

# modification from the Tweepy documentation on Cursor
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            # Twitter default is 15 minutes so feel free to change 
            print('Hit rate limit. Paused for 16 minutes.') 
            print(datetime.datetime.now())
            data = api.rate_limit_status()
            # These do not work against your rate limit. Returns in unix time
            print(data['resources']['followers']['/followers/ids'])
            print(data['resources']['friends']['/friends/ids'])
            time.sleep(16 * 60)
            data = api.rate_limit_status()
            print(data['resources']['followers']['/followers/ids'])
            print(data['resources']['friends']['/friends/ids'])
            print("Resuming")

# REMEMBER to fill this in
tweeps = ['','',''] 

# This will assemble your friends_ids into a column per tweep
df = pd.DataFrame(columns=tweeps)
for tweep in tweeps:
    print('Starting',tweep)
    # this is using the helper function above for if/when you hit a rate limit
    for friend in limit_handled(tweepy.Cursor(api.friends_ids, id=tweep).items()):
        df = df.append({tweep: friend}, ignore_index=True)
    print(tweep, "complete.")

# saves to csv in your current working directory
df.to_csv('tweeps_friends.csv', index=False)

# same as above but for followers. This will likely take longer.
df2 = pd.DataFrame(columns=tweeps)
for tweep in tweeps:
    print('Starting',tweep)
    for follow in limit_handled(tweepy.Cursor(api.followers_ids, id=tweep).items()):
        df2 = df2.append({tweep: follow}, ignore_index=True)
    print(tweep, "complete.")

# saves to csv in your current working directory
df2.to_csv('tweeps_follow.csv', index=False)
