#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: 文件.py
# Mail: 1957875073@qq.com
# Created Time:  2022-4-25 10:17:34
# Description: 有关 文件 的自动化操作
#############################################
import pypistats
from pprint import pprint

# Call the API
def pip_times(package_name):
    print(pypistats.recent(package_name))