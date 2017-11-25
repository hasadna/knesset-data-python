# -*- coding: utf-8 -*-
import logging
from .base import BaseProtocolFile
from cached_property import cached_property
import re
import contextlib
from .utils import fix_hyphens, get_people_list, get_speaker_list
import six

# solve issues with unicode for python3/2
if six.PY2:
    def decode(a, b):
        return a.decode(b)
    unicode = unicode
elif six.PY3:
    def decode(a, b):
        return a
    unicode = str

logger = logging.getLogger(__name__)


class CommitteeMeetingProtocolPart(object):

    def __init__(self, header, body):
        self.header = header
        self.body = body

    def all_field_values(self):
        return {
            'header': self.header,
            'body': self.body
        }


class CommitteeMeetingProtocol(BaseProtocolFile):

    not_header = re.compile(decode(r'(^אני )|((אלה|אלו|יבוא|מאלה|ייאמר|אומר|אומרת|נאמר|כך|הבאים|הבאות):$)|(\(.\))|(\(\d+\))|(\d\.)', 'utf8'))

    def _is_legitimate_header(self, line):
        """Returns true if 'line' looks like something should be a protocol part header"""
        if re.match(r'^\<.*\>\W*$', line):  # this is a <...> line.
            return True
        if not (line.strip().endswith(':')) or len(line) > 50 or self.not_header.search(line):
            return False
        return True

    @cached_property
    def text(self):
        if self._file_type == 'text':
            return self._file_data
        else:
            text = decode(self.antiword_text, 'utf-8')
            tmp = text.split('OMNITECH')
            if len(tmp)==2 and len(tmp[0]) < 40:
                text = tmp[1]
            text = text.strip()
            return text

    def _get_section_text(self, section_lines):
        section_text = '\n'.join(section_lines).strip()
        return section_text.replace(u"\n\n–\n\n", u' - ')

    @cached_property
    def parts(self):
        parts = []
        # break the protocol to its parts
        # first, fix places where the colon is in the beginning of next line
        # (move it to the end of the correct line)
        protocol_text = []
        for line in re.sub("[ ]+", " ", self.text).split('\n'):
            # if re.match(r'^\<.*\>\W*$',line): # this line start and ends with
            #                                  # <...>. need to remove it.
            #    line = line[1:-1]
            if line.startswith(':'):
                protocol_text[-1] += ':'
                protocol_text.append(line[1:])
            else:
                protocol_text.append(line)

        i = 1
        section = []
        header = ''

        # now create the sections
        for line in protocol_text:
            if self._is_legitimate_header(line):
                if (i > 1) or (section):
                    parts.append(CommitteeMeetingProtocolPart(header.strip(), self._get_section_text(section)))
                i += 1
                header = re.sub('[\>:]+$', '', re.sub('^[\< ]+', '', line))
                section = []
            else:
                section.append(line)

        # don't forget the last section
        parts.append(CommitteeMeetingProtocolPart(header.strip(), self._get_section_text(section)))
        return parts

    def find_attending_members(self, mk_names):
        """
        iterates over the given list of mk names
        returns a list of mks names which attended the meeting
        this is done by parsing the protocol text, so it's not very accurate
        """
        attended_mk_names = []
        if isinstance(self.text, (str, unicode)) and self.text:
            result = re.search(
                decode("חברי הו?ועד(.*?)(\n[^\n]*(ייעוץ|יועץ|רישום|רש(מים|מות|מו|מ|מת|ם|מה)|קצר(נים|ניות|ן|נית))[\s|:])", 
                    'utf8'), self.text, re.DOTALL)
            if not result:
                return attended_mk_names
            r = result.group(1)
            s = r.split('\n')
            for (i, name) in enumerate(mk_names):
                for s0 in s:
                    if s0.find(name.strip()) >= 0 and name not in attended_mk_names:
                        attended_mk_names.append(name)
        return attended_mk_names

    @cached_property
    def attendees(self):
        """
        finds the people that attended the comittee meeting
        will also try to parse their role and who it represents
        """
        if isinstance(self.text, (str, unicode)) and self.text:
            text = fix_hyphens(self.text)
            members = CommitteeMeetingProtocol._get_committee_members(text)
            invitees = CommitteeMeetingProtocol._get_invitees(text)
            legal_advisors = CommitteeMeetingProtocol._get_legal_advisors(text)
            manager = CommitteeMeetingProtocol._get_committee_manager(text)

            attendees = {}
            attendees["mks"] = members
            attendees["invitees"] = invitees
            attendees["legal_advisors"] = legal_advisors
            attendees["manager"] = manager

            return attendees

        return None

    @cached_property
    def speakers(self):
        """
        finds the people who spoke in this committee meeting
        """
        if isinstance(self.text, (str, unicode)) and self.text:
            return get_speaker_list(self.text)

        return []

    @staticmethod
    def _get_committee_members(text):
        """
        returns a list of mks names which attended the meeting, from the protocol text
        """
        results = get_people_list(text,u'חברי הכנסת:')
        results.extend(get_people_list(text,u"חברי הוועדה:"))
        return results
        

    @staticmethod
    def _get_invitees(text):
        """
        returns a list of the invitees which attended the meeting, from the protocol text
        """
        invitees = []
        invitees_list = get_people_list(text,u"מוזמנים:")
        for invitee_line in invitees_list:
            invitee = {}
            
            if u"–" in invitee_line:
                line_elements = invitee_line.split(u"–")
                invitee["name"] = line_elements[0]
                invitee["role"] = line_elements[1]

            else:
                invitee["name"] = invitee_line

            invitees.append(invitee)

        return invitees

    @staticmethod
    def _get_legal_advisors(text):
        return get_people_list(text,u"ייעוץ משפטי:")

    @staticmethod
    def _get_committee_manager(text):
        results = get_people_list(text,u"מנהל/ת הוועדה:")
        results.extend(get_people_list(text,u"מנהלת הוועדה:"))
        results.extend(get_people_list(text,u"מנהל הוועדה:"))
        return results

    @classmethod
    @contextlib.contextmanager
    def get_from_text(cls, text):
        with cls._get_from('text', text) as p: yield p


