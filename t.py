import requests
import os
import re

with open('./a.txt', 'a+', encoding='utf-8') as fp:
  fp.write('\r\nasd')