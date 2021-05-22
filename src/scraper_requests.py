###
# Download Excel file by sending HTTP requests
###

import os
import requests
import json

def login(session):
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
	session.post(login_url, data=login_payload)

def download_cookie(session):
	# Get new cookie (used for downloading)
	webiview_url = 'http://bonew.qteam.be/AnalyticalReporting/WebiView.do?bypassLatestInstance=true&cafWebSesInit=true&appKind=InfoView&service=/InfoViewApp/common/appService.do&loc=en&pvl=en_US&ctx=standalone&actId=214&objIds=443820&containerId=22099&pref=maxOpageU=10;maxOpageUt=200;maxOpageC=10;tz=Europe/Paris;mUnit=inch;showFilters=true;smtpFrom=true;promptForUnsavedData=true;'
	session.get(webiview_url)

def get_s_entry(session):
	# Get sEntry for refreshDocument.jsp
	view_document_url = 'http://bonew.qteam.be/AnalyticalReporting/viewers/cdz_adv/viewDocument.jsp?id=443820&ctx=standalone&objIds=443820&loc=en&pref=maxOpageU=10;maxOpageUt=200;maxOpageC=10;tz=Europe/Paris;mUnit=inch;showFilters=true;smtpFrom=true;promptForUnsavedData=true;&actId=214&pvl=en_US&containerId=22099&appKind=InfoView&cafWebSesInit=true&bypassLatestInstance=true&service=/InfoViewApp/common/appService.do&kind=Webi&iventrystore=widtoken&ViewType=H&entSession=CE_ENTERPRISESESSION&lang=en'
	view_document_response = session.get(view_document_url)
	# Get sEntry from response
	text = view_document_response.text
	s_entry1 = text.split('strEntry="')[1].split('"')[0]

	# Get sEntry for processPrompts.jsp
	refresh_document_url = f'http://bonew.qteam.be/AnalyticalReporting/viewers/cdz_adv/refreshDocument.jsp?iViewerID=1&sEntry={s_entry1}&iReport=0&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&iFoldPanel=0&nbPage=NaN'
	refresh_document_response = session.get(refresh_document_url)
	# Get sEntry from response
	text = refresh_document_response.text
	s_entry2 = text.split('strEntry="')[1].split('"')[0]

	# Get sEntry for downloadPDForXLS
	process_prompts_url = f'http://bonew.qteam.be/AnalyticalReporting/viewers/cdz_adv/processPrompts.jsp?iViewerID=1&sEntry={s_entry2}&iReport=0&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&iFoldPanel=0&sNEV=no&sNewDoc=false&viewType=&sApplyFormat=&iDPIndex=&bValidateSQL=false&nAction=&advPrompts=yes&bCreateDefaultReportBody=false&defaultRepTitle=Report Title'
	process_prompts_payload = {
		"LPV1_textField": "Type+values+here",
		"text_LPV1_calendarText": "",
		"LPV1_searchTxt": "Enter+your+search+pattern+here",
		"LPV1_searchVal": "",
		"PV1": "",
		"PI1": "",
		"PV1_Encoded": "",
		"sLovID": "",
		"sEmptyLab": "[EMPTY_VALUE]"
	}
	process_prompts_response = session.post(process_prompts_url, data=process_prompts_payload)
	text = process_prompts_response.text
	return text.split('sEntry=')[1].split('&')[0]

def download(session, s_entry):

	download_url = f'http://bonew.qteam.be/AnalyticalReporting/viewers/cdz_adv/downloadPDForXLS.jsp?iViewerID=1&sEntry={s_entry}&iReport=0&sPageMode=QuickDisplay&sReportMode=Analysis&iPage=1&zoom=100&isInteractive=false&iFoldPanel=0&doctype=wid&viewType=O&saveReport=N'
	response = session.get(download_url)

	return response.content


def main():
	session = requests.session()

	login(session)

	download_cookie(session)

	# NOTE: the download url is dynamic: needs an sEntry
	# This sEntry can be found in the HTML response of previous requests
	s_entry = get_s_entry(session)

	payload = download(session, s_entry)

	print('[SCRAPER] Excel file downloaded')

	return payload
