'''
png2pdf.py
Copyright 2020 by Algebra-FUN
ALL RIGHTS RESERVED.
'''


import cv2
import img2pdf
import numpy as np
from PIL import Image


def png2jpg(file_name, binary_threshold=95, quality=95):
    img = cv2.imdecode(np.fromfile(f'{file_name}.png', dtype=np.uint8), -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval, dst = cv2.threshold(gray, binary_threshold, 255, cv2.THRESH_BINARY)
    binim = cv2.bitwise_not(dst)
    Image.fromarray(binim).save(f'{file_name}.jpg', quality=quality)
    return f'{file_name}.jpg'


def jpg2pdf(file_name, jpg_name_list):
    file_name = f'{file_name}.pdf'
    with open(file_name, 'wb') as f:
        pdf_bytes = img2pdf.convert(jpg_name_list)
        f.write(pdf_bytes)
        print(f'Converted to pdf at {file_name}')
