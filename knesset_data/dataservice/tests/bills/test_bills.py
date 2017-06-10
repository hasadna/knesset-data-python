import datetime
import os
from collections import OrderedDict
from itertools import islice
from unittest import TestCase

from knesset_data.dataservice.bills import Bill


class MockBill(Bill):
    @classmethod
    def _get_response_content(cls, url, params, timeout, proxies):
        if url == "http://knesset.gov.il/Odata/ParliamentInfo.svc//KNS_Bill":
            filename = os.path.join(os.path.dirname(__file__), "ParliamentInfo.svc_KNS_Bill.xml")
            if os.environ.get("TEST_BILLS_DOWNLOAD_DATA", "") == "yes":
                content = super(MockBill, cls)._get_response_content(url, params, timeout, proxies)
                with open(filename, "w") as f:
                    f.write(content)
            else:
                with open(filename) as f:
                    content = f.read()
        else:
            raise Exception("invalid url: {}".format(url))
        return content


class BillsTestCase(TestCase):
    maxDiff = None

    def _listify_bills(self, bills):
        res = []
        for bill in bills:
            res.append(bill.all_field_values())
        return res

    def test(self):
        bills = self._listify_bills(list(islice(MockBill.get_all(), 2)))
        self.assertEqual(bills, [
            OrderedDict([
                ('id', 5), ('kns_num', 1), ('name',
                                            u'\u05d7\u05d5\u05e7 \u05e9\u05db\u05e8 \u05d7\u05d1\u05e8\u05d9 \u05d4\u05db\u05e0\u05e1\u05ea, \u05d4\u05ea\u05e9"\u05d8-1949'),
                ('type_id', 53), ('type_description', u'\u05de\u05de\u05e9\u05dc\u05ea\u05d9\u05ea'),
                ('private_num', None), ('committee_id', 377), ('status_id', 118), ('num', None),
                ('postponent_reason_id', None), ('postponent_reason_desc', None),
                ('public_date', datetime.datetime(1949, 6, 7, 0, 0)), ('magazine_num', 10), ('page_num', 41),
                ('is_continuation', None), ('sum_law', None), ('public_series_id', 6071),
                ('public_series_desc', 6071), ('public_series_first_call', None),
                ('last_update', datetime.datetime(2016, 3, 8, 11, 1, 1))]),
            OrderedDict([('id', 20), ('kns_num', 7), ('name',
                                                      u'\u05d7\u05d5\u05e7 \u05de\u05e7\u05e6\u05d5\u05e2\u05d5\u05ea \u05e8\u05e4\u05d5\u05d0\u05d9\u05d9\u05dd (\u05d0\u05d2\u05e8\u05d5\u05ea), \u05d4\u05ea\u05e9\u05dc"\u05d0-1971'),
                         ('type_id', 53), ('type_description', u'\u05de\u05de\u05e9\u05dc\u05ea\u05d9\u05ea'),
                         ('private_num', None), ('committee_id', 280), ('status_id', 118), ('num', 887),
                         ('postponent_reason_id', None), ('postponent_reason_desc', None),
                         ('public_date', datetime.datetime(1971, 4, 7, 0, 0)), ('magazine_num', 618), ('page_num', 68),
                         ('is_continuation', None), ('sum_law', None), ('public_series_id', 6071),
                         ('public_series_desc', 6071), ('public_series_first_call', None),
                         ('last_update', datetime.datetime(2016, 3, 8, 11, 0, 56))])
        ])
