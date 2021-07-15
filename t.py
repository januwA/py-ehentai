import os
import time
import requests

__dirname = os.path.dirname(os.path.abspath(__file__))
download_path = os.path.join(__dirname, 'test_dir')
qbittorrent_exe = os.path.join(__dirname, 'bin', 'qbittorrent', 'qbittorrent.exe')
os.popen(qbittorrent_exe)


torrent_urls = [
"https://www.torrentdownloads.pro/td/?search=1&keyword=adventure-harbor-2021-720p-webrip-yts-mx",
"https://www.torrentdownloads.pro/td/?search=1&keyword=gunpowder-milkshake-2021-1080p-webrip-x264-rarbg",
"https://www.torrentdownloads.pro/td/?search=1&keyword=gunpowder-milkshake-2021-1080p-webrip-5-1-yts-mx",
]

r = requests.post(
    url='http://localhost:7777/api/v2/torrents/add',
    data={
        'urls': '\r\n'.join(torrent_urls),
        'savepath': download_path,
    }
)

if r.status_code != 200:
    print(f'add torrents error: {r.status_code}')
    

