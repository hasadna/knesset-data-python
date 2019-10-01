import unittest
from knesset_data.protocols.utils import get_people_list


from .test_meetings import get_protocol_text_cached


def assert_get_people_list(text, token, expected):
    people_list = get_people_list(text, token)
    assert people_list == expected, 'token = {}, expected = {}, actual = {}'.format(token, expected, people_list)



class TestGetPeopleList(unittest.TestCase):

    def test(self):
        text = get_protocol_text_cached('86485')
        assert_get_people_list(text, 'מנהלת הוועדה:', ['לאה ורון'])

        text = get_protocol_text_cached('2058899')
        assert_get_people_list(text, 'מנהל/ת הוועדה:', ['איוור קירשנר'])
