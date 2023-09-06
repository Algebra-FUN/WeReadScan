# WeReadScan (html-scan variant)

![GitHub last commit](https://img.shields.io/github/last-commit/Algebra-FUN/WeReadScan) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Algebra-FUN/WeReadScan) ![GitHub top language](https://img.shields.io/github/languages/top/Algebra-FUN/WeReadScan)

## About

This branch is a html-scan variant of WeReadScan, integrating script developed by [Sec-ant](https://github.com/Sec-ant).

Thanks for [Sec-ant](https://github.com/Sec-ant), this variant of WeReadScan can be more efficient.

More detail about Sec-ant's project, you can visit https://github.com/Sec-ant/weread-scraper

## Get started

```
pip install WeReadScan-HTML
```

> This package needs selenium, so you should have some basis of selenium.

## Demo

Talk is cheap, just show you the code.

```python
"""
demo.py
The demo of WeReadScan.py
Copyright 2023 by Algebra-FUN
ALL RIGHTS RESERVED.
"""


from selenium.webdriver import Edge
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.options import Options

from WeReadScan import WeRead


options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('disable-infobars')
options.add_argument('log-level=3')
options.add_argument("headless")

# service = Service("/Users/creator/Downloads/msedgedriver")

# launch Webdriver
print('Webdriver launching...')
driver = Edge(options=options)
# driver = Edge(service=service, options=options)
print('Webdriver launched.')

with WeRead(driver,debug=True) as weread:
    weread.login() #? login for grab the whole book
    weread.scan2html('https://weread.qq.com/web/reader/2c632ef071a486a92c60226kc81322c012c81e728d9d180')
    weread.scan2html('https://weread.qq.com/web/reader/a9c32f40717db77aa9c9171kc81322c012c81e728d9d180')
```

## Usage

Just code as demo show.

## Stargazers over time

[![Stargazers over time](https://starchart.cc/Algebra-FUN/WeReadScan.svg)](https://starchart.cc/Algebra-FUN/WeReadScan)  
