import os
import time
import requests

os.popen(f'.\\bin\\qbittorrent\\qbittorrent.exe')

__dirname = os.path.dirname(os.path.abspath(__file__))
download_path = os.path.join(__dirname, 'test_dir')

r = requests.post(
    timeout=3000,
    url='http://localhost:7777/api/v2/torrents/add',
    data= {
        'urls': ['https://ehtracker.org/get/1671092/10357fc4f9ea1c5da7311392b292e0891d804401.torrent'],
        'savepath': os.path.join(download_path),
    }
)

if r.status_code != 200:
    print('add torrents error.')
else:
    print(r.status_code)

