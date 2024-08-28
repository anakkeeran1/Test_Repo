import requests
import os

# This sample source code is offered only as an example of what can or might be built using the IICS Github APIs, 
# and is provided for educational purposes only. This source code is provided "as-is" 
# and without representations or warrantees of any kind, is not supported by Informatica.
# Users of this sample code in whole or in part or any extraction or derivative of it 
# assume all the risks attendant thereto, and Informatica disclaims any/all liabilities 
# arising from any such use to the fullest extent permitted by law.

URL = os.environ['IICS_LOGIN_URL']
USERNAME = os.environ['IICS_USERNAME']
PASSWORD = os.environ['IICS_PASSWORD']

UAT_USERNAME = os.environ['UAT_IICS_USERNAME']
UAT_PASSWORD = os.environ['UAT_IICS_PASSWORD']

URL = "https://dm-us.informaticacloud.com/saas/public/core/v3/login"
BODY = {"username": USERNAME,"password": PASSWORD}

r = requests.post(url = URL, json = BODY)

if r.status_code != 200:
    print("Caught exception: " + r.text)

UAT_BODY = BODY = {"username": UAT_USERNAME,"password": UAT_PASSWORD}

u = requests.post(url = URL, json = BODY)

if u.status_code != 200:
    print("Caught exception: " + r.text)

# extracting data in json format
data = r.json()
uat_data = u.json()

# Set session tokens to the environment
env_file = os.getenv('GITHUB_ENV')

with open(env_file, "a") as myfile:
    myfile.write("sessionId=" + data['userInfo']['sessionId'] + "\n")
    myfile.write("uat_sessionId=" + uat_data['userInfo']['sessionId'] + "\n")