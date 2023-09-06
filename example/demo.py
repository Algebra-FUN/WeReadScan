"""
demo.py
The demo of WeReadScan.py
Copyright 2020 by Algebra-FUN
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

service = Service("/Users/creator/Downloads/msedgedriver")

# launch Webdriver
print('Webdriver launching...')
driver = Edge(service=service, options=options)
# driver = Chrome(options=chrome_options)
print('Webdriver launched.')

with WeRead(driver,debug=True) as weread:
    weread.login() #? login for grab the whole book
    weread.scan2html('https://weread.qq.com/web/reader/2c632ef071a486a92c60226kc81322c012c81e728d9d180')
    weread.scan2html('https://weread.qq.com/web/reader/a9c32f40717db77aa9c9171kc81322c012c81e728d9d180')