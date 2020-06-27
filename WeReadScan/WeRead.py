'''
WeRead.py
Copyright 2020 by Algebra-FUN
ALL RIGHTS RESERVED.
'''


from time import sleep

from matplotlib import pyplot as plt
from PIL import Image

from .script import jpg2pdf, png2jpg, dir_check, os_start_file, clear_temp


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

    def __init__(self, headless_driver):
        headless_driver.get('https://weread.qq.com/')
        headless_driver.implicitly_wait(5)
        self.driver = headless_driver

    def __enter__(self):
        return self

    def __exit__(self,*args):
        clear_temp('wrs-temp')

    def full_display(self):
        width = self.driver.execute_script(
            "return window.outerWidth")
        height = self.driver.execute_script(
            "return document.documentElement.scrollHeight")
        self.driver.set_window_size(width, height)

    def shot_full_displayed_element(self, element, file_name):
        self.full_display()
        element.screenshot(file_name)

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
        self.driver.find_element_by_css_selector(
            'button.navBar_link_Login').click()
        self.driver.find_element_by_css_selector(
            '.login_dialog_qrcode>img').screenshot('wrs-temp/login_qrcode.png')

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
        self.driver.find_element_by_css_selector('button.catalog').click()
        sleep(1)
        self.driver.find_element_by_css_selector(
            'li.chapterItem:nth-child(2)').click()

    def scan2pdf(self, book_url, save_at='.', binary_threshold=95, quality=90, show_output=True):
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
         - binary_threshold=95:
                threshold of scan binary
                二值化处理的阈值
         - quality=90:
                quality of scan pdf
                扫描PDF的质量
         - show_output=True:
                if show the output pdf file at the end of this method
                是否在该方法函数结束时展示生成的PDF文件

        :Usage:
            weread.scan2pdf('https://weread.qq.com/web/reader/a57325c05c8ed3a57224187kc81322c012c81e728d9d180')
        """
        print('Task launching...')

        # valid the url
        if not 'https://weread.qq.com/web/reader/' in book_url:
            raise Exception('WeRead.UrlError: Wrong url format.')

        # switch to target book url
        self.driver.get(book_url)
        print(f'navigate to {book_url}')
        sleep(2)

        # switch to target book's cover
        self.switch_to_context()

        # get the name of the book
        book_name = self.driver.find_element_by_css_selector(
            'span.readerTopBar_title_link').text
        print(f'preparing to scan "{book_name}"')

        # check the dir for future save
        dir_check(f'wrs-temp/{book_name}/context')

        # used to store jpg_name for pdf converting
        jpg_name_list = []

        while True:
            sleep(1)

            # loop to get chapter
            while True:
                chapter = self.driver.find_element_by_css_selector(
                    'span.readerTopBar_title_chapter').text
                if chapter:
                    break
                sleep(1)
            print(f'scanning chapter "{chapter}"')

            # locate the renderTargetContainer
            context = self.driver.find_element_by_css_selector(
                'div.renderTargetContainer')

            # context_scan2png
            png_name = f'wrs-temp/{book_name}/context/{chapter}'
            self.shot_full_displayed_element(context, f'{png_name}.png')

            # png2bin-jpg
            jpg_name = png2jpg(png_name, binary_threshold=95, quality=85)
            jpg_name_list.append(jpg_name)
            print(f'save chapter scan {jpg_name}')
            sleep(1)

            # go to next chapter
            try:
                self.driver.find_element_by_css_selector(
                    'button[title="下一章"]').click()
            except Exception:
                break

        # convert to pdf and save offline
        jpg2pdf(f'{save_at}/{book_name}', jpg_name_list)
        print('scanning finished.')
        if show_output:
            os_start_file(f'{save_at}/{book_name}.pdf')
