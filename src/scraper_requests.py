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

# Set extra cookies (probably not necessary)
session.cookies.set("infoview_css", "\"default.css\"")
session.cookies.set("infoview_prefs", "\"view=0&dv4=1&defaultnav=folder&dv2=1&dv1=1&dv0=1&rpp=10\"")
session.cookies.set("infoview_userLocale", "\"userDefaultLocale\"")
session.cookies.set("infoview_userPreference", "\"maxOpageU=10;maxOpageUt=200;maxOpageC=10;tz=Europe/Paris;mUnit=inch;showFilters=true;smtpFrom=true;promptForUnsavedData=true;\"")
session.cookies.set("infoview_userTimeZone", "\"Europe/Paris\"")

def replace_url_encoding(element):
    return (element[0], urllib.parse.unquote(element[1]))

cookie_dict = session.cookies.get_dict()

cookie_dict = dict(map(replace_url_encoding, cookie_dict.items()))

response = session.get(file_url, cookies=cookie_dict)

# Problem: cookies don't work

# How it works in terminal:
# (some values removed for pushing to Github)
"""
>>> import requests
>>> file_url = 'http://bonew.qteam.be/AnalyticalReporting/viewers/cdz_adv/downloadPDForXLS.jsp?iViewerID=1&sEntry=we00020000aad681e98955&iReport=0&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&iFoldPanel=0&doctype=wid&viewType=O&saveReport=N'
>>> cookies = { # Copied from real request on website
...     "infoview_css": "\"default.css\"",
...     "infoview_prefs": "\"view=0&dv4=1&defaultnav=folder&dv2=1&dv1=1&dv0=1&rpp=10\"",
...     "infoview_userLocale": "\"userDefaultLocale\"",
...     "infoview_userPreference": "\"maxOpageU=10;maxOpageUt=200;maxOpageC=10;tz=Europe/Paris;mUnit=inch;showFilters=true;smtpFrom=true;promptForUnsavedData=true;\"",
...     "infoview_userTimeZone": "\"Europe/Paris\"",
...     "InfoViewPLATFORMSVC_COOKIE_AUTH": "",
...     "InfoViewPLATFORMSVC_COOKIE_CMS": "",
...     "InfoViewPLATFORMSVC_COOKIE_TOKEN": "",
...     "InfoViewPLATFORMSVC_COOKIE_USR": "",
...     "InfoViewses": "",
...     "ivsEntSessionVar": "\"\"",
...     "ivsExitPage": "\"\"",
...     "JSESSIONID": ""
... }
>>> 
>>> response = requests.get(file_url, cookies=cookies)
>>> response.status_code
200
"""