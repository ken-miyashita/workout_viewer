# -*- coding: utf-8 -*-
"""
download TCX data.

based on http://shima-nigoro.hatenablog.jp/entry/2016/07/17/160448
"""

import sys
import fitbit
import gather_keys_oauth2 as Oauth2

TCX_NAMESPACE = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
LOG_ID = '5268825224'

"""for OAuth2.0"""
USER_ID = '2285V4'
CLIENT_SECRET = '89222abf86ff863106886a2957f97e58'
 
"""for obtaining Access-token and Refresh-token"""
server = Oauth2.OAuth2Server(USER_ID, CLIENT_SECRET)
server.browser_authorize()
 
"""Authorization"""
auth2_client = fitbit.Fitbit(USER_ID, CLIENT_SECRET, oauth2=True, access_token=server.oauth.token['access_token'], refresh_token=server.oauth.token['refresh_token'])

"""Get activity logs list"""
alist = auth2_client.activity_logs_list(after_date='2016-12-21')
print(alist)

"""Getting data"""
fitbit_tcx = auth2_client.activity_tcx(log_id=LOG_ID)

for tp in fitbit_tcx.iter(TCX_NAMESPACE + 'Trackpoint'):
    time = tp.find(TCX_NAMESPACE + 'Time').text
    hr = tp.find(TCX_NAMESPACE + 'HeartRateBpm')
    hr_val = hr.find(TCX_NAMESPACE+'Value').text
    print(time, hr_val)
