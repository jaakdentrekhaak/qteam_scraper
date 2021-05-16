import requests

login_url = 'https://putzeys.synology.me:5001/webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account=jensp%20mobile&passwd=not_my_actual_password&session=FileStation&format=cookie'

login_response = requests.get(login_url)

sid = login_response.json()['data']['sid']

print(sid)