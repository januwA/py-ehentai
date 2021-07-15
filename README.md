## 运行爬虫
```
$ git clone git@github.com:januwA/py-ehentai.git
$ cd py-ehentai
$ conda install -c conda-forge scrapy
$ scrapy crawl example
```

如果运行错误，尝试[将conda添加到环境变量](https://www.zhihu.com/question/308832259)

一些版本信息
```
λ python --version
Python 3.8.5

λ scrapy version
Scrapy 2.4.1

λ conda --version
conda 4.10.1
```

## miniconda
- [下载 miniconda (python环境)](https://docs.conda.io/en/latest/miniconda.html)

## 网络代理
- 修改`ehentai/settings.py`中的`PROXY`

## unzip.py

解压所有"./downloads/\*.{zip|rar|7z}"文件，解压后压缩文件将被删除

```
python unzip.py
```