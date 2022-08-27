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
from selenium.webdriver import Chrome, ChromeOptions

from WeReadScan import WeRead

# options
chrome_options = ChromeOptions()

# now you can choose headless or not
chrome_options.add_argument('--headless')  
 
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('log-level=3')

# launch Webdriver
print('Webdriver launching...')
driver = Chrome(options=chrome_options)
print('Webdriver launched.')

with WeRead(driver) as weread:
    # login to grab the whole book
    weread.login() 
    # scan the book number one with it's url
    weread.scan2html('https://weread.qq.com/web/reader/2c632ef071a486a92c60226kc81322c012c81e728d9d180')
    # scan the book number two with it's url
    weread.scan2html('https://weread.qq.com/web/reader/a9c32f40717db77aa9c9171kc81322c012c81e728d9d180')
```

## Usage

Just code as demo show.

## Stargazers over time

[![Stargazers over time](https://starchart.cc/Algebra-FUN/WeReadScan.svg)](https://starchart.cc/Algebra-FUN/WeReadScan)  
