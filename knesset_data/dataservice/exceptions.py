from requests import RequestException


class KnessetDataServiceRequestException(RequestException):

    def __init__(self, service_name, method_name, original_request_exception, *args, **kwargs):
        self.knesset_data_service_name = service_name
        self.knesset_data_method_name = method_name
        self.original_request_exception = original_request_exception
        original_request = getattr(original_request_exception, "request", None)
        self.url = original_request.url if original_request else ""
        self.message = original_request_exception.message
        super(KnessetDataServiceRequestException, self).__init__(response=original_request_exception.response, request=original_request_exception.request, *args, **kwargs)

    def __str__(self):
        return "{}, {}".format(self.message, self.url)