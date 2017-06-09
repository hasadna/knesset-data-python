# -*- coding: utf-8 -*-
from datetime import datetime
from unittest import TestCase

from knesset_data.dataservice.bill_split import BillSplit
from knesset_data.dataservice.tests.test_utils import execute_from_local_file


class TestBillSplit(TestCase):
    def test(self):
        bill_split = execute_from_local_file(BillSplit, "ParliamentInfo.svc_KNS_BillSplit.xml", 2)
        self.assertEqual(bill_split.id, 2)
        self.assertEqual(bill_split.bill_id, 258446)
        self.assertEqual(bill_split.split_bill_id, 262882)
        self.assertEqual(bill_split.name, u'הצעת חוק הבלו על הדלק (תיקון), התשס"ח-2007')
        self.assertEqual(bill_split.last_update, datetime(2015, 3, 20, 12, 3, 32))
