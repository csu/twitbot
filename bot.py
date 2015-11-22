import tweepy

from modularity import modularity

class Twitbot(object):
    class TwitbotStreamListener(tweepy.StreamListener):
        listener_modules = []

        def set_modules(self, listener_modules):
            self.listener_modules = listener_modules

        def on_status(self, status):
            pass

    def __init__(self, api_key, api_secret, auth_token, auth_secret):
        # Set up Tweepy
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(auth_token, auth_secret)
        self.api = tweepy.API(auth)

        # Set up stream listener
        stream_listener = TwitbotStreamListener()
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        stream.userstream(_with='user', replies='all')