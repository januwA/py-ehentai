import requests
import os
from ehentai.settings import PROXY, IMAGES_STORE,WEB_API


__dirname__ = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', IMAGES_STORE)

def add_torrents(urls, path):  # 添加网络torrent到下载列表中，添加后将自动下载(如果你关闭了自动下载，将不会下载)
    r = requests.post(
        url=WEB_API+'/api/v2/torrents/add',
        data={
            'urls': urls,
            'savepath': os.path.join(__dirname__, path),
        }
    )
    if r.status_code != 200:
        print('add torrents error.')
