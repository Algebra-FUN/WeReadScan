'''
demo.py
The demo of WeReadScan.py
Copyright 2020 by Algebra-FUN
ALL RIGHTS RESERVED.
'''


from selenium.webdriver import Chrome, ChromeOptions

from WeReadScan import WeRead

# options
chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('log-level=3')

# launch Webdriver
print('Webdriver launching...')
driver = Chrome(chrome_options=chrome_options)
print('Webdriver launched.')

with WeRead(driver) as weread:
    weread.login()
    weread.scan2pdf('https://weread.qq.com/web/reader/1f132bb071a1a7861f14eb4')
