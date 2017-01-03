# -*- coding: utf-8 -*-
"""
download TCX data.

based on http://shima-nigoro.hatenablog.jp/entry/2016/07/17/160448
"""

import fitbit
import gather_keys_oauth2 as Oauth2

TCX_NAMESPACE = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'
LOG_ID = '5268825224'

"""for OAuth2.0"""
USER_ID = '2285V4'
CLIENT_SECRET = '89222abf86ff863106886a2957f97e58'
 

"""Getting data"""
def get_tcx_data(auth2_client):
    fitbit_tcx = auth2_client.activity_tcx(log_id=LOG_ID)

    for tp in fitbit_tcx.iter(TCX_NAMESPACE + 'Trackpoint'):
        time = tp.find(TCX_NAMESPACE + 'Time').text
        hr = tp.find(TCX_NAMESPACE + 'HeartRateBpm')
        hr_val = hr.find(TCX_NAMESPACE+'Value').text
        print(time, hr_val)

def enumerate_activity_logs(auth2_client, log_type, from_date, to_date):
    """
    enumerate activity logs with a certain log type.
    note this function works as a 'generator' which you can use in
    enumeration loop.
    
    Parameters
    ----------
    auth2_client : fitbit.Fitbit
        web API client object
    log_type : str
        log type such as 'mobile_run'.
        See https://dev.fitbit.com/docs/activity/#get-activity-logs-list
        for more details.
    from_date : str
        The beginning date in the format yyyy-MM-ddTHH:mm:ss. 
        Only yyyy-MM-dd is required.
    to_date : str
        The ending date in the format yyyy-MM-ddTHH:mm:ss. 
        Only yyyy-MM-dd is required.
    
    Return (yield)
    --------------
    act : 'Activity' map object
        map object which contains an Activity data.
        See https://dev.fitbit.com/docs/activity/#get-activity-logs-list
        for more details.
    """
    response = auth2_client.activity_logs_list(after_date=from_date)
    enumerating = True
    while enumerating:
        for act in response['activities']:
            if act['startTime'] > to_date:
                enumerating = False
                break
            if act['logType'] == log_type:
                yield act
        if enumerating:
            next_request = response['pagination']['next']
            response = auth2_client.make_request(next_request)


"""for obtaining Access-token and Refresh-token"""
server = Oauth2.OAuth2Server(USER_ID, CLIENT_SECRET)
server.browser_authorize()
 
"""Authorization"""
auth2_client = fitbit.Fitbit(USER_ID, CLIENT_SECRET, oauth2=True, access_token=server.oauth.token['access_token'], refresh_token=server.oauth.token['refresh_token'])

for run in enumerate_activity_logs(auth2_client, 'mobile_run', '2016-12-01', '2017-01-01'):
    print(run['startTime'])
