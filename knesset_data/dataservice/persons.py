from base import (
	BaseKnessetDataServiceCollectionObject, KnessetDataServiceSimpleField
	)

class Person(BaseKnessetDataServiceCollectionObject):
	SERVICE_NAME = "api"
	METHOD_NAME = "KNS_Person"
	ORDERED_FIELDS =[
		("id", KnessetDataServiceSimpleField('PersonID', "integer", "the primary key")),
		("last_name", KnessetDataServiceSimpleField('LastName', "string", "last name")),
		("first_name", KnessetDataServiceSimpleField('FirstName', "string", "first name")),
		("gender_id", KnessetDataServiceSimpleField('GenderID', "integer", "gender id code")),
		("gender_description", KnessetDataServiceSimpleField('GenderDesc', "string", "gender description")),
		("email", KnessetDataServiceSimpleField('Email', "string", "email address")),
		("is_current", KnessetDataServiceSimpleField('IsCurrent', "bool", "is a current member")),
		("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", ))
		]