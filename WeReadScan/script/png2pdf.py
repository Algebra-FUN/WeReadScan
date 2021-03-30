'''
png2pdf.py
Copyright 2020 by Algebra-FUN
ALL RIGHTS RESERVED.
'''


import cv2
import numpy as np
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter


def png2bmp(file_name, binary_threshold, keep_color):
    if keep_color:
        img = Image.open(f'{file_name}.png')
        if len(img.split()) == 4:
            r, g, b, a = img.split()
            img = Image.merge("RGB", (r, g, b))
        return img.convert('RGB')
    else:
        img = cv2.imdecode(np.fromfile(f'{file_name}.png', dtype=np.uint8), -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        retval, dst = cv2.threshold(gray, binary_threshold, 255, cv2.THRESH_BINARY)
        return Image.fromarray(dst)

def img2pdf(file_name, jpg_name_list, binary_threshold = 200, keep_color = False):
    image_list = [png2bmp(path, binary_threshold, keep_color) for path in jpg_name_list]
    image_list[0].save(f'{file_name}.pdf', save_all=True,
                       append_images=image_list[1:], resolution=100)

def addBookmark2pdf(file_name, toc):
    book = PdfFileReader(f'{file_name}.pdf')
    pdf = PdfFileWriter()
    pdf.cloneDocumentFromReader(book)   
    chapter_stack = []
    for item in toc:
        if item[1] <= 1:
            bookmarkRef = pdf.addBookmark(item[0], item[2], None, None, False, False, '/FitH', item[3])
        else:
            bookmarkRef = pdf.addBookmark(item[0], item[2], chapter_stack[item[1] - 2], None, False, False, '/FitH', item[3])
        if len(chapter_stack) < item[1]:
            chapter_stack.append(bookmarkRef)
        else:
            chapter_stack[item[1] - 1] = bookmarkRef; 
    with open(f'{file_name}_带书签.pdf','wb') as fout:
        pdf.write(fout)
