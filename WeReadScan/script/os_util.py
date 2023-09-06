'''
os_util.py
Copyright 2023 by Algebra-FUN
ALL RIGHTS RESERVED.
'''

import os
import shutil
import sys


def dir_check(dir):
    try:
        os.makedirs(f'{os.getcwd()}/{dir}')
    except FileExistsError:
        pass

def os_start_file(file_name):
    commands = {
        'linux1' : 'xdg-open',
        'linux2' : 'xdg-open',
        'darwin' : 'open',
        'win32' : 'start'
    }
    if sys.platform in commands.keys():
        command = commands[sys.platform]
        os.system(f'{command} "{file_name}"')

def clear_temp(file_name):
    shutil.rmtree(file_name)
