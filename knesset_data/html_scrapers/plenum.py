# encoding: utf-8
import os
import re
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
from logging import getLogger
from itertools import chain
from knesset_data.exceptions import KnessetDataObjectException
from knesset_data.protocols.plenum import PlenumProtocolFile

logger = getLogger(__name__)


class PlenumMeetings(object):

    FULL_URL = "http://www.knesset.gov.il/plenum/heb/display_full.asp"
    PLENUM_URL = "http://www.knesset.gov.il/plenum/heb/plenum_queue.aspx"
    FILE_BASE_URL = "http://www.knesset.gov.il/plenum/heb/"
    WORDS_OF_THE_KNESSET = u"דברי הכנסת"
    WORDS_OF_THE_KNESSET_FULL = u"כל הפרוטוקול"
    DISCUSSIONS_ON_DATE = u"הדיונים בתאריך"

    def _get_committees_index_page(self, full):
        if full:
            url = self.FULL_URL
            encoding = 'iso_8859_8'
        else:
            url = self.PLENUM_URL
            # encoding='utf8'
            # the encoding of this page used to be utf-8 but looks like they reverted back to iso-8859-8
            encoding = 'iso_8859_8'
        logger.info('getting index page html from %s' % url)
        try:
            return unicode(self._read_index_page(url), encoding)
        except:
            logger.exception(u'could not fetch committees_index_page for url %s' % url)
            # send_chat_notification(__name__, "could not fetch committees index page", {'url': url})
            return ''

    def _read_index_page(self, url):
        return urllib2.urlopen(url).read()

    def _read_file(self, url):
        return urllib.urlopen(url).read()

    def _download_latest(self, full, skip_exceptions=False):
        html = self._get_committees_index_page(full)
        if not html:
            raise Exception("failed to fetch committees_index_page({})".format(full))
        soup = BeautifulSoup(html)
        if full:
            words_of_the_knesset = self.WORDS_OF_THE_KNESSET_FULL
        else:
            words_of_the_knesset = self.WORDS_OF_THE_KNESSET
        aelts = soup('a', text=words_of_the_knesset)
        for aelt in aelts:
            try:
                selt = aelt.findPrevious('span', text=re.compile(self.DISCUSSIONS_ON_DATE))
                href = aelt.parent.get('href')
                if href.startswith('http'):
                    url = href
                else:
                    url = self.FILE_BASE_URL + href
                filename = re.search(r"[^/]*$", url).group()
                logger.debug(filename)
                m = re.search(r"\((.*)/(.*)/(.*)\)", selt)
                if m is None:
                    selt = selt.findNext()
                    m = re.search(r"\((.*)/(.*)/(.*)\)", unicode(selt))
                if m is not None:
                    day = int(m.group(1))
                    mon = int(m.group(2))
                    year = int(m.group(3))
                    url = url.replace('/heb/..', '')
                    logger.debug(url)
                    yield self._get_plenum_meeting(url, self._read_file(url.replace('/heb/..', '')), year, mon, day)
            except Exception, e:
                if skip_exceptions:
                    yield KnessetDataObjectException(e)
                else:
                    raise e

    def _get_plenum_meeting(self, url, protocol, year, month, day):
        return PlenumMeeting(url, protocol, year, month, day)

    def download(self, skip_exceptions=False, sorted=False):
        res = chain(*[self._download_latest(full, skip_exceptions) for full in [True, False]])
        return res if not sorted else self.sort(res)

    @staticmethod
    def sort(plenum_meetings, descending=True):
        return sorted(plenum_meetings, key=lambda o: (o.year, o.month, o.day) if not isinstance(o, Exception) else None, reverse=descending)


class PlenumMeeting(object):

    def __init__(self, url, protocol, year, month, day):
        self.url = url
        self.protocol = PlenumProtocolFile.get_from_data(protocol)
        self.year = year
        self.month = month
        self.day = day
