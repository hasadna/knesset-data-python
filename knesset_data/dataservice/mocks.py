# this module is used by knesset-data-datapackage for testing
# please try not to break backwards compatibility

from knesset_data.dataservice.members import Member


class MockMember(Member):
    SOUP_MEMBER_IDS = range(200, 205)
    EXCEPTION_ON_INIT_MEMBER_ID = 203
    EXCEPTION_ON_PARSE_MEMBER_ID = 204
    EXCEPTION_ON_GET_MEMBER_ID = 215

    def __init__(self, entry):
        if entry["data"]["mk_individual_id"] == self.EXCEPTION_ON_INIT_MEMBER_ID:
            raise Exception("member with exception on init")
        super(MockMember, self).__init__(entry)

    @classmethod
    def _parse_entry(cls, entry):
        parsed_entry = super(MockMember, cls)._parse_entry(entry)
        if parsed_entry["data"]["mk_individual_id"] == cls.EXCEPTION_ON_PARSE_MEMBER_ID:
            raise Exception("member with exception on parse")
        return parsed_entry

    @classmethod
    def _parse_entry_id(cls, entry):
        return str(entry)

    @classmethod
    def _parse_entry_links(cls, entry):
        return []

    @classmethod
    def _parse_entry_data(cls, entry):
        data = {field._knesset_field_name: "" for field in cls.get_fields().values() if hasattr(field, "_knesset_field_name")}
        data["mk_individual_id"] = entry
        return data

    @classmethod
    def _get_soup(cls, url, params=None, proxies=None):
        if "({})".format(cls.EXCEPTION_ON_GET_MEMBER_ID) in url:
            raise Exception("member with exception on get")
        else:
            def find(soup_instance, name, **kwargs):
                return None
            def find_all(feed_instance, name, attrs=None):
                if name == "link":
                    return []
                else:
                    return [i for i in cls.SOUP_MEMBER_IDS]
            return type("MockSoup", (object,),
                        {"feed": type("MockFeed", (object,),
                                      {"find_all": find_all})(),
                         "find": find})()
