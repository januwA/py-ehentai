import scrapy
import os
import re
from ehentai.items import EhentaiItem
from urllib.parse import urlparse, parse_qs
import datetime
from ehentai.settings import README_FILENAME, IMAGES_STORE
from ehentai.qbittorrent import add_torrents


class ExampleSpider(scrapy.Spider):
    name = 'example'
    # allowed_domains = ['example.com']

    _start_page = 0  # 分页从0开始
    _end_page = 10  # 到多少页结束爬取

    # page 分页
    # f_sr 开启最低评分
    # f_srdd 评分
    URL_TEMP = 'https://e-hentai.org/?page={0}&f_cats=959&f_sr=on&f_srdd=4'

    start_urls = []

    def __init__(self):
        self.start_urls.append(self.URL_TEMP.format(self._start_page))

    # torrent 列表页面
    def torrent_page(self, res):
        id = parse_qs(urlparse(res.url).query)['gid'][0]
        fpath = os.path.join(IMAGES_STORE, id, README_FILENAME)
        table_list = res.xpath(
            '//div[@id="torrentinfo"]/div[1]/descendant::table[./tr[3]/descendant::a]')

        latest_torrent = ''
        latest_date = ''
        for it in table_list:
            href = it.xpath(
                './tr[3]/descendant::a/@href').extract_first().strip()
            date = it.xpath('./tr[1]/td[1]/text()').extract_first().strip()
            size = it.xpath('./tr[1]/td[2]/text()').extract_first().strip()
            
            # 获取最新的torrent地址
            if not latest_torrent:
                latest_torrent = href
                latest_date = date
            else:
                if datetime.datetime.fromisoformat(date) > datetime.datetime.fromisoformat(latest_date):
                    latest_torrent = href
                    latest_date = date

            with open(fpath, 'a+', encoding='utf-8') as fp:
                fp.write('''\r\n{date}\t{size}\r{href}'''.format(
                    date=date, size=size, href=href))
        add_torrents(urls=[latest_torrent], path=id)

    # 原图页面
    def s_page(self, res):
        origin_img = res.xpath('//img[@id="img"]/@src')
        info = os.path.basename(res.url).split('-')

        if origin_img:
            item = EhentaiItem()
            item['id'] = info[0].strip()
            item['page'] = info[1].strip()
            item['img'] = origin_img.extract_first()
            yield item  # 下载图片
        else:
            print("Origin image not find: %s" % (res.url))

        url = res.xpath('//a[@id="next"]/@href').extract_first()
        if url != res.url:  # 确保还有下一张
            yield scrapy.Request(url=url, callback=self.s_page)

    # detai 列表页面
    def g_page(self, res):
        first_s_page_url = res.xpath('//div[@id="gdt"]/div[1]/div/a/@href')

        has_torrent = False
        # get torrent list
        torrent_a = res.xpath(
            '//*[@id="gd5"]/descendant::a[contains(text(), "Torrent")]')
        if torrent_a:
            torrent_a_text = torrent_a.xpath('./text()').extract_first()
            m = re.match(r'.*(\d+)', torrent_a_text)
            if m and m[1] and m[1].strip() != '0':  # has torrent list
                onclick_str = torrent_a.xpath('./@onclick').extract_first()
                torrent_page_url = re.match(
                    r".*popUp\('([^']+)'", onclick_str, re.I)[1]
                has_torrent = True
                yield scrapy.Request(url=torrent_page_url,
                                     callback=self.torrent_page)

        # 没有torrent才一张一张下载图片
        # 图片下载多了，会被禁止下载
        if not has_torrent:
            if first_s_page_url:
                yield scrapy.Request(url=first_s_page_url.extract_first(), callback=self.s_page)
            else:
                print('g_page not find first image: %s' % (res.url))

    def parse(self, res):
        # 过滤第一个tr和没有td[3]的tr
        tr_list = res.xpath(
            '//table[contains(@class, "itg")]/tr[position()>1 and ./td[3]]')

        if not len(tr_list):  # 当前page没有数据,不在继续
            print('EMPTY: curent page is ({0})'.format(self._start_page))
            return

        for tr in tr_list:
            name = tr.xpath('./td[3]/a/div[1]/text()').extract_first()
            g_page_url = tr.xpath('./td[3]/a//@href').extract_first()

            id = re.compile(r'.*/g/(.+?)/', re.I).match(g_page_url)[1]
            dpath = os.path.join(IMAGES_STORE, id)
            if os.path.exists(dpath):  # 避免重复下载
                # print("文件(%s)已存在,跳过重复下载!" % (id))
                continue
            else:  # 创建readme
                self.createReadmeFile(dpath, name, g_page_url)
            yield scrapy.Request(url=g_page_url, callback=self.g_page)

        # 爬取下一页
        self._start_page += 1
        if self._start_page < self._end_page:
            yield scrapy.Request(url=self.URL_TEMP.format(self._start_page), callback=self.parse)

    def createReadmeFile(self, dpath, name, url):
        os.makedirs(dpath)
        with open(os.path.join(dpath, README_FILENAME), 'w', encoding='utf-8') as fp:
            fp.write("{0}\r\n{1}".format(name, url))
