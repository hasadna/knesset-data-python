from base import (BaseKnessetDataServiceCollectionObject, KnessetDataServiceSimpleField)


class DocumentBill(BaseKnessetDataServiceCollectionObject):
    SERVICE_NAME = "api"
    METHOD_NAME = "KNS_DocumentBill"
    ORDERED_FIELDS = [
        ("id", KnessetDataServiceSimpleField('DocumentBillID', "integer", "the primary key")),
        ("bill_id", KnessetDataServiceSimpleField('BillID', "integer", "The main bill id that was merged")),
        ("group_type_id", KnessetDataServiceSimpleField('GroupTypeID', "integer", "The type of the document")),
        ("group_type_desc", KnessetDataServiceSimpleField('GroupTypeDesc', "string", "Type of the document")),
        ("application_id", KnessetDataServiceSimpleField('ApplicationID', "integer", "Code of the document format")),
        ("application_desc",
         KnessetDataServiceSimpleField('ApplicationDesc', "string", "The document format(word, pdf, etc...)")),
        ("file_path",
         KnessetDataServiceSimpleField('FilePath', "string", "The url of the document")),
        ("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", ))
    ]
