# To be integrated in with the langchain portion of this app. The vision is to present the researcher with
# a list of tweets from the person in question, and have them manually select whether or not that tweet
# indicates that the person is Jewish or not.

# e.g. The workflow could look as follows.
# 1. Get the list of individuals to research (as of now, manually)
# 2. Use langchain to perform the research on Google searches
# 3. Have an optional flag to search tweets. If enabled, then after the google searches, the tool will attempt to find
#       this individual on twitter. It will ask the user to verify it is the correct person. If after a few guesses, the 
#       tool is unable to find the correct person, it will ask the user to manually search for the person on twitter, and
#       then paste the link to the correct twitter profile.


import tweepy
import configparser

api_config = configparser.ConfigParser()
api_config.read_file(open('apidata.config'))
 
api_key = api_config['TWITTER']['API_KEY']
api_secrets = api_config['TWITTER']['API_SECRETS']
access_token = api_config['TWITTER']['ACCESS_TOKEN']
access_secret = api_config['TWITTER']['ACCESS_SECRET']
 
# Authenticate to Twitter
auth = tweepy.OAuthHandler(api_key,api_secrets)
auth.set_access_token(access_token,access_secret)
 
api = tweepy.API(auth)
 
try:
    api.verify_credentials()
    print('Successful Authentication')
except:
    print('Failed authentication')


user = api.get_user(screen_name="libbyemmons") # Store user as a variable
 
# # Get user Twitter statistics
# print(f"user.followers_count: {user.followers_count}")
# print(f"user.listed_count: {user.listed_count}")
# print(f"user.statuses_count: {user.statuses_count}")
 
# # Show followers
# for follower in user.followers():
#     print('Name: ' + str(follower.name))
#     print('Username: ' + str(follower.screen_name))
 
# # Get tweets from a user tmeline
# tweets = api.user_timeline(id='libbyemmons', count=5)
# tweets_extended = api.user_timeline(id='libbyemmons', tweet_mode='extended', count=5)
# print(tweets_extended)
