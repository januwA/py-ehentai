# Scrapy settings for ehentai project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'ehentai'

SPIDER_MODULES = ['ehentai.spiders']
NEWSPIDER_MODULE = 'ehentai.spiders'
LOG_LEVEL = 'ERROR'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 下载目录，别改
DOWNLOAD_DIR = './downloads/'

# 代理地址
PROXY = 'http://localhost:19996'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# 配置对同一网站的请求延迟 (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# 下载延迟设置仅支持以下一项:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# 禁用cookie (enabled by default)
#COOKIES_ENABLED = False

# 禁用Telnet控制台 (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'ehentai.middlewares.EhentaiSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'ehentai.middlewares.HttpProxyMiddleware': 1,

   #  'ehentai.middlewares.EhentaiDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'ehentai.pipelines.EhentaiPipeline': 300,
    'ehentai.pipelines.downloadImages': 301,
}

# 启用和配置AutoThrottle扩展名 (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# 初始下载延迟
#AUTOTHROTTLE_START_DELAY = 5
# 高延迟时要设置的最大下载延迟
#AUTOTHROTTLE_MAX_DELAY = 60
# Scrapy应该并行发送到每个远程服务器的平均请求数
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# 为收到的每个响应启用节流统计信息:
#AUTOTHROTTLE_DEBUG = False

# 启用和配置HTTP缓存 (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
