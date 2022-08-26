'''
WeRead.py
Copyright 2020 by Algebra-FUN
ALL RIGHTS RESERVED.
'''

from matplotlib import pyplot as plt
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from .script import dir_check, os_start_file, clear_temp

from time import sleep
import os


class WeRead:
    """
        The agency who control `WeRead` web page with selenium webdriver to processing book scanning.

        `微信读书`网页代理，用于图书扫描

        :Args:
         - headless_driver:
                Webdriver instance with headless option set.
                设置了headless的Webdriver示例

        :Returns:
         - WeReadInstance

        :Usage:
            chrome_options = ChromeOptions()
            chrome_options.add_argument('--headless')

            headless_driver = Chrome(chrome_options=chrome_options)

            weread = WeRead(headless_driver)
    """

    current_book_name = ''

    def __init__(self, headless_driver: WebDriver, patience=15, debug=False):
        headless_driver.get('https://weread.qq.com/')
        headless_driver.implicitly_wait(5)
        self.driver: WebDriver = headless_driver
        self.debug_mode = debug
        self.patience = patience
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.inject_js = self.load_js_file('inject')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self.debug_mode:
            clear_temp('wrs-temp')

    def load_js_file(self, name):
        with open(f'{self.path}\\script\\{name}.js','r',encoding='utf-8') as f:
            return f.read()

    def S(self, selector):
        return WebDriverWait(self.driver, self.patience).until(lambda driver: driver.find_element(By.CSS_SELECTOR, selector))

    def click(self, target):
        self.driver.execute_script('arguments[0].click();', target)

    def shot_full_canvas_context(self, file_name):
        renderTargetContainer = self.S('.renderTargetContainer')
        height = renderTargetContainer.get_property('offsetHeight')
        height += renderTargetContainer.get_property('offsetTop')
        width = self.driver.execute_script("return window.outerWidth")
        self.driver.set_window_size(width, height)
        sleep(1)
        content = self.S('.app_content')
        content.screenshot(file_name)

    def login(self, wait_turns=15):
        """
        show QRCode to login weread.

        展示二维码以登陆微信读书

        :Args:
         - wait_turns:
                Loop turns wait for scanning QRCode
                登陆二维码等待扫描的等待轮数

        :Usage:
            weread.login()
        """

        dir_check('wrs-temp')

        # get QRCode for Login
        self.S('button.navBar_link_Login').click()
        self.S('.login_dialog_qrcode>img').screenshot(
            'wrs-temp/login_qrcode.png')

        login_qrcode = Image.open('wrs-temp/login_qrcode.png')
        plt.ion()
        plt.title('Scan this QRCode to Login.')
        plt.imshow(login_qrcode)
        plt.show()
        plt.pause(.001)

        # wair for QRCode Scan
        for i in range(wait_turns):
            print(f'Waiting for QRCode Scan...{i}/{wait_turns}turns')
            try:
                self.driver.find_element(By.CSS_SELECTOR, '.menu_container')
                print('Login Succeed.')
                break
            except Exception:
                plt.pause(1)
        else:
            raise Exception('WeRead.Timeout: Login timeout.')

        # close QRCode Window
        plt.ioff()
        plt.close()

    def switch_to_context(self):
        """switch to main body of the book"""
        self.S('button.catalog').click()
        self.S('li.chapterItem:nth-child(2)').click()

    def inject_observer_js(self):
        self.driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument', {'source': self.inject_js})

    def observer_start(self):
        js = '''
        contentObserver.observe(document.documentElement, {
            childList: true,
            subtree: true,
        });
        '''
        self.driver.execute_script(js)

    def get_html(self, book_url):
        # valid the url
        if 'https://weread.qq.com/web/reader/' not in book_url:
            raise Exception('WeRead.UrlError: Wrong url format.')

        # inject observer js
        self.inject_observer_js()

        # switch to target book url
        self.driver.get(book_url)

        # init observer
        self.observer_start()

        # switch to target book's cover
        self.switch_to_context()

        # get the name of the book
        self.current_book_name = self.S('span.readerTopBar_title_link').text
        print(f'Scanning the book:"{self.current_book_name}"')

        while True:
            # find next page or chapter button
            try:
                readerFooter = self.S('.readerFooter_button,.readerFooter_ending')
            except Exception:
                break
            
            readerFooterClass = readerFooter.get_attribute('class')

            if 'ending' in readerFooterClass:
                break

            # go to next page or chapter
            readerFooter.click()

        self.driver.execute_script("contentObserver.disconnect()")
        html = self.driver.execute_script("return rootElement.outerHTML")
        self.driver.execute_script(
            'styleElement.innerHTML = "";bodyElement.innerHTML = "";')

        return html

    def download_html(self, html, save_at='.', book_name='', show_output=True):
        book_name = book_name or self.current_book_name
        print(f'Downloading the book:"{book_name}"')
        dir_check(save_at)
        save_path = f'{save_at}/{book_name}.html'
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(html)
        if show_output:
            os_start_file(save_path)
        return save_path

    def scan2html(self, book_url, save_at='.', show_output=True):
        html = self.get_html(book_url)
        self.download_html(html, save_at=save_at, show_output=show_output)
