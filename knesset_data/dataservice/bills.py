from base import (
    BaseKnessetDataServiceCollectionObject, BaseKnessetDataServiceFunctionObject,
    KnessetDataServiceSimpleField, KnessetDataServiceLambdaField
)
import constants


class Bill(BaseKnessetDataServiceCollectionObject):
    SERVICE_NAME = "api"
    METHOD_NAME = "KNS_Bill"
    ORDERED_FIELDS = [
        ("id", KnessetDataServiceSimpleField('BillID', "integer", "the primary key")),
        ("kns_num", KnessetDataServiceSimpleField('KnessetNum', "integer", "kneset number")),
        ("name", KnessetDataServiceSimpleField('Name', "string", "bill heb name")),
        ("type_id", KnessetDataServiceSimpleField('SubTypeID', "integer", "type id of the bill")),
        ("type_description",
         KnessetDataServiceSimpleField('SubTypeDesc', "string", "type description of the bill")),
        ("private_num", KnessetDataServiceSimpleField('PrivateNumber', "integer",)),
        ("committee_id", KnessetDataServiceSimpleField('CommitteeID', "integer",)),
        ("status_id", KnessetDataServiceSimpleField('StatusID', "integer",)),
        ("num", KnessetDataServiceSimpleField('Number', "Integer",)),
        ("postponent_reason_id", KnessetDataServiceSimpleField('PostponementReasonID',
                                                               "Integer",)),
        ("postponent_reason_desc", KnessetDataServiceSimpleField('PostponementReasonDesc', "string",)),
        ("public_date", KnessetDataServiceSimpleField('PublicationDate', "datetime",)),
        ("magazine_num", KnessetDataServiceSimpleField('MagazineNumber', "integer",)),
        ("page_num", KnessetDataServiceSimpleField('PageNumber', "integer")),
        ("is_continuation", KnessetDataServiceSimpleField('IsContinuationBill', "bool",)),
        ("sum_law", KnessetDataServiceSimpleField('SummaryLaw', "string", )),
        ("public_series_id", KnessetDataServiceSimpleField('PublicationSeriesID', "integer",)),
        ("public_series_desc", KnessetDataServiceSimpleField('PublicationSeriesID', "string",)),
        ("public_series_first_call", KnessetDataServiceSimpleField('PublicationSeriesFirstCall', "string", )),
        ("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", ))


    ]



