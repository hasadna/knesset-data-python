from base import (BaseKnessetDataServiceCollectionObject, KnessetDataServiceSimpleField)


class BillName(BaseKnessetDataServiceCollectionObject):
    SERVICE_NAME = "api"
    METHOD_NAME = "KNS_BillName"
    ORDERED_FIELDS = [
        ("id", KnessetDataServiceSimpleField('BillNameID', "integer", "the primary key")),
        ("bill_id", KnessetDataServiceSimpleField('BillID', "integer", "The bill id")),
        ("name", KnessetDataServiceSimpleField('Name', "string", "The bill heb name")),
        ("name_history_type_id", KnessetDataServiceSimpleField('NameHistoryTypeID', "NameHistoryTypeID",
                                                               "Code for the name change time, ie before first or second call")),
        ("name_history_type_desc", KnessetDataServiceSimpleField('NameHistoryTypeDesc', "string",
                                                                 "Type of name change, ie name for first call, second call, etc..")),
        ("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", ))
    ]
