# -*- coding: utf-8 -*
import difflib
from collections import namedtuple

ParsedHeader = namedtuple('ParsedHeader', ['text', 'speaker_id'])


class HeaderNamesTokenizer(object):
    def __init__(self, text):
        self.text = text

    def tokenize(self):

        tokens = self._tokenize()
        return list(tokens)

    def _tokenize(self):
        tokens = set()
        sentence_words = []
        for word in self.text.split(' '):
            sentence_words.append(word)
            tokens.add(word)
        for i, word in enumerate(sentence_words):
            if i < len(sentence_words) - 1:
                pair = u'{0} {1}'.format(word, sentence_words[i + 1])
                reverse_pair = u'{1} {0}'.format(word, sentence_words[i + 1])
                tokens.add(pair)
                tokens.add(reverse_pair)
            if i < len(sentence_words) - 2:
                triple = u'{0} {1} {2}'.format(word, sentence_words[i + 1], sentence_words[i + 2])
                tokens.add(triple)

        return tokens




class ProtocolHeaderParser(object):
    def __init__(self, header_text, persons_map):
        """

        :param headers:
        :param persons_map: dict()
        """

        self.persons_map = persons_map
        self.header_text = header_text

    def parse(self):
        speaker_id = None
        for person_name, person_id in self.persons_map.items():
            if person_name in self.header_text:
                speaker_id = person_id
                break
        if not speaker_id:
            possible_names = HeaderNamesTokenizer(self.header_text).tokenize()
            for person_name, person_id in self.persons_map.items():

                possible_matches = difflib.get_close_matches(person_name, possible_names, 1, cutoff=0.9)
                if len(possible_matches) > 0:
                    speaker_id = person_id
                    break
        return ParsedHeader(text=self.header_text, speaker_id=speaker_id)
