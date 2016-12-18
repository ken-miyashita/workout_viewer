# -*- coding: utf-8 -*-
"""
This file is a copy of:
http://shima-nigoro.hatenablog.jp/entry/2016/07/17/160448

Modified a little to set parameters.
"""

import sys
import fitbit
import gather_keys_oauth2 as Oauth2

#if (len(sys.argv) < 2):
#    print 'Usage: # python %s YYYY-MM-DD' % sys.argv[0]
#    quit()

"""for Save file."""
BASE_DATE = '2016-12-14'
OUTPUT_FILE = "HR_%s.csv" % BASE_DATE

"""for OAuth2.0"""
USER_ID = '2285V4'
CLIENT_SECRET = '89222abf86ff863106886a2957f97e58'
 
"""for obtaining Access-token and Refresh-token"""
server = Oauth2.OAuth2Server(USER_ID, CLIENT_SECRET)
server.browser_authorize()
 
"""Authorization"""
auth2_client = fitbit.Fitbit(USER_ID, CLIENT_SECRET, oauth2=True, access_token=server.oauth.token['access_token'], refresh_token=server.oauth.token['refresh_token'])
 
"""Getting data"""
fitbit_stats = auth2_client.intraday_time_series('activities/heart', BASE_DATE, detail_level='1min')
 
"""Getting only 'heartrate' and 'time'"""
stats = fitbit_stats['activities-heart-intraday']['dataset']
 
"""Timeseries data of Heartrate"""
csv_file = open(OUTPUT_FILE, 'w')
for var in range(0, len(stats)):
    csv_file.write(stats[var]['time'])
    csv_file.write(",")
    csv_file.write(str(stats[var]['value']))
    csv_file.write("\n")
csv_file.close()