#!/usr/bin/env python
# 
#coding: utf-8
import _env  # noqa
import MySQLdb as sqldb
from datetime import datetime
from controller.send_email import VirtualEmail, SimpleGoogleAds 
from config import ProductionConfig


conn = sqldb.connect(
    host=ProductionConfig.MYSQL_HOST,
    port=ProductionConfig.MYSQL_PORT,
    user=ProductionConfig.MYSQL_USER,
    passwd=ProductionConfig.MYSQL_PASS,
    db=ProductionConfig.MYSQL_DB
)

class ReportEmail(VirtualEmail, SimpleGoogleAds):

    def __init__(self, **kwds):
        super(ReportEmail, self).__init__(**kwds)

    def __del__(self):
        return conn.close()

    def query(self, spec):
        _cursor = conn.cursor(cursorclass=sqldb.cursors.DictCursor)
        try:
            _cursor.execute(spec)
            _cursor.scroll(0, "absolute")
        finally:
            _cursor.close()
        return _cursor

    def get_offers(self):
        _t = datetime.now().strftime('%H:%M')
        _t = '01:00'  # test
        QUERY_STRING = "SELECT id, status FROM offer WHERE email_time = '%s'" % (_t)
        offers = self.query(QUERY_STRING)

    def main(self):
        # self.get_offers()
        ids = ['548-123-9135', '296-153-6464', '468-594-0001']
        for customer_id in ids:
            self.get_report_from_google(customer_id)
        self._send()

if __name__ == '__main__':
    r = ReportEmail(title='22')
    r.main()
