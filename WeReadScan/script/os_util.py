'''
os_util.py
Copyright 2020 by Algebra-FUN
ALL RIGHTS RESERVED.
'''

import os
import shutil


def dir_check(dir):
    try:
        os.makedirs(f'{os.getcwd()}/{dir}')
    except FileExistsError:
        pass

def os_start_file(file_name):
    os.system(f'start {file_name}')

def clear_temp(file_name):
    shutil.rmtree(file_name)
