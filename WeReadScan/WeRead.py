'''
WeRead.py
Copyright 2020 by Algebra-FUN
ALL RIGHTS RESERVED.
'''
from matplotlib import pyplot as plt
from PIL import Image
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver

from .script import img2pdf, dir_check, os_start_file, clear_temp, addBookmark2pdf

from time import sleep
import re
import time

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

    def shot_full_canvas_context(self, file_name):
        renderTargetContainer = self.S('.renderTargetContainer')
        height = renderTargetContainer.get_property('offsetHeight')
        height += renderTargetContainer.get_property('offsetTop')
        width = self.driver.execute_script("return window.innerWidth")
       
        # check all image loaded
        self.check_all_image_loaded(width, height)

        content = self.S('.app_content')
        content.screenshot(file_name)

    def check_all_image_loaded(self, width, height, frequency=10, max_wait_duration=15, retry_once=True):
        """
        check if all image is loaded.

        检查图书Image是否全部加载完毕.
        """
        interval = 1/frequency

        self.driver.set_window_size(width, height)
        self.driver.execute_script(f"window.scrollTo(0, {height})")
        sleep(interval)
        self.driver.execute_script(f"window.scrollTo(0, 0)")

        try:
            WebDriverWait(self.driver, 3).until(
                lambda driver: driver.find_elements_by_css_selector('img.wr_absolute'))
        except Exception:
            return False

        if self.debug_mode:
            print(f"Total img: {len(self.driver.find_elements_by_css_selector('img.wr_absolute'))}")

        for _ in range(frequency * max_wait_duration):
            unloadedImg = len(self.driver.find_elements_by_css_selector('img.wr_pendingLoading'))
            if self.debug_mode:
                print(f"Remaining unloaded img: {unloadedImg}")
            if unloadedImg == 0:
                return True            
            sleep(interval)

        if retry_once:
            self.driver.set_window_size(width, 1000)
            self.driver.refresh()
            for unloadImg in self.driver.find_elements_by_css_selector('img.wr_pendingLoading'):
                if self.debug_mode:
                    print(f"Retry to scroll to: {unloadImg.get_property('offsetTop')}")
                self.driver.execute_script(f"window.scrollTo(0, {unloadImg.get_property('offsetTop')})")
                sleep(interval)
        for _ in range(frequency * max_wait_duration):
            unloadedImg = len(self.driver.find_elements_by_css_selector('img.wr_pendingLoading'))
            if self.debug_mode:
                print(f"Still unloaded img: {unloadedImg}")
            if unloadedImg == 0:
                self.driver.execute_script(f"window.scrollTo(0, 0)")
                self.driver.set_window_size(width, height)
                return True            
            sleep(interval)
        self.driver.execute_script(f"window.scrollTo(0, 0)")
        self.driver.set_window_size(width, height)
        if self.debug_mode:
            print(f"Fail to load all pictures, remaining unloaded pic: {unloadedImg}")
        return False

    def remove_header_and_split_long_page(self, png_name):
        split_pngs = []
        img = Image.open(f'{png_name}.png')
        renderTargetContainer = self.S('.renderTargetContainer')
        header_height = renderTargetContainer.get_property('offsetTop')
        # 分割目标为小于20000像素，应为AdobeReader单页图片醉倒显示为20000高度，否则会截断。同时，用PIL保存PDF时，中间过程会转成JPEG，此时图片长度超过65500会报错
        # 微信读书的章节内容页面一般的布局为1-2个最大大约为4000高度的canvas，如果内容超过2个canvas的容量，则后续内容为单个字符的span组成。图片则一律为单个img标签
        # 由于2个canvas的最大高度最大大约也就是8000出头，远小于20000，所以在确定分割位置是，只考虑span和img
        last_split_offset = header_height
        img_index = 1
        if last_split_offset + 20000 < img.height:
            if self.debug_mode:
                print('Page is too long and need to split')
                print(f'Total characters and images: {len(renderTargetContainer.find_elements_by_css_selector("span,img"))}')
                print(f'Start calculating rows at: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
            row_info = {}        
            for x in renderTargetContainer.find_elements_by_css_selector("span,img"):
                if not row_info.__contains__(x.get_property('offsetTop') + header_height):
                    row_info[x.get_property('offsetTop') + header_height] = x.get_property('offsetHeight')
            row_offsets = list(row_info.keys())
            row_offsets.sort()
            if self.debug_mode:
                print(f'Finish calculating rows at: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
            start_index = 0
            end_index = len(row_offsets) - 1
            while last_split_offset + 20000 < img.height:
                split_row_index = self.binarySearch(row_offsets, start_index, end_index, last_split_offset + 20000)
                start_index = split_row_index + 1
                # calculate the split height
                split_row_top_offset = row_offsets[split_row_index]
                last_row_top_offset = row_offsets[split_row_index - 1]
                last_row_height = row_info[last_row_top_offset]
                row_space = split_row_top_offset - last_row_top_offset - last_row_height
                split_offset = split_row_top_offset - int(row_space / 2)

                split_img = img.crop((0, last_split_offset, img.width, split_offset))
                split_img.save(f"{png_name}_{img_index}.png")
                last_split_offset = split_offset
                split_pngs.append((f"{png_name}_{img_index}", split_offset - last_split_offset))
                img_index = img_index + 1

        last_img = img.crop((0, last_split_offset, img.width, img.height))
        last_img.save(f"{png_name}_{img_index}.png")
        split_pngs.append((f"{png_name}_{img_index}", img.height - last_split_offset))
        return split_pngs

    # return largest element in arr, which is less then x
    def binarySearch(self, arr, l, r, x):
        if arr[r] <= x:
            return r;
        if arr[l] > x:
            return -1
        if r > l:    
            if r == l + 1:
                return l
            mid = int(l + (r - l)/2)
            if arr[mid] == x: 
                return mid 
            elif arr[mid] > x: 
                return self.binarySearch(arr, l, mid-1, x) 
            else: 
                return self.binarySearch(arr, mid, r, x) 
        else: 
            return r

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

        # wait for QRCode Scan
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

    def init_toc_and_swich_to_front_page(self):
        toc = []
        self.S('button.catalog').click()
        sleep(1)
        chapterItem_links = self.driver.find_elements_by_css_selector('div.chapterItem_link')
        for i in range(1, len(chapterItem_links)): 
            chap_level = int(re.match( r'.*chapterItem_level(\d+)', chapterItem_links[i].get_attribute('class'), re.M|re.I).group(1))
            chap_name = chapterItem_links[i].text
            toc.append((chap_name, chap_level, 0, 0))
        self.S('li.chapterItem:nth-child(2)').click()
        return toc

    def refresh_toc_per_chapter(self, chapter_name, toc, start_page, start_page_height):
        try:
            chapter_idx = list(zip(*toc))[0].index(chapter_name)
            for i in range(chapter_idx, len(toc)):
                toc[i] = (toc[i][0], toc[i][1], start_page, start_page_height)
            return flag
        except:
            return toc

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

        if len(self.driver.find_elements_by_xpath("//div[@class='vue-slider-mark vue-slider-mark-active']")) != font_size_index:
            self.S(f'.vue-slider-mark:nth-child({font_size_index})').click()
        self.S('.app_content').click()

    def is_element_exist(self, element):
        flag = True
        try:
            self.driver.find_element_by_css_selector(element)
            return flag
        except:
            flag = False
            return flag

    def turn_light_on(self):
        sleep(1)
        if self.is_element_exist('button.readerControls_item.white'):
            self.S('button.readerControls_item.white').click()

    def scan2pdf(self, book_url, save_at='.', binary_threshold=200, keep_color=False, show_output=True, font_size_index=1):
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
                threshold of scan binary, only used in black and white mode
                二值化处理的阈值
         - keep_color=Flase:
                If True will keep doc in its original color, else will convert doc to black and white
                是否保持原色，或者转换成黑白模式
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
        print(f'Scanning start at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')

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

        # init toc and switch to target book's cover       
        toc = self.init_toc_and_swich_to_front_page()

        # get the name of the book
        book_name = self.S('span.readerTopBar_title_link').text
        print(f'preparing to scan "{book_name}"')

        # check the dir for future save
        dir_check(f'wrs-temp/{book_name}/context')

        # used to store png_name for pdf converting
        png_name_list = []

        while True:
            sleep(0.1)

            # get chapter
            chapter = self.S('span.readerTopBar_title_chapter').text
            print(f'scanning chapter "{chapter}"')

            # context_scan2png
            png_name = f'wrs-temp/{book_name}/context/{chapter}'
            self.shot_full_canvas_context(f'{png_name}.png')

            # remove header and split long page
            split_pngs = self.remove_header_and_split_long_page(png_name)

            # store toc
            toc = self.refresh_toc_per_chapter(chapter, toc, len(png_name_list), list(zip(*split_pngs))[1][0])

            png_name_list.extend(list(zip(*split_pngs))[0])
            print(f'save chapter scan {png_name}')

            # go to next chapter
            try:
                self.S('button[title="下一章"]').click()
            except Exception:
                break

        print('pdf converting...')

        # convert to pdf and save offline
        img2pdf(f'{save_at}/{book_name}', png_name_list, binary_threshold, keep_color)
        if self.debug_mode:
            print(f"Book ToC: {toc}")
        addBookmark2pdf(f'{save_at}/{book_name}', toc)
        print(f'Scanning finished at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
        if show_output:
            os_start_file(f'{save_at}/{book_name}_带书签.pdf')
        


