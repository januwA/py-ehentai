import requests
import os
import time
from ehentai.settings import DOWNLOAD_DIR

__dirname = os.path.dirname(os.path.abspath(__file__))

qbittorrent_exe = os.path.join(
    __dirname, '..', 'bin', 'qbittorrent', 'qbittorrent.exe')

if(not os.path.exists(qbittorrent_exe)):
    print(f'文件不存在: {qbittorrent_exe}')
    exit(1)
else: os.popen(qbittorrent_exe)

# 检查保存目录
download_path = os.path.join(__dirname, '..', DOWNLOAD_DIR)
if not os.path.exists(download_path):
    os.makedirs(download_path)


def add_torrents(torrent_urls):
    '''
        添加网络torrent到下载列表中，添加后将自动下载(如果你关闭了自动下载，将不会下载)
        qbittorrent Web API 文档: https://github.com/qbittorrent/qBittorrent/wiki
    '''

    r = requests.post(
        url='http://localhost:7777/api/v2/torrents/add',
        data={
            'urls': '\r\n'.join(torrent_urls),
            'savepath': download_path,
        }
    )

    if r.status_code != 200:
        print(f'Error [torrents/add]: {r.status_code}')
