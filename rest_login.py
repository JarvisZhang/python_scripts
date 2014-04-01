import requests
import json
from requests.auth import HTTPBasicAuth
# from requests_kerberos import HTTPKerberosAuth

# my_auth = HTTPBasicAuth('jarvis', 'leftzhang')
# auth_url = 'http://localhost:8080/rest/auth/1/session'
# headers = {'content-type': 'application/json'}
# auth_response = requests.get(auth_url, auth = my_auth)
# print auth_response.text

online_auth = HTTPBasicAuth('zuzhang', 'Left1991=')
rapidview_url = 'http://projects.engineering.redhat.com/rest/greenhopper/1.0/rapidview'
rapidview_response = requests.get(rapidview_url, auth = online_auth, verify = False)
print rapidview_response.text

# online_url = 'http://projects.engineering.redhat.com/rest/greenhopper/1.0/rapidview'
# rapidview_response = requests.get(online_url, auth = my_auth)
# print rapidview_response.text