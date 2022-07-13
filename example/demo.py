"""
demo.py
The demo of WeReadScan.py
Copyright 2020 by Algebra-FUN
ALL RIGHTS RESERVED.
"""


from selenium.webdriver import Chrome, ChromeOptions

from WeReadScan import WeRead

# options
chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')  #! important argument
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument('log-level=3')

# launch Webdriver
print('Webdriver launching...')
driver = Chrome(options=chrome_options)
print('Webdriver launched.')

with WeRead(driver,debug=True) as weread:
    weread.login() #? login for grab the whole book
    weread.scan2pdf('https://weread.qq.com/web/reader/60b32c107207bc8960bd9cekecc32f3013eccbc87e4b62e')