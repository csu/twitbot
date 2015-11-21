import tweepy

from modularity import modularity

class Twitbot(object):
    class StreamListener(tweepy.StreamListener):
        def on_status(self, status):
            pass

    def __init__(self, api_key, api_secret, auth_token, auth_secret):
        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(auth_token, auth_secret)
        self.api = tweepy.API(auth)

        stream_listener = StreamListener()
        stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
        stream.userstream(_with='user', replies='all')