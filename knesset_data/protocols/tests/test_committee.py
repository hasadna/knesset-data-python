# -*- coding: utf-8 -*-
import unittest
from knesset_data.protocols.committee import CommitteeMeetingProtocol
import os
from knesset_data.utils.testutils import TestCaseFileAssertionsMixin
from knesset_data.non_knesset_data.open_knesset import get_all_mk_names
from knesset_data.non_knesset_data.mocks import MOCK_OPEN_KNESSET_GET_ALL_MK_NAMES_RESPONSE


class TestCommitteeMeetings(unittest.TestCase, TestCaseFileAssertionsMixin):

    maxDiff = None

    def setUp(self):
        source_doc_file_name = os.path.join(os.path.dirname(__file__), '20_ptv_317899.doc')
        self.protocol_generator = CommitteeMeetingProtocol.get_from_filename(source_doc_file_name)

    def test_text(self):
        with self.protocol_generator as protocol:
            self.assertFileContents(
                expected_file_name=os.path.join(os.path.dirname(__file__), '20_ptv_317899_processed.txt'),
                actual_content=protocol.text
            )

    def test_attending_members(self):
        with self.protocol_generator as protocol:
            self.assertEqual([u"משה גפני", u"מיקי לוי"],
                             protocol.find_attending_members([u"סתיו שפיר", u"משה גפני", u"מיקי לוי"]))

    def test_parts(self):
        with self.protocol_generator as protocol:
            parts = protocol.parts
            self.assertProtocolPartEquals(parts[0], u"", u"""הכנסת העשרים

מושב שני

פרוטוקול מס' 189

מישיבת ועדת הכספים

יום שלישי, כ"ו בכסלו התשע"ו (08 בדצמבר 2015), שעה 10:00""")
            self.assertProtocolPartEquals(parts[1],
                                          u"""סדר היום""",
                                          u"""צו תעריף המכס והפטורים ומס קנייה על טובין (הוראת שעה מס' 11), התשע"ה-2015 (ממירים – הטלת מכס על יבוא ממירים אלקטרוניים)""")
            self.assertProtocolPartEquals(parts[2],
                                          u"""נכחו""",
                                          "")
            self.assertProtocolPartEquals(parts[3],
                                          u"""חברי הוועדה:""",
                                          u"""משה גפני – היו"ר

מיקי לוי""")
            self.assertProtocolPartEquals(parts[4],
                                          u"""מוזמנים:""",
                                          u"""איריס וינברגר - סגנית בכירה ליועמ"ש, משרד האוצר

גיא גולדמן - עוזר ראשי מחלקה משפטית, משרד האוצר

עמוס יוגב - מנהל תחום סיווג ארצי, משרד האוצר

קובי בוזו - מנהל תחום בכיר תכנון וכלכלה, משרד האוצר

רפאל חדד - מנהל פיתוח עסקים, משרד הכלכלה

שאול ששון - מנהל תחום תעשיות, משרד הכלכלה

גילה ורד - עו"ד, הרשות השניה לטלוויזיה ורדיו

חניתה חפץ - לוביסטית (פוליסי), מייצגת את סלקום""")
            self.assertProtocolPartEquals(parts[5], u"""ייעוץ משפטי""", u"""שלומית ארליך""")
            self.assertProtocolPartEquals(parts[6], u"""מנהל הוועדה""", u"""טמיר כהן""")
            self.assertProtocolPartEquals(parts[7], u"""רישום פרלמנטרי""", u"""הדס צנוירט

צו תעריף המכס והפטורים ומס קנייה על טובין (הוראת שעה מס' 11), התשע"ה-2015 (ממירים – הטלת מכס על יבוא ממירים אלקטרוניים)""")
            self.assertProtocolPartEquals(parts[8],
                                          u"""היו"ר משה גפני""",
                                          u"""בוקר טוב, אני מתכבד לפתוח את ישיבת ועדת הכספים. יש לנו היום צווים, תעריפי מכס. צו תעריף המכס והפטורים ומס קנייה על טובין (הוראת שעה מס' 11), התשע"ו-2015 (ממירים – הטלת מכס על יבוא ממירים אלקטרוניים). מי מציג את הצו? בבקשה.""")
            self.assertProtocolPartEquals(parts[9],
                                          u"""קובי בוזו""",
                                          u"""בוקר טוב. קובי בוזו, רשות המסים. לצדי גיא גולדמן. לפני כחצי שנה היינו בוועדת הכספים בנושא של ממירים, וביקשנו, בשיתוף עם משרד הכלכלה, להמיר את מס הקנייה בשיעור 10% על ממירים, למכס בשיעור 10% על ממירים.""")

    def test_protocol_attendenace_strange_title(self):
        source_doc_file_name = os.path.join(os.path.dirname(__file__), '20_ptv_321195.doc')
        protocol_generator = CommitteeMeetingProtocol.get_from_filename(source_doc_file_name)
        with protocol_generator as protocol:
            self.assertEqual([u"קארין אלהרר", u"דוד אמסלם", u"אוסאמה סעדי"],
                             protocol.find_attending_members([u"קארין אלהרר", u"דוד אמסלם", u"אוסאמה סעדי"]))

    def test_attending_members_invalid_data(self):
        # file does not exist
        with CommitteeMeetingProtocol.get_from_filename('/foo/bar/baz') as protocol:
            with self.assertRaises(IOError): protocol.find_attending_members([])
        # no text
        with CommitteeMeetingProtocol.get_from_text(None) as protocol:
            self.assertEqual([], protocol.find_attending_members([]))

    def test_missing_member_issue132(self):
        # TODO: switch to env_conditional_mock function when PR #9 is merged
        if os.environ.get("NO_MOCKS", "") == "1":
            all_mk_names = get_all_mk_names()
        else:
            all_mk_names = MOCK_OPEN_KNESSET_GET_ALL_MK_NAMES_RESPONSE
        mks, mk_names = all_mk_names
        with CommitteeMeetingProtocol.get_from_filename(os.path.join(os.path.dirname(__file__), '20_ptv_367393.doc')) as protocol:
            attending_members = protocol.find_attending_members(mk_names)
            self.assertEqual(attending_members, [u"אוסאמה סעדי",
                                                 u"אורי מקלב",
                                                 u"זאב בנימין בגין",
                                                 u"יוליה מלינובסקי",
                                                 # this MK has extra space which caused him not to be found
                                                 # now we search the stripped name
                                                 # but the return value still has the extra space (as provided)
                                                 u"מיכאל מלכיאלי ",
                                                 u"רויטל סויד",
                                                 u"בנימין בגין",])

    def assertProtocolPartEquals(self, part, header, body):
        try:
            self.assertEqual(part.header, header)
        except Exception as e:
            print("--expected-header=", header, "--")
            print("--actual-header=", part.header, "--")
            raise
        try:
            self.assertEqual(part.body, body)
        except Exception as e:
            print("--expected-body = ", body, "--")
            print("--actual-body = ", part.body, "--")
            raise

