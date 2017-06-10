from base import (BaseKnessetDataServiceCollectionObject, KnessetDataServiceSimpleField)


class BillUnion(BaseKnessetDataServiceCollectionObject):
    SERVICE_NAME = "api"
    METHOD_NAME = "KNS_BillUnion"
    ORDERED_FIELDS = [
        ("id", KnessetDataServiceSimpleField('BillUnionID', "integer", "the primary key")),
        ("main_bill_id", KnessetDataServiceSimpleField('MainBillID', "integer", "The referenced bill id")),
        ("union_bill_id", KnessetDataServiceSimpleField('UnionBillID', "integer", "The merged bill id")),
        ("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", ))
    ]
