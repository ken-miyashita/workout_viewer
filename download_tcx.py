# -*- coding: utf-8 -*-
"""
download TCX data.

based on http://shima-nigoro.hatenablog.jp/entry/2016/07/17/160448
"""

import sys
import fitbit
import gather_keys_oauth2 as Oauth2

LOG_ID = '5268825224'

"""for OAuth2.0"""
USER_ID = '2285V4'
CLIENT_SECRET = '89222abf86ff863106886a2957f97e58'
 
"""for obtaining Access-token and Refresh-token"""
server = Oauth2.OAuth2Server(USER_ID, CLIENT_SECRET)
server.browser_authorize()
 
"""Authorization"""
auth2_client = fitbit.Fitbit(USER_ID, CLIENT_SECRET, oauth2=True, access_token=server.oauth.token['access_token'], refresh_token=server.oauth.token['refresh_token'])
 
"""Getting data"""
fitbit_tcx = auth2_client.activity_tcx(log_id=LOG_ID)
print(fitbit_tcx)
