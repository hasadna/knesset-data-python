from future.standard_library import install_aliases
install_aliases()
from urllib.request import urlopen
import re

from logging import getLogger

logger = getLogger(__name__)


class HtmlVote(object):
    def __init__(self, page):
        self.page = page

    @property
    def member_votes(self):
        """
         Returns a tuple of (member_id, vote_result_code) describing the vote found in page, where:
         member_id = link to dataservice member id
         vote_result_code = "voted for"|"voted against"|"abstain"|"did not vote" - matching the codes in dataservice.votes.VoteMember.vote_result_code
        """
        results = []
        pattern = re.compile("""Vote_Bord""")
        match = pattern.split(self.page)
        for i in match:
            vote_result_code = ""
            if re.match("""_R1""", i):
                vote_result_code = "voted for"
            if re.match("""_R2""", i):
                vote_result_code = "voted against"
            if re.match("""_R3""", i):
                vote_result_code = "abstain"
            if re.match("""_R4""", i):
                vote_result_code = "did not vote"
            if vote_result_code != "":
                try:
                    member_id = re.search("""MKID=(\d+)""", i).group(1)
                    results.append((member_id, vote_result_code))
                except AttributeError as e:
                    logger.exception('Failed to find html vote for specific mk %s' % i)
                    continue
        return results

    @classmethod
    def get_from_vote_id(cls, vote_id):
        url = 'http://www.knesset.gov.il/vote/heb/Vote_Res_Map.asp?vote_id_t=%s' % vote_id
        logger.info('Trying to scrape member votes from %s', url)
        page = urlopen(url).read()
        return cls(page)
