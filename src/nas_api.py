import requests
import json
import os


def upload_file(file_path, nas_url, upload_path, upload_version, sid, dest_path, create_parents=False, overwrite=False):
    session = requests.session()

    with open(file_path, 'rb') as payload:
        url = f'{nas_url}/webapi/{upload_path}?api=SYNO.FileStation.Upload&version={upload_version}&method=upload&_sid={sid}'
        
        args = {
            'path': dest_path,
            'create_parents': create_parents,
            'overwrite': overwrite,
        }

        files = {
            'file': (os.path.basename(file_path), payload, 'application/octet-stream')
        }

        r = session.post(url, data=args, files=files, verify=False)

        print(r.status_code, r.content)


def main(file_path, dest_path):
    # Path of directory where this file is in
    file_dir = os.path.dirname(os.path.realpath(__file__))

    with open(f'{file_dir}/config.json') as config:
            data = json.load(config)
            username = data['synology']['username']
            password = data['synology']['password']
            nas_url = data['synology']['url']
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

    upload_file(file_path, nas_url, upload_path, upload_version, sid, dest_path)

    print(f'[NAS] {file_path} saved to NAS')