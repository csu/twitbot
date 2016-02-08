import tweepy
from ttp import ttp
from modularity import modularity

import secrets

parser = ttp.Parser()

def parse_tweet(parser, tweet_from, tweet_text):
  query = tweet_text[tweet_text.index('@%s' % secrets.bot_username) + len('@%s' % secrets.bot_username) + 1:]

  result = parser.parse(tweet_text)
  mentions = result.users + [tweet_from]
  while secrets.bot_username in mentions:
    mentions.remove(secrets.bot_username)
  tagged_hashtags = result.tags
  tagged_urls = result.urls

  for user in mentions:
    query = query.replace('@%s' % user, '')
  for tag in tagged_hashtags:
    query = query.replace('#%s' % tag, '')
  for url in tagged_urls:
    query = query.replace('%s' % url, '')

  if query:
    try:
      return mentions, query.strip()  
    except:
      return None, None
  
  return None, None

class Twitbot(object):
  class TwitbotStreamListener(tweepy.StreamListener):
    listener_modules = []

    def set_modules(self, listener_modules):
      self.listener_modules = listener_modules

    def set_api(self, api):
      self.api = api

    def on_status(self, status):
      try:
        tweet_from = status.user.screen_name

        if (tweet_from != secrets.bot_username and
          tweet_from not in secrets.blacklist and
          not hasattr(status, 'retweeted_status')):

          tweet_id = status.id
          tweet_text = status.text
          mentions, tweet_text = parse_tweet(parser, tweet_from, tweet_text)

          if mentions:
            mentions = ['@%s' % x for x in mentions]
          
          if tweet_text:
            for mod in self.listener_modules:
              m = getattr(mod, 'process_tweet')
              result = m(tweet_id, tweet_text, mentions, self.api)
      except:
        return None

  def __init__(self, api_key, api_secret, auth_token, auth_secret, modules=[]):
    # Set up Tweepy
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(auth_token, auth_secret)
    api = tweepy.API(auth)

    # Set up stream listener
    stream_listener = self.TwitbotStreamListener()
    stream_listener.set_modules(modules)
    stream_listener.set_api(api)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    try:
      stream.userstream(_with='user', replies='all')
    except:
      pass

if __name__ == "__main__":
  bot = Twitbot(secrets.twitter['api_key'],
        secrets.twitter['api_secret'],
        secrets.twitter['auth_token'],
        secrets.twitter['auth_secret'],
        modules=modularity.get_imported('modules'))