import tweepy

def fetch_twitter_data(kol_handle):
    # Set up Tweepy API (assuming you have your credentials)
    auth = tweepy.OAuthHandler('consumer_key', 'consumer_secret')
    auth.set_access_token('access_token', 'access_token_secret')
    api = tweepy.API(auth)
    
    # Fetch tweets
    tweets = api.user_timeline(screen_name=kol_handle, count=10)
    return tweets 