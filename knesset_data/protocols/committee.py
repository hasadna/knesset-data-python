# -*- coding: utf-8 -*-
import logging
from .base import BaseProtocolFile
from cached_property import cached_property
import re
import contextlib
from .utils import fix_hyphens, get_people_list, get_speaker_list, get_people_list_all
import six
import os

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

    def _parse_header(self, line):
        if re.match(r'^<.*>\W*$', line):  # this is a <...> line.
            return re.sub('[>:]+$', '', re.sub('^[< ]+', '', line)).strip()
        elif self.not_header.search(line):
            return False
        elif len(line) <= 50 and line.strip().endswith(':'):
            return line.strip()[:-1].strip()
        else:
            splitline = line.split(':')
            # print(splitline)
            if len(splitline) == 2 and 5 < len(splitline[0]) <= 50 and (splitline[1].startswith('\t') or splitline[1].startswith(' ')):
                return splitline[0].strip(), splitline[1].strip()
        return False

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
        section_text = section_text.replace(u"\n\n–\n\n", u' - ')
        section_text = section_text.replace(u"\n\t–\n\t", u' - ')
        section_text = section_text.replace(u"\n\n\t", u'\n\n')
        return section_text

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

        def add_part(_header, _section):
            _header = _header.strip().strip('<>')
            parts.append(CommitteeMeetingProtocolPart(_header, self._get_section_text(_section)))

        # now create the sections
        for line in protocol_text:
            line = re.sub(r'(<<\W[^>]*\W>>)', "", line)
            # print('-------', line)
            parsed_header = self._parse_header(line)
            # print('=======', parsed_header)
            if parsed_header:
                if isinstance(parsed_header, tuple):
                    line = parsed_header[1]
                    parsed_header = parsed_header[0]
                else:
                    line = None
                if (i > 1) or (section):
                    add_part(header, section)
                i += 1
                header = parsed_header
                section = []
                if line is not None:
                    section.append(line)
            else:
                section.append(line)

        # don't forget the last section
        add_part(header, section)
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
            financial_advisors = CommitteeMeetingProtocol._get_financial_advisors(text)

            attendees = {}
            attendees["mks"] = members
            attendees["invitees"] = invitees
            attendees["legal_advisors"] = legal_advisors
            attendees["manager"] = manager
            attendees['financial_advisors'] = financial_advisors

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
        invitees_list = get_people_list(text,u"מוזמנים:", no_limit=True)
        for invitee_line in invitees_list:
            invitee = {}
            
            if u"–" in invitee_line:
                line_elements = invitee_line.split(u"–")
                invitee["name"] = line_elements[0]
                invitee["role"] = line_elements[1]

            else:
                invitee["name"] = invitee_line

            invitee['name'] = invitee['name'].strip()
            if invitee['name']:
                if 'role' in invitee:
                    invitee['role'] = invitee['role'].strip()
                    if not invitee['role']:
                        del invitee['role']
                invitees.append(invitee)

        return invitees

    @staticmethod
    def _get_advisor_texts():
        return ['ייעוץ', 'יעוץ', 'יועץ', 'יועץ/ת', 'יועצת']

    @staticmethod
    def _get_legal_advisors(text):
        tokens = set()
        for legal in ['משפטי', 'משפטית']:
            for advisor in CommitteeMeetingProtocol._get_advisor_texts():
                tokens.add('{} {}:'.format(advisor, legal))
        return get_people_list_all(text, tokens)

    @staticmethod
    def _get_financial_advisors(text):
        tokens = set()
        for financial in ['כלכלית', 'כלכלי']:
            for advisor in CommitteeMeetingProtocol._get_advisor_texts():
                tokens.add('{} {}:'.format(advisor, financial))
        return get_people_list_all(text, tokens)

    @staticmethod
    def _get_committee_manager(text):
        tokens = set()
        for committee in ['הוועדה', 'הועדה']:
            for manager in ['מנהל/ת', 'מנהלת', 'מנהל']:
                tokens.add('{} {}:'.format(manager, committee))
        return get_people_list_all(text, tokens)

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
