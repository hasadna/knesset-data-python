import requests


GET_ALL_MK_NAMES_URL = "https://oknesset.org/api/knesset-data/get_all_mk_names.json"


def get_all_mk_names():
    return requests.get(GET_ALL_MK_NAMES_URL).json()
