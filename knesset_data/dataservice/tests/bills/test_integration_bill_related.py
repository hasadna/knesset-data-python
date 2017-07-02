# -*- coding: utf-8 -*-
from unittest import TestCase

from knesset_data.utils.testutils import data_dependant_test

from knesset_data.dataservice.bill_history_initiator import BillHistoryInitiator
from knesset_data.dataservice.bill_initiator import BillInitiator
from knesset_data.dataservice.bill_name import BillName
from knesset_data.dataservice.bill_split import BillSplit
from knesset_data.dataservice.bill_union import BillUnion


@data_dependant_test()
class TestIntegrationBillRelated(TestCase):
    def test_bill_initiator(self):
        bill_initiator = BillInitiator.get(2)
        self.assertIsNotNone(bill_initiator)

    def test_bill_history_initiator(self):
        res = BillHistoryInitiator.get(2)
        self.assertIsNotNone(res)

    def test_bill_name(self):
        res = BillName.get(2)
        self.assertIsNotNone(res)

    def test_bill_split(self):
        res = BillSplit.get(2)
        self.assertIsNotNone(res)

    def test_bill_union(self):
        res = BillUnion.get(2)
        self.assertIsNotNone(res)
