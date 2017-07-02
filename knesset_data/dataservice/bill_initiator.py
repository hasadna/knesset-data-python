from base import (BaseKnessetDataServiceCollectionObject, KnessetDataServiceSimpleField)


class BillInitiator(BaseKnessetDataServiceCollectionObject):
    SERVICE_NAME = "api"
    METHOD_NAME = "KNS_BillInitiator"
    ORDERED_FIELDS = [
        ("id", KnessetDataServiceSimpleField('BillInitiatorID', "integer", "the primary key")),
        ("bill_id", KnessetDataServiceSimpleField('BillID', "integer", "the bill id in bill table")),
        ("person_id", KnessetDataServiceSimpleField('PersonID', "integer", "the initiator peron id")),
        ("ordinal", KnessetDataServiceSimpleField('Ordinal', "integer",
                                                  "The position of the initiator in the list of initiators")),
        ("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", ))
    ]
