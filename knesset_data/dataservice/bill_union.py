from base import (BaseKnessetDataServiceCollectionObject, KnessetDataServiceSimpleField)


class BillUnion(BaseKnessetDataServiceCollectionObject):
    SERVICE_NAME = "api"
    METHOD_NAME = "KNS_BillUnion"
    ORDERED_FIELDS = [
        ("id", KnessetDataServiceSimpleField('BillUnionID', "integer", "the primary key")),
        ("main_bill_id", KnessetDataServiceSimpleField('MainBillID', "integer", "The main bill id that was merged")),
        ("name", KnessetDataServiceSimpleField('Name', "string", "The bill heb name")),
        ("name_history_type_id", KnessetDataServiceSimpleField('NameHistoryTypeID', "NameHistoryTypeID",
                                                               "Code for the name change time, ie before first or second call")),
        ("name_history_type_desc", KnessetDataServiceSimpleField('NameHistoryTypeDesc', "string",
                                                                 "Type of name change, ie name for first call, second call, etc..")),
        ("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", ))
    ]
