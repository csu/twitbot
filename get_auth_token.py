import tweepy
import secrets

auth = tweepy.OAuthHandler(secrets.twitter['api_key'],
    secrets.twitter['api_secret'])

try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print 'Error! Failed to get request token.'
print redirect_url

verifier = raw_input('Verifier: ')

try:
    auth.get_access_token(verifier)
except tweepy.TweepError:
    print 'Error! Failed to get access token.'
print auth.access_token
print auth.access_token_secret