# TODO: find out if the rtf protocol code is needed in some cases, currently, we don't seem to get rtf files form knesset
# @classmethod
# def handle_rtf_protocol(cls, file_str):
#     # looks like this is only relevant for old meetings
#     # this code is copied from Open-Knesset, it should work, but should keep this error until it's tested
#     raise NotImplementedError()
#     doc = Rtf15Reader.read(file_str)
#     text = []
#     attended_list = False
#     for paragraph in doc.content:
#         for sentence in paragraph.content:
#             if 'bold' in sentence.properties and attended_list:
#                 attended_list = False
#                 text.append('')
#             if 'מוזמנים'.decode('utf8') in sentence.content[0] and 'bold' in sentence.properties:
#                 attended_list = True
#             text.append(sentence.content[0])
#     all_text = '\n'.join(text)
#     return re.sub(r'\n:\n',r':\n',all_text)

# TODO: find out if rtf protocol code is needed in some cases, currently, we don't seem to get rtf files form knesset
# url = str(self.url)
# logger.debug('get_committee_protocol_text. url=%s' % url)
# if url.find('html') >= 0:
#     url = url.replace('html','rtf')
# file_str = StringIO()
# count = 0
# flag = True
# while count<10 and flag:
#     try:
#         file_str.write(self._get_url_contents(url))
#         flag = False
#     except Exception:
#         count += 1
# if flag:
#     logger.error("can't open url %s. tried %d times" % (url, count))
# if url.find(".rtf") >= 0:
#     self._cached_text = self.handle_rtf_protocol(file_str)
