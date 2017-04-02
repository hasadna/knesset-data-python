from unittest import TestCase
import os
from knesset_data.utils.reblaze import is_reblaze_content


class ReblazeTestCase(TestCase):

    def test(self):
        self.assertTrue(is_reblaze_content(open(os.path.join(os.path.dirname(__file__), "reblaze_response.html")).read()))
