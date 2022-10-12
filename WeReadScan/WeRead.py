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

from .script import img2pdf, dir_check, os_start_file, clear_temp, escape

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

    def __init__(self, headless_driver: WebDriver, patience=30, debug=False):
        headless_driver.get('https://weread.qq.com/')
        headless_driver.implicitly_wait(5)
        self.driver: WebDriver = headless_driver
        self.patience = patience
        self.debug_mode = debug

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self.debug_mode:
            clear_temp('wrs-temp')

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

    def check_all_image_loaded(self, frequency=10, max_wait_duration=30):
        """
        check if all image is loaded.

        检查图书Image是否全部加载完毕.
        """
        interval = 1/frequency

        try:
            img_unloaded = WebDriverWait(self.driver, 3).until(
                lambda driver: driver.find_elements(By.CSS_SELECTOR, 'img.wr_absolute'))
        except Exception:
            return False

        for _ in range(frequency*max_wait_duration):
            sleep(interval)
            for img in img_unloaded:
                if img.get_property('complete'):
                    img_unloaded.remove(img)
            if not len(img_unloaded):
                self.debug_mode and print('all image is loaded!')
                return True
        return False

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

    def set_font_size(self, font_size_index=1):
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

    def scan2pdf(self, book_url, save_at='.', binary_threshold=200, quality=100, show_output=True, font_size_index=1):
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
        book_name = escape(self.S('span.readerTopBar_title_link').text)
        print(f'preparing to scan "{book_name}"')

        # check the dir for future save
        dir_check(f'wrs-temp/{book_name}/context')

        # used to store png_name for pdf converting
        png_name_list = []

        page = 1

        while True:
            sleep(1)

            # get chapter
            chapter = escape(self.S('span.readerTopBar_title_chapter').text)
            print(f'scanning chapter "{chapter}"')

            # locate the renderTargetContent
            context = self.S('div.app_content')

            # check all image loaded
            self.check_all_image_loaded()

            # context_scan2png
            png_name = f'wrs-temp/{book_name}/context/{chapter}_{page}'
            self.shot_full_canvas_context(f'{png_name}.png')

            png_name_list.append(png_name)
            print(f'save chapter scan {png_name}')

            # find next page or chapter button
            try:
                readerFooter = self.S(
                    '.readerFooter_button,.readerFooter_ending')
            except Exception:
                break

            readerFooterClass = readerFooter.get_attribute('class')

            # quick ending
            if 'ending' in readerFooterClass:
                break

            next_btn_text = readerFooter.text.strip()

            if next_btn_text == "下一页":
                print("go to next page")
                page += 1
            elif next_btn_text == "下一章":
                print("go to next chapter")
                page = 1
            else:
                raise Exception("Unexpected Exception")

            # go to next page or chapter
            readerFooter.click()

        print('pdf converting...')

        # convert to pdf and save offline
        img2pdf(f'{save_at}/{book_name}', png_name_list,
                binary_threshold=binary_threshold, quality=quality)
        print('scanning finished.')
        if show_output:
            os_start_file(f'{save_at}/{book_name}.pdf')
