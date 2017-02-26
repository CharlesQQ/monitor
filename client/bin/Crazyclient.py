#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Charles Chang'

import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
print BASE_DIR

from core import main

if __name__ == '__main__':
    client = main.command_hander(sys.argv)