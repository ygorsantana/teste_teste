from bs4 import BeautifulSoup
from datetime import datetime
import glob, json, os, requests, re, sys, unicodedata, zipfile

def download_file(store):
    try:
        server_url = 'http://142.93.186.99:3001'
        username = 'admin'
        password = 'Napp2599'
        # create headers dict
        headers = dict()
        headers['content-type'] = 'application/json'

        # create payload data dict
        payload = dict()
        payload['username'] = username
        payload['password'] = password
        payload['store'] = store

        # make request on marketplace server for download latest store file
        r = requests.post(url=server_url + '/download', data=json.dumps(payload), headers=headers)

        # check status code to continue
        if r.status_code == 200:
            print('Download catalog file from {}, with status code: {} OK'.format(server_url, r.status_code))
            open('./{}.zip'.format(store.replace('.','_')), 'wb').write(r.content)
        else:
            print('Download catalog file from {}, with status code: {} FAIL {}'.format(server_url, r.status_code, r.content))
        
        # Extract file
        try:
            print("Extracting file...")
            extract_file()
            print("Extracted !")
        except:
            print("Error extracting files !!!")
            return

    except Exception as e:
        print(e)


def extract_file():
    for file in glob.glob('./*.zip'):
        with zipfile.ZipFile(file) as zip_file:
            for file_name in zip_file.namelist():
                with zip_file.open(file_name) as f:
                    xml_name = 'temp.csv'
                    open(xml_name, 'wb').write(f.read())
        os.remove(file)

