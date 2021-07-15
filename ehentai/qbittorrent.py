import requests
import os
import time
from ehentai.settings import DOWNLOAD_DIR

__dirname = os.path.dirname(os.path.abspath(__file__))

# 下载目录
download_path = os.path.join(__dirname, '..', DOWNLOAD_DIR)

# 可执行文件目录
is_open_qbittorrent = False
qbittorrent_exe = os.path.join(
    __dirname, '..', 'bin', 'qbittorrent', 'qbittorrent.exe')


def add_torrents(torrent_urls):
    '''
        添加网络torrent到下载列表中，添加后将自动下载(如果你关闭了自动下载，将不会下载)
        qbittorrent Web API 文档: https://github.com/qbittorrent/qBittorrent/wiki
    '''

    if not os.path.exists(DOWNLOAD_DIR):
         os.makedirs(DOWNLOAD_DIR)

    # 第一次下载启动 qbittorrent
    global is_open_qbittorrent
    if(not is_open_qbittorrent):

        if(not os.path.exists(qbittorrent_exe)):
            print(f'文件不存在: {qbittorrent_exe}')
            exit(1)

        # print(f'启动 qbittorrent: {qbittorrent_exe}')

        os.popen(qbittorrent_exe)
        time.sleep(1)
        is_open_qbittorrent = True

    # print(f'下载 torrent: {torrent_link}')
    r = requests.post(
        url='http://localhost:7777/api/v2/torrents/add',
        data={
            'urls': '\r\n'.join(torrent_urls),
            'savepath': download_path,
        }
    )

    if r.status_code != 200:
        print(f'add torrents error: {r.status_code}')
