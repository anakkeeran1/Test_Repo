# This sample source code is offered only as an example of what can or might be built using the IICS Github APIs, 
# and is provided for educational purposes only. This source code is provided "as-is" 
# and without representations or warrantees of any kind, is not supported by Informatica.
# Users of this sample code in whole or in part or any extraction or derivative of it 
# assume all the risks attendant thereto, and Informatica disclaims any/all liabilities 
# arising from any such use to the fullest extent permitted by law.

import requests
import os
import json
import time
import sys

URL = os.environ['IICS_POD_URL']
SESSION_ID = os.environ['sessionId']
COMMIT_HASH = os.environ['COMMIT_HASH']

HEADERS = {"Content-Type": "application/json; charset=utf-8", "INFA-SESSION-ID": SESSION_ID }
HEADERS_V2 = {"Content-Type": "application/json; charset=utf-8", "icSessionId": SESSION_ID }

print('Getting all objects for the commit: ' + COMMIT_HASH)
# Get all the objects for commit
r = requests.get(URL + "/public/core/v3/commit/" + COMMIT_HASH, headers = HEADERS)

if r.status_code != 200:
    print("Exception caught: " + r.text)
    sys.exit(99)
    
request_json = r.json()

# Only get Mapping Tasks
r_filtered = [x for x in request_json['changes'] if ( x['type'] == 'MTT') ]

# This loop runs tests for each one of the mapping tasks
for x in r_filtered:
    BODY = {"@type": "job","taskId": x['appContextId'],"taskType": "MTT"}
    t = requests.post(URL + "/api/v2/job/", headers = HEADERS_V2, json = BODY )

    if t.status_code != 200:
        print("Exception caught: " + t.text)
        sys.exit(99)

    test_json = t.json()
    PARAMS = "?runId=" + str(test_json['runId'])
    #"?taskId=" + test_json['taskId']

    STATE=0
    
    while STATE == 0:
        time.sleep(60)
        a = requests.get(URL + "/api/v2/activity/activityLog" + PARAMS, headers = HEADERS_V2)
        
        activity_log = a.json()

        STATE = activity_log[0]['state']

    if STATE != 1:
        print("Mapping task: " + activity_log[0]['objectName'] + " failed. ")
        sys.exit(99)
    else:
        print("Mapping task: " + activity_log[0]['objectName'] + " completed successfully. ")

requests.post(URL + "/public/core/v3/logout", headers = HEADERS)