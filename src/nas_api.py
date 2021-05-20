import requests

nas_url = 'https://putzeys.synology.me:5001'
username = ''
password = ''
info_url = '/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.FileStation.Upload'
login_url = f'/webapi/auth.cgi?api=SYNO.API.Auth&version=3&method=login&account={username}&passwd={password}&session=FileStation'

# Get info about the API version we need to use to login and upload
info_response = requests.get(info_url).json()
auth_version = info_response['data']['SYNO.API.Auth']['maxVersion']
auth_path = info_response['data']['SYNO.API.Auth']['path']
upload_version = info_response['data']['SYNO.FileStation.Upload']['maxVersion']
upload_path = info_response['data']['SYNO.FileStation.Upload']['path']

# Login and get sid
login_url = f'{nas_url}/webapi/{auth_path}?api=SYNO.API.Auth&version={auth_version}&method=login'

