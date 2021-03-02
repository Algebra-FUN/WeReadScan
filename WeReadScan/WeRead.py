'''
WeRead.py
Copyright 2020 by Algebra-FUN
ALL RIGHTS RESERVED.
'''

from matplotlib import pyplot as plt
from PIL import Image
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from .script import jpg2pdf, png2jpg, dir_check, os_start_file, clear_temp

from time import sleep


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

    def __init__(self, headless_driver: WebDriver, debug=False):
        headless_driver.get('https://weread.qq.com/')
        headless_driver.implicitly_wait(5)
        self.driver: WebDriver = headless_driver
        self.debug_mode = debug

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self.debug_mode:
            clear_temp('wrs-temp')

    def S(self, selector):
        return WebDriverWait(self.driver, 60).until(lambda driver: driver.find_element_by_css_selector(selector))

    def execute_script(self,script):
        return self.driver.execute_script(script)

    def shot_full_canvas_context(self,file_name):
        sleep(1)
        try:
            self.__offsetTop = self.execute_script("return document.querySelector('.renderTargetContainer').offsetTop")
            self.__offsetHeight = self.execute_script("return document.querySelector('.renderTargetContainer').offsetHeight")
        except Exception:
            pass
        width = self.execute_script("return window.outerWidth")
        self.__offsetHeight += self.__offsetTop
        self.driver.set_window_size(width, self.__offsetHeight)
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
            print(f'Wait for QRCode Scan...{i}/{wait_turns}turns')
            try:
                self.driver.find_element_by_css_selector('.menu_container')
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
    
    def set_font_size(self,font_size_index=1):
        """
        set font size

        设置字体大小

        :Args:
         - font_size_index=0:
                the index of font size(1-7)
                字体大小级别(1-7)
                In particular, 1 represents minimize, 7 represents maximize
                特别地，1为最小，7为最大
        """ 
        sleep(1)
        self.S('button.fontSizeButton').click()
        sleep(1)
        self.S(f'.vue-slider-mark:nth-child({font_size_index})').click()
        self.S('.app_content').click()

    def turn_light_on(self):
        sleep(1)
        self.S('button.readerControls_item.white').click()

    def scan2pdf(self, book_url, save_at='.', binary_threshold=200, quality=95, show_output=True, font_size_index=1):
        """
        scan `weread` book to pdf and save offline.

        扫面`微信读书`的书籍转换为PDF并保存本地

        :Args:
         - book_url:
                the url of weread book which aimed to scan
                扫描目标书籍的ULR
         - save_at='.':
                the path of where to save
                保存地址
         - binary_threshold=200:
                threshold of scan binary
                二值化处理的阈值
         - quality=95:
                quality of scan pdf
                扫描PDF的质量
         - show_output=True:
                if show the output pdf file at the end of this method
                是否在该方法函数结束时展示生成的PDF文件
         - font_size_index=1:
                the index of font size(1-7)
                字体大小级别(1-7)
                In particular, 1 represents minimize, 7 represents maximize
                特别地，1为最小，7为最大

        :Usage:
            weread.scan2pdf('https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180')
        """
        print('Task launching...')

        # valid the url
        if 'https://weread.qq.com/web/reader/' not in book_url:
            raise Exception('WeRead.UrlError: Wrong url format.')

        # switch to target book url
        self.driver.get(book_url)
        print(f'navigate to {book_url}')

        # turn theme to light theme
        self.turn_light_on()

        # set font size
        self.set_font_size(font_size_index)

        # switch to target book's cover
        self.switch_to_context()

        # get the name of the book
        book_name = self.S('span.readerTopBar_title_link').text
        print(f'preparing to scan "{book_name}"')

        # check the dir for future save
        dir_check(f'wrs-temp/{book_name}/context')

        # used to store jpg_name for pdf converting
        jpg_name_list = []

        while True:
            sleep(1)

            # get chapter
            chapter = self.S('span.readerTopBar_title_chapter').text
            print(f'scanning chapter "{chapter}"')

            # locate the renderTargetContent
            context = self.S('div.app_content')

            # context_scan2png
            png_name = f'wrs-temp/{book_name}/context/{chapter}'
            self.shot_full_canvas_context(f'{png_name}.png')

            # png2bin-jpg
            jpg_name = png2jpg(png_name, binary_threshold, quality)
            jpg_name_list.append(jpg_name)
            print(f'save chapter scan {jpg_name}')

            # go to next chapter
            try:
                self.S('button[title="下一章"]').click()
            except Exception:
                break

        print('pdf converting...')

        # convert to pdf and save offline
        jpg2pdf(f'{save_at}/{book_name}', jpg_name_list)
        print('scanning finished.')
        if show_output:
            os_start_file(f'{save_at}/{book_name}.pdf')
