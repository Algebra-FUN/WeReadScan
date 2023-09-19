# WeReadScan

![GitHub last commit](https://img.shields.io/github/last-commit/Algebra-FUN/WeReadScan) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Algebra-FUN/WeReadScan) ![GitHub top language](https://img.shields.io/github/languages/top/Algebra-FUN/WeReadScan) [![pip](https://img.shields.io/badge/pip-0.8.7-orange)](https://pypi.org/project/WeReadScan/)

## About

一个用于的将`微信读书`上的图书扫描转换本地PDF/HTML的爬虫库.

### 谈谈为何而开发

不得不说，“微信读书”是一个很好的平台。但是美中不足很明显，用户购买了图书资源，但是只能在“微信读书”的Application中阅读或者做一些文字批注╮(╯▽╰)╭，这些功能相较于购买的纸质书籍显然是不足的。比如，作者就习惯于用iPad的相关notebook类app做笔记，而“微信读书”并没有适配pencil做handwriting笔记的功能。

因此，既然“微信读书”没有提供，那只好自己解决了。于是，经过2天的开发，终于有了这个爬虫脚本，也可以开心地做手写笔记了o(_￣▽￣_)ブ

### 相关版本

在[Sec-ant](https://github.com/Sec-ant)的建议下，参考了他的解决方案[weread-scraper](https://github.com/Sec-ant/weread-scraper)，将其中最重要的获取#preRenderContent的部分脚本进行整合，得到了[WeReadScan-HTML](https://github.com/Algebra-FUN/WeReadScan/tree/html-variant)版本，可以直接自动化获得多本图书的HTML，更加高效。

## Get started

```shell
pip install WeReadScan-HTML
```

> 本项目需要使用selenium，需要对selenium具备基础的了解

### Demo

话不多说，直接上代码

```python
from selenium.webdriver import Edge
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.edge.options import Options

from WeReadScan import WeRead

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('disable-infobars')
options.add_argument('log-level=3')
options.add_argument("headless")

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

扫描结果样例：

![](https://github.com/Algebra-FUN/WeReadScan/blob/master/example/sample.png?raw=true)

几点说明：

1.  webdriver 需要 `无头(headless)` 模式启动
2.  只有登陆后，才能扫描完整的图书资源；若不登陆，也可以扫描部分无需解锁的部分

## API Reference

### WeRead

WeReadScan.WeRead(headless_driver)

`微信读书`网页代理，用于图书扫描

#### Args

-   headless_driver:	设置了headless的Webdriver示例

#### Returns

-   WeReadInstance

#### Usage

```python
chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
headless_driver = Chrome(chrome_options=chrome_options)
weread = WeRead(headless_driver)
```

### Login

WeReadScan.WeRead.login(wait_turns=15)

展示二维码以登陆微信读书

#### Args

-   wait_turns:	登陆二维码等待扫描的等待轮数

#### Usage

```python
weread.login()
```

### Scan2html

WeReadScan.WeRead.scan2html(book_url, save_at='.', show_output=True)

扫面`微信读书`的书籍转换为PDF并保存本地

#### Args

| 参数名              | 类型   | 默认值  | 描述                    |
| ---------------- | ---- | ---- | --------------------- |
| book_url         | str  | 必填   | 扫描目标书籍的URL            |
| save_at          | str  | '.'  | 保存地址                  |
| show_output      | bool | True | 是否在该方法函数结束时展示生成的PDF文件 |

#### Usage

```python
weread.scan2html('https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180')
```

## Disclaimer

-   本脚本仅限用于**已购**图书的爬取，用于私人学习目的，禁止用于商业目的和网上资源扩散，尊重微信读书方面的利益
-   若User使用该脚本用于不当的目的，责任由使用者承担，作者概不负责

## Stargazers over time

[![Stargazers over time](https://starchart.cc/Algebra-FUN/WeReadScan.svg)](https://starchart.cc/Algebra-FUN/WeReadScan)
      
