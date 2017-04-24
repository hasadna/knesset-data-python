from knesset_data.exceptions import KnessetDataObjectException, KnessetDataRequestException


class KnessetDataServiceRequestException(KnessetDataRequestException):

    def __init__(self, service_name, method_name, original_request_exception, *args, **kwargs):
        self.knesset_data_service_name = service_name
        self.knesset_data_method_name = method_name
        super(KnessetDataServiceRequestException, self).__init__(original_request_exception, *args, **kwargs)

    def __str__(self):
        return "{}, {}".format(self.message, self.url)


class KnessetDataServiceObjectException(KnessetDataObjectException):

    def __init__(self, cls, original_exception, entry=None, *args, **kwargs):
        self.dataservice_class = cls
        self.unparsed_entry = entry
        super(KnessetDataServiceObjectException, self).__init__(original_exception, *args, **kwargs)
