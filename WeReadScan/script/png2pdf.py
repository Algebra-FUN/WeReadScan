'''
png2pdf.py
Copyright 2020 by Algebra-FUN
ALL RIGHTS RESERVED.
'''


import cv2
import numpy as np
from PIL import Image


def png2bmp(file_path, binary_threshold=200):
    img = cv2.imdecode(np.fromfile(f'{file_path}.png', dtype=np.uint8), -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    retval, dst = cv2.threshold(gray, binary_threshold, 255, cv2.THRESH_BINARY)
    return Image.fromarray(dst)


def img2pdf(file_name, jpg_name_list, binary_threshold=200, quality=100):
    image_list = [png2bmp(path, binary_threshold=binary_threshold)
                  for path in jpg_name_list]
    image_list[0].save(f'{file_name}.pdf', save_all=True,
                       append_images=image_list[1:], resolution=quality)
