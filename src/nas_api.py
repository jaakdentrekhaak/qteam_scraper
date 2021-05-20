import requests
import json
import os

# Path of directory where this file is in
file_dir = os.path.dirname(os.path.realpath(__file__))

nas_url = 'https://putzeys.synology.me:5001'
with open(f'{file_dir}/config.json') as config:
        data = json.load(config)
        username = data['synology']['username']
        password = data['synology']['password']
info_url = '/webapi/query.cgi?api=SYNO.API.Info&version=1&method=query&query=SYNO.API.Auth,SYNO.FileStation.Upload'

# Get info about the API version we need to use to login and upload
info_response = requests.get(nas_url + info_url).json()
auth_version = info_response['data']['SYNO.API.Auth']['maxVersion']
auth_path = info_response['data']['SYNO.API.Auth']['path']
upload_version = info_response['data']['SYNO.FileStation.Upload']['maxVersion']
upload_path = info_response['data']['SYNO.FileStation.Upload']['path']

# Login and get sid
login_url = f'{nas_url}/webapi/{auth_path}?api=SYNO.API.Auth&version={auth_version}&method=login&account={username}&passwd={password}&session=FileStation'
login_response = requests.get(login_url).json()
sid = login_response['data']['sid']
