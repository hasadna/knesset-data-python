from base import (BaseKnessetDataServiceCollectionObject, KnessetDataServiceSimpleField)


class BillSplit(BaseKnessetDataServiceCollectionObject):
    SERVICE_NAME = "api"
    METHOD_NAME = "KNS_BillSplit"
    ORDERED_FIELDS = [
        ("id", KnessetDataServiceSimpleField('BillSplitID', "integer", "the primary key")),
        ("bill_id", KnessetDataServiceSimpleField('MainBillID', "integer", "The bill that was split")),
        ("split_bill_id",
         KnessetDataServiceSimpleField('SplitBillID', "integer", "the bill that was created from the split")),
        ("name", KnessetDataServiceSimpleField('Name', "string", "The newly created bill heb name")),
        ("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", ))
    ]
