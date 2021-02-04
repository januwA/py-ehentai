# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class EhentaiPipeline:
    def process_item(self, item, spider):
        return item


class downloadImages(ImagesPipeline):

    # download file path
    def dfpath(self, item):
        # .jpg
        ext = os.path.splitext(item['img'])[1]

        # 文件夹分装
        # downloads/<id>/<i>.jpg
        fpath = os.path.join(item['id'], item['page']+ext)

        # 全部下载到一起
        # downloads/<id>-<i>.jpg
        # fpath = '{0}-{1}{2}'.format(item['id'], item['page'], ext)
        return fpath

    # 重写获取图片
    def get_media_requests(self, item, info):
        return scrapy.Request(item['img'])

    # 重写保存路径
    def file_path(self, request, response=None, info=None, *, item=None):
        return self.dfpath(item)

    # 下载完成
    def item_completed(self, results, item, info):
        print('下载完成: ' + self.dfpath(item))
        return item
