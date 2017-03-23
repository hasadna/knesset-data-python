from requests import RequestException


class KnessetDataRequestException(RequestException):

    def __init__(self, original_request_exception, *args, **kwargs):
        self.original_request_exception = original_request_exception
        original_request = getattr(original_request_exception, "request", None)
        self.url = original_request.url if original_request else ""
        self.message = original_request_exception.message
        super(KnessetDataRequestException, self).__init__(response=original_request_exception.response, request=original_request_exception.request, *args, **kwargs)

    def __str__(self):
        return "{}, {}".format(self.message, self.url)


class KnessetDataObjectException(Exception):

    def __init__(self, original_exception, *args, **kwargs):
        self.original_exception = original_exception
        self.message = self.original_exception.message
        super(KnessetDataObjectException, self).__init__(*args, **kwargs)
