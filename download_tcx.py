# -*- coding: utf-8 -*-
"""
download TCX data.

based on http://shima-nigoro.hatenablog.jp/entry/2016/07/17/160448
"""
import numpy as np
import pandas as pd
import fitbit
import gather_keys_oauth2 as Oauth2

TCX_NAMESPACE = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}'

# 2016/12/21T07:38:00+9:00 running
# https://www.fitbit.com/activities/exercise/5257513042
LOG_ID = '5257513042'

# for OAuth2.0
USER_ID = '2285V4'
CLIENT_SECRET = '89222abf86ff863106886a2957f97e58'

def get_activity_tcx(auth2_client, log_id):
    """
    get TCX data with log_id.

    Parameters
    ----------
    auth2_client : fitbit.Fitbit
        web API client object
    log_id : str
        Activity log ID.

    Return
    ------
    df : pandas.DataFrame
        data frame containing the Activity.
    """
    fitbit_tcx = auth2_client.activity_tcx(log_id=log_id)
    # convert XML elements into DataFrame
    rows = []
    for tp in fitbit_tcx.iter(TCX_NAMESPACE + 'Trackpoint'):
        time_text = tp.find(TCX_NAMESPACE + 'Time').text
        time = pd.to_datetime(time_text, utc=True)
        hr_body = tp.find(TCX_NAMESPACE + 'HeartRateBpm')
        hr_text = hr_body.find(TCX_NAMESPACE+'Value').text
        hr = float(hr_text)
        dist_text = tp.find(TCX_NAMESPACE + 'DistanceMeters').text
        dist = float(dist_text)
        rows.append((time, [dist, hr]))
    df = pd.DataFrame.from_items(rows, orient='index',
                                 columns=['distance_meters', 'heartrate_bpm'])
    return df

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
        The beginning date in local time in the format yyyy-MM-ddTHH:mm:ss.
        Only yyyy-MM-dd is required.
    to_date : str
        The ending date in local time in the format yyyy-MM-ddTHH:mm:ss.
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

"""
main
"""
# for obtaining Access-token and Refresh-token
server = Oauth2.OAuth2Server(USER_ID, CLIENT_SECRET)
server.browser_authorize()

# Authorization
auth2_client = fitbit.Fitbit(USER_ID, CLIENT_SECRET, oauth2=True, access_token=server.oauth.token['access_token'], refresh_token=server.oauth.token['refresh_token'])

# enumerate run logs.
for run in enumerate_activity_logs(auth2_client, 'mobile_run', '2016-12-01', '2017-01-01'):
    print(run['startTime'])

# get TCX data and plot it.
df = get_activity_tcx(auth2_client, LOG_ID)

# replace index with elapsed seconds.
df.index = (df.index - df.index[0]) / pd.Timedelta(1, unit='s')
df.plot(subplots=True, sharex=True)


