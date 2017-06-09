from base import (BaseKnessetDataServiceCollectionObject, KnessetDataServiceSimpleField)


class BillName(BaseKnessetDataServiceCollectionObject):
    SERVICE_NAME = "api"
    METHOD_NAME = "KNS_BillName"
    ORDERED_FIELDS = [
        ("id", KnessetDataServiceSimpleField('BillNameID', "integer", "the primary key")),
        ("bill_id", KnessetDataServiceSimpleField('BillID', "integer", "The referenced bill id")),
        ("union_bill_id", KnessetDataServiceSimpleField('UnionBillID', "integer", "The merged bill id")),
        ("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", ))
    ]
