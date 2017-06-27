from requests import RequestException
import six


class KnessetDataRequestException(RequestException):

    def __init__(self, original_request_exception, *args, **kwargs):
        self.original_request_exception = original_request_exception
        original_request = getattr(original_request_exception, "request", None)
        self.url = original_request.url if original_request else ""

        # no message field in python3
        if six.PY2:
            self.message = original_request_exception.message
        elif six.PY3:
            self.message = original_request_exception.args[0]
        else:
            raise RuntimeError("unsupported python version")
        super(KnessetDataRequestException, self).__init__(response=original_request_exception.response, request=original_request_exception.request, *args, **kwargs)

    def __str__(self):
        if six.PY2:
            return "{}, {}".format(self.message, self.url)
        elif six.PY3:
            return "{}, {}".format(self.args[0], self.url)
        else:
            raise RuntimeError("unsupported python version")


class KnessetDataObjectException(Exception):

    def __init__(self, original_exception, *args, **kwargs):
        self.original_exception = original_exception
        # no message field in python3
        if six.PY2:
            self.message = self.original_exception.message
        elif six.PY3:
            self.message = self.original_exception.args[0]
        else:
            raise RuntimeError("unsupported python version")
        super(KnessetDataObjectException, self).__init__(*args, **kwargs)

    def __str__(self):
        if six.PY2:
            return self.message
        elif six.PY3:
            return self.args[0]
        else:
            raise RuntimeError("unsupported python version")
