#!/usr/bin/env python
import sys
import gdc_settings as config
from twython import Twython

tweetStr = "Yay!  Tweet from GDO."

# your twitter consumer and access information goes here
# note: these are garbage strings and won't work

api = Twython(config.apiKey,config.apiSecret,config.accessToken,config.accessTokenSecret)

api.update_status(status=tweetStr)

print "Tweeted: " + tweetStr

