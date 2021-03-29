# WeReadScan

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/c00b1cc6fa3245668bbda64584479f9d)](https://app.codacy.com/manual/Algebra-FUN/WeReadScan?utm_source=github.com&utm_medium=referral&utm_content=Algebra-FUN/WeReadScan&utm_campaign=Badge_Grade_Dashboard) ![GitHub last commit](https://img.shields.io/github/last-commit/Algebra-FUN/WeReadScan) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Algebra-FUN/WeReadScan) ![GitHub top language](https://img.shields.io/github/languages/top/Algebra-FUN/WeReadScan) [![pip](https://img.shields.io/badge/pip-0.8.3-orange)](https://pypi.org/project/WeReadScan/)

## About

一个用于的将`微信读书`上的图书扫描转换本地PDF的爬虫库.

### 谈谈为何而开发

不得不说，“微信读书”是一个很好的平台。但是美中不足很明显，用户购买了图书资源，但是只能在“微信读书”的Application中阅读或者做一些文字批注╮(╯▽╰)╭，这些功能相较于购买的纸质书籍显然是不足的。比如，作者就习惯于用iPad的相关notebook类app做笔记，而“微信读书”并没有适配pencil做handwriting笔记的功能。

因此，既然“微信读书”没有提供，那只好自己解决了。于是，经过2天的开发，终于有了这个爬虫脚本，也可以开心地做手写笔记了o(_￣▽￣_)ブ

## Get started

```shell
pip install WeReadScan
```

> 本项目需要使用selenium，需要对selenium具备基础的了解

### Demo

话不多说，直接上代码

```python
from selenium.webdriver import Chrome, ChromeOptions
from WeReadScan import WeRead

# 重要！为webdriver设置headless
chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--window-size=1440,900')

# 启动webdriver(--headless)
headless_driver = Chrome(options=chrome_options)

with WeRead(headless_driver) as weread:
    # 重要！登陆
    weread.login()
    # 爬去指定url对应的图书资源并保存到当前文件夹
    weread.scan2pdf('https://weread.qq.com/web/reader/2c632ef071a486a92c60226', keep_color=True)
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

### Scan2pdf

WeReadScan.WeRead.scan2pdf(self, book_url, save_at='.', binary_threshold=95, keep_color=True, show_output=True,font_size_index=1)

扫面`微信读书`的书籍转换为PDF并保存本地

#### Args

| 参数名              | 类型   | 默认值  | 描述                    |
| ---------------- | ---- | ---- | --------------------- |
| book_url         | str  | 必填   | 扫描目标书籍的URL            |
| save_at          | str  | '.'  | 保存地址                  |
| binary_threshold | int  | 200   | 二值化处理的阈值              |
| keep_color          | bool  | False   | 是否保持原色，或者转换成黑白模式           |
| show_output      | bool | True | 是否在该方法函数结束时展示生成的PDF文件 |
| font_size_index  | int  | 1 | 设置字号大小(对应微信读书字号) |

#### Usage

```python
weread.scan2pdf('https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180')
```

## Disclaimer

-   本脚本仅限用于**已购**图书的爬取，用于私人学习目的，禁止用于商业目的和网上资源扩散，尊重微信读书方面的利益
-   若User使用该脚本用于不当的目的，责任由使用者承担，作者概不负责
