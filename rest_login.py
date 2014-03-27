import requests
import json
from requests.auth import HTTPBasicAuth

my_auth = HTTPBasicAuth('jarvis', 'leftzhang')
# auth_url = 'http://localhost:8080/rest/auth/1/session'
# headers = {'content-type': 'application/json'}
# auth_response = requests.get(auth_url, auth = my_auth)
# print auth_response.text


rapidview_url = 'http://localhost:8080/rest/greenhopper/1.0/rapidview'
rapidview_response = requests.get(rapidview_url, auth = my_auth)
print rapidview_response.text