import os
from mock import mock


def execute_from_local_file(tested_obj, content_file_path, object_id_to_test):
    content_file_path = os.path.join(os.path.dirname(__file__), "response_files", content_file_path)
    tested_obj._get_response_content = mock.MagicMock()
    with open(content_file_path, 'r') as f:
        content = f.read()
    tested_obj._get_response_content.return_value = content
    return tested_obj.get(object_id_to_test)
