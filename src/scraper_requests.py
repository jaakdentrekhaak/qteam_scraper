import os
import requests
import urllib
import json


session = requests.session()

login_url = 'http://bonew.qteam.be/PlatformServices/service/app/logon.object'
file_dir = os.path.dirname(os.path.realpath(__file__))
with open(f'{file_dir}/config.json') as config:
        data = json.load(config)
        username = data['qteam']['username']
        password = data['qteam']['password']
login_payload = {
	"qryStr": "",
	"cmsVisible": "false",
	"cms": "SRV-BO:6400",
	"authenticationVisible": "false",
	"authType": "secEnterprise",
	"isFromLogonPage": "true",
	"appName": "SAP+BusinessObjects+InfoView",
	"prodName": "BusinessObjects",
	"sessionCookie": "true",
	"backUrl": "/listing/main.do",
	"backUrlParents": "1",
	"backContext": "/InfoViewApp",
	"persistCookies": "true",
	"useLogonToken": "true",
	"service": "/InfoViewApp/common/appService.do",
	"appKind": "InfoView",
	"loc": "en",
	"reportedIP": "",
	"reportedHostName": "bonew.qteam.be",
	"username": username,
	"password": password
}

file_url = 'http://bonew.qteam.be/AnalyticalReporting/viewers/cdz_adv/downloadPDForXLS.jsp?iViewerID=1&sEntry=we0002000099ef567a6ad0&iReport=0&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&iFoldPanel=0&doctype=wid&viewType=O&saveReport=N'

session.post(login_url, data=login_payload)

def replace_url_encoding(element):
    return (element[0], urllib.parse.unquote(element[1]))

cookie_dict = session.cookies.get_dict()

cookie_dict = dict(map(replace_url_encoding, cookie_dict.items()))

response = session.get(file_url, cookies=cookie_dict)

# Problem: cookies don't work

# How it works in terminal:
# (cookies copied from request on website itself)
# (values removed for pushing to Github)
# The only necessary cookie is the JSESSIONID! (found through testing)
"""
>>> import requests
>>> file_url = 'http://bonew.qteam.be/AnalyticalReporting/viewers/cdz_adv/downloadPDForXLS.jsp?iViewerID=1&sEntry=we00020000aad681e98955&iReport=0&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&iFoldPanel=0&doctype=wid&viewType=O&saveReport=N'
>>> cookies = {
...     "JSESSIONID": ""
... }
>>> 
>>> response = requests.get(file_url, cookies=cookies)
>>> response.status_code
200
"""

# The problem probably is that the JSESSIONID received at login is not the sid needed to ask for the file
# Strange thing is that you don't get sid at login in response and you send a sid in the first login post