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

# PROBLEM:
# file_url is DYNAMIC:
# http://bonew.qteam.be/AnalyticalReporting/viewers/cdz_adv/downloadPDForXLS.jsp?iViewerID=1&sEntry=we0002000099ef567a6ad0&iReport=0&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&iFoldPanel=0&doctype=wid&viewType=O&saveReport=N
# http://bonew.qteam.be/AnalyticalReporting/viewers/cdz_adv/downloadPDForXLS.jsp?iViewerID=1&sEntry=we00020000aad681e98955&iReport=0&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&iFoldPanel=0&doctype=wid&viewType=O&saveReport=N
# sEntry is different for the links
# NOTE: it works if you use the link with the correct sEntry

# The sEntry for the file_url can be found in the HTML response of processPrompts.jsp -> pp.Report.location (current sEntry for processPrompts: we0001000062b63ba9577b)
# The new problem is that processPrompts needs an sEntry itself
# The sEntry for processPrompts can be found in refreshDocument.jsp HTML response -> strEntry (current sEntry for refreshDocument: we0000000097e61511dfbe)
# The new problem is that refreshDocument.jsp needs an sEntry itself
# (The sEntry for refreshDocument is also needed in viewReport.jsp)
# (The sEntry for refreshDocument is also needed in report.jsp)
# The sEntry for refreshDocument can be found in viewDocument.jsp HTML response -> strEntry (current sEntry for refreshDocument: we0000000097e61511dfbe)
# Hopefully the id needed in the link of viewDocument.jsp is static (same id as used in WebiView.do, retrieved from ajaxRequest json)
