# WeReadScan

![GitHub last commit](https://img.shields.io/github/last-commit/Algebra-FUN/WeReadScan) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Algebra-FUN/WeReadScan) ![GitHub top language](https://img.shields.io/github/languages/top/Algebra-FUN/WeReadScan) [![pip](https://img.shields.io/badge/pip-0.8.5-orange)](https://pypi.org/project/WeReadScan/)

## About

This branch is a html-scan variant of WeReadScan, integrating script developed by Secant.

Thanks for Secant, this variant of WeReadScan can be more efficient.

More detail about Secant's project, you can visit https://github.com/Sec-ant/weread-scraper


## Get started

```shell
pip install WeReadScan
```

> This project needs selenium，so you should have basic knowledge of selenium.

### Demo

Talk is cheap, show you the code as following.

```python
from selenium.webdriver import Chrome, ChromeOptions
from WeReadScan import WeRead

# Important! Set headless mode for chromedriver
chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('log-level=3')

headless_driver = Chrome(options=chrome_options)

with WeRead(headless_driver,debug=True) as weread:
    # Important! Login
    weread.login()
    # get html of book by giving its url.
    weread.scan2html('https://weread.qq.com/web/reader/2c632ef071a486a92c60226')
```

## Stargazers over time

[![Stargazers over time](https://starchart.cc/Algebra-FUN/WeReadScan.svg)](https://starchart.cc/Algebra-FUN/WeReadScan)
      
