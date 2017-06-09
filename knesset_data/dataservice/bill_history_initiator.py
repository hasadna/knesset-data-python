from base import (
    BaseKnessetDataServiceCollectionObject, KnessetDataServiceSimpleField
)


class BillHistoryInitiator(BaseKnessetDataServiceCollectionObject):
    SERVICE_NAME = "api"
    METHOD_NAME = "KNS_BillHistoryInitiator"
    ORDERED_FIELDS = [
        ("id", KnessetDataServiceSimpleField('BillHistoryInitiatorID', "integer", "the primary key")),
        ("bill_id", KnessetDataServiceSimpleField('BillID', "integer", "The referenced bill id")),
        ("person_id", KnessetDataServiceSimpleField('PersonID', "integer", "the person id")),
        ("is_initiator", KnessetDataServiceSimpleField('IsInitiator', "integer", "Is the person initiator of the bill")),

        ("start_date", KnessetDataServiceSimpleField('StartDate', "datetime", "The date that the person was added to the bill")),
        ("end_date", KnessetDataServiceSimpleField('EndDate', "datetime", "The date that the person was removed from the bill")),
        ("reason_id", KnessetDataServiceSimpleField('ReasonID', "int", "The code reason of the person removal from the bill")),
        ("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", ))

    ]
