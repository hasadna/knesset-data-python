from unittest import TestCase
from ..open_knesset import get_all_mk_names
from ..mocks import MOCK_OPEN_KNESSET_GET_ALL_MK_NAMES_RESPONSE
import os
from copy import deepcopy


class OpenKnessetTestCase(TestCase):

    def test(self):
        # TODO: switch to env_conditional_mock function when PR #9 is merged
        if os.environ.get("NO_MOCKS", "") == "1":
            all_mk_names = get_all_mk_names()
        else:
            all_mk_names = MOCK_OPEN_KNESSET_GET_ALL_MK_NAMES_RESPONSE
        mks, mk_names = all_mk_names
        expected_mks, expected_mk_names = MOCK_OPEN_KNESSET_GET_ALL_MK_NAMES_RESPONSE
        self.assertEqual(mks, expected_mks)
        self.assertEqual(mk_names, expected_mk_names)
