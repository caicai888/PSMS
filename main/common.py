#!/usr/bin/env python
# *_ coding:utf-8 _*_


import csv
import sys
import os
import config
import traceback

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




