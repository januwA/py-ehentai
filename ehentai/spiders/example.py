import scrapy
import os
import re
from ehentai.items import EhentaiItem
from urllib.parse import urlparse, parse_qs
import datetime
from ehentai.settings import DOWNLOAD_DIR
from ehentai.qbittorrent import add_torrents


class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = []
    # allowed_domains = ['example.com']

    # page 分页
    # f_sr 开启最低评分
    # f_srdd 评分
    # f_cats 搜索类型
    page = 0   # 分页从0开始
    end_page = 1  # 到多少页结束爬取
    category = {'Copslay': 959}
    f_srdd = 5

    def __init__(self):
        self.start_urls.append(self.get_url())

    def get_url(self):
        url = f'''https://e-hentai.org/?page={self.page}&f_cats={self.category['Copslay']}&f_sr=on&f_srdd={self.f_srdd}'''
        # print(f'正在爬取页面: {url}')
        return url

    def torrent_page(self, res):
        ''' torrent 列表页面，获取torrent link并下载种子 '''
        id = parse_qs(urlparse(res.url).query)['gid'][0]
        fpath = os.path.join(DOWNLOAD_DIR, id, 'readme.md')
        table_list = res.xpath(
            '//div[@id="torrentinfo"]/div[1]/descendant::table[./tr[3]/descendant::a]')

        torrent_link = ''
        latest_date = ''
        for it in table_list:
            href = it.xpath(
                './tr[3]/descendant::a/@href').extract_first().strip()
            date = it.xpath('./tr[1]/td[1]/text()').extract_first().strip()
            size = it.xpath('./tr[1]/td[2]/text()').extract_first().strip()

            # 获取最新的torrent地址
            if not torrent_link:
                torrent_link = href
                latest_date = date
            else:
                if datetime.datetime.fromisoformat(date) > datetime.datetime.fromisoformat(latest_date):
                    torrent_link = href
                    latest_date = date

            with open(fpath, 'a+', encoding='utf-8') as fp:
                fp.write(f'\r\n{date}\t{size}\r{href}')
        add_torrents(torrent_link, id)

    # 废弃，没有torrent将不再下载原图
    # def s_page(self, res):
    #     ''' 原图页面，下载原图 '''
    #     origin_img = res.xpath('//img[@id="img"]/@src')
    #     info = os.path.basename(res.url).split('-')

    #     if origin_img:
    #         item = EhentaiItem()
    #         item['id'] = info[0].strip()
    #         item['page'] = info[1].strip()
    #         item['img'] = origin_img.extract_first()
    #         yield item  # 下载图片
    #     else:
    #         print("Origin image not find: %s" % (res.url))

    #     url = res.xpath('//a[@id="next"]/@href').extract_first()
    #     if url != res.url:  # 确保还有下一张
    #         yield scrapy.Request(url=url, callback=self.s_page)

    def g_page(self, res):
        ''' 详情页面获取torrent下载信息 '''
        first_s_page_url = res.xpath('//div[@id="gdt"]/div[1]/div/a/@href')

        if not first_s_page_url:
            print(f'  获取 first_s_page_url 失败')
            return

        # get torrent list
        torrent_a = res.xpath(
            '//*[@id="gd5"]/descendant::a[contains(text(), "Torrent")]')
        if not torrent_a:
            print(f'  未发现 torrent 资源')
            return

        torrent_a_text = torrent_a.xpath('./text()').extract_first()
        m = re.match(r'.*(\d+)', torrent_a_text)

        if not m or not m[1]:
            print(f'  获取 torrent 资源数量失败')
            return

        if m[1].strip() == 0:
            print('  torrent 资源数量为0')
            return

        onclick_str = torrent_a.xpath('./@onclick').extract_first()
        torrent_page_url = re.match(
            r".*popUp\('([^']+)'", onclick_str, re.I)[1]

        if not torrent_page_url:
            print('  获取 torrent 资源页面 url 失败')
            return

        # print(f'  torrent资源页面url: {torrent_page_url}')
        yield scrapy.Request(url=torrent_page_url, callback=self.torrent_page)

    def parse(self, res):
        ''' 解析页面列表，然后进入每条数据的详情页面(g_page_url) '''
        # 过滤第一个tr和没有td[3]的tr
        tr_list = res.xpath(
            '//table[contains(@class, "itg")]/tr[position()>1 and ./td[3]]')

        if not len(tr_list):  # 当前页面没有数据,不在继续
            print(f'页面没有数据: ({self.page})')
            return

        for tr in tr_list:
            name = tr.xpath('./td[3]/a/div[1]/text()').extract_first()
            g_page_url = tr.xpath('./td[3]/a//@href').extract_first()
            id = re.compile(r'.*/g/(.+?)/', re.I).match(g_page_url)[1]
            dpath = os.path.join(DOWNLOAD_DIR, id)
            if os.path.exists(dpath):  # 避免重复下载
                print(f"文件已存在跳过: { os.path.join(DOWNLOAD_DIR, id) }")
                continue
            else:  # 创建readme
                self.createReadmeFile(dpath, name, g_page_url)
                yield scrapy.Request(url=g_page_url, callback=self.g_page)

        # 爬取下一页
        self.page += 1
        if self.page < self.end_page:
            yield scrapy.Request(url=self.get_url(), callback=self.parse)

    def createReadmeFile(self, dpath, name, url):
        os.makedirs(dpath)
        with open(os.path.join(dpath, 'readme.md'), 'w', encoding='utf-8') as fp:
            fp.write(f"{name}\r\n{url}")
