#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Charles Chang'
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")

    from app01.backends.management import execute_from_command_line

    execute_from_command_line(sys.argv)