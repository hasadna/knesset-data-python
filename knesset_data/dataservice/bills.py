from base import (
    BaseKnessetDataServiceCollectionObject, BaseKnessetDataServiceFunctionObject,
    KnessetDataServiceSimpleField, KnessetDataServiceLambdaField
)
import constants

class Bill(BaseKnessetDataServiceCollectionObject):
    SERVICE_NAME = "api"
    METHOD_NAME = "KNS_Bill"
    ORDERED_FIELDS = [("id", KnessetDataServiceSimpleField('BillID', "integer", "the primary key")),]



