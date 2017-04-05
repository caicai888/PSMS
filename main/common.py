#!/usr/bin/env python
# *_ coding:utf-8 _*_

import csv
import sys
import os
import config
import traceback
from collections import namedtuple
import shutil
import socket, struct
import getopt
import logging
import time, datetime

reload(sys)
sys.setdefaultencoding('utf8')

class csvHandler(object):
    def __init__(self, filename, contents, headers):
        self.contents = contents
        self.headers = headers
        self.filename = filename

    def writeCsv(self):
        with open(self.filename, 'wb') as fp:
            f_csv = csv.DictWriter(fp, self.headers)
            f_csv.writeheader()
            f_csv.writerows(self.contents)

    def readCsv(self):
        with open(self.filename) as fp:
            f_csv = csv.DictReader(fp)
            for row in f_csv:
                pass

    def dirDetect(self):
        csv_dir = '/'.join(config.template_cvs_config['csv_store_path'].split('/')[:-1])
        if not os.path.exists(csv_dir):
            os.makedirs(csv_dir)


class Pager(object):
    def __init__(self, g_list, current_page, total, limit):
        self.current_page = int(current_page)
        self.total = int(total)
        self.limit = int(limit)
        self.g_list = g_list

    # 把方法伪造成属性(1)
    @property
    def start(self):
        return (self.current_page - 1) * self.limit

    @property
    def end(self):
        return self.current_page * self.limit

    @property
    def totalpage(self):
        all_page, div = divmod(self.total, self.limit)
        if div > 0:
            all_page += 1
        return all_page


