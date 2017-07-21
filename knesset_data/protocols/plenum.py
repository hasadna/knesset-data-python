# -*- coding: utf-8 -*-
from tempfile import mkstemp
from datetime import datetime
from hebrew_numbers import gematria_to_int
from .utils import antiword, antixml
import re
from .base import BaseProtocolFile
from cached_property import cached_property
import six

# solve issues with unicode for python3/2
if six.PY2:
    def encode(a, *b):
        return a.encode(*b)
    def decode(a, *b):
        return a.decode(*b)
elif six.PY3:
    def encode(a, b):
        return a
    def decode(a, *b):
        return a

class PlenumProtocolFile(BaseProtocolFile):

    @classmethod
    def get_json_table_schema(cls):
        return {"fields": [{"name": "header_text", "type": "string"},
                           {"name": "meeting_num_heb", "type": "string"},
                           {"name": "knesset_num_heb", "type": "string"},
                           {"name": "knesset_num", "type": "integer"},
                           {"name": "booklet_num", "type": "integer"},
                           {"name": "booklet_num_heb", "type": "string"},
                           {"name": "booklet_meeting_num", "type": "integer"},
                           {"name": "booklet_meeting_num_heb", "type": "string"},
                           {"name": "day_heb", "type": "string"},
                           {"name": "date_string_heb", "type": "array", "description": "[day, month_name_heb, year]"},
                           {"name": "time_string", "type": "array", "description": "[hours, minutes]"},
                           {"name": "datetime", "type": "datetime"}]}

    @cached_property
    def header_text(self):
        # the decode / encode here ensures we don't cut in the middle of utf-8 chars
        z = decode(self.antiword_text[:1000], "utf-8", "ignore")
        return encode(z, "utf-8").replace("\n", "NL")

    @cached_property
    def meeting_num_heb(self):
        match = re.search(r'הישיבה ה(.*) של הכנסת', self.header_text)
        return match.groups()[0].strip() if match else None

    @cached_property
    def knesset_num_heb(self):
        match = re.search(r'של הכנסת ה(.+?(?=NL))', self.header_text)
        return match.groups()[0].strip() if match else None

    @cached_property
    def knesset_num(self):
        # TODO: write a proper algorythm (maybe add it to https://github.com/OriHoch/python-hebrew-numbers)
        return {
            'עשרים': 20,
            'עשרים ואחת': 21,
            'עשרים ושתיים': 22
        }[self.knesset_num_heb]

    @cached_property
    def booklet_num(self):
        return gematria_to_int(decode(self.booklet_num_heb, 'utf-8'))

    @cached_property
    def booklet_num_heb(self):
        match = re.search(r'חוברת (.+?(?=NL))', self.header_text)
        return match.groups()[0].strip() if match else None

    @cached_property
    def booklet_meeting_num(self):
        return gematria_to_int(decode(self.booklet_meeting_num_heb, 'utf-8'))

    @cached_property
    def booklet_meeting_num_heb(self):
        match = re.search(r'ישיבה (.+?(?=NL))', self.header_text)
        return match.groups()[0].strip() if match else None

    @cached_property
    def day_heb(self):
        match = re.search(r'יום ([קראטוןםפףךלחיעכגדשזסבהנמצתץ]*)', self.header_text)
        return match.groups()[0].strip() if match else None

    @cached_property
    def date_string_heb(self):
        match = re.search(r'\(([0-9]+) ב([קראטוןםפףךלחיעכגדשזסבהנמצתץ]+) ([0-9]+)\)', self.header_text)
        day, month_name_heb, year = match.groups()[0].strip(), match.groups()[1].strip(), match.groups()[2].strip()
        return day, month_name_heb, year

    @cached_property
    def time_string(self):
        match = re.search(r'שעה ([0-9]+):([0-9]+)(.+?(?=NL))', self.header_text)
        hours, minutes = match.groups()[0].strip(), match.groups()[1].strip()
        return hours, minutes

    @cached_property
    def datetime(self):
        day, month_name_heb, year = self.date_string_heb
        hours, minutes = self.time_string
        month_name_heb = {"מרס": "מרץ"}.get(month_name_heb, month_name_heb)
        months = ['ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'דצמבר']
        month = months.index(month_name_heb)+1
        return datetime(int(year), month, int(day), int(hours), int(minutes))
