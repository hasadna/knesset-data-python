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
		("is_current", KnessetDataServiceSimpleField('IsCurrent', "string", "is a current member")),
		("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", "last updated"))
		]

class Position(BaseKnessetDataServiceCollectionObject):
	SERVICE_NAME = "api"
	METHOD_NAME = "KNS_Position"
	ORDERED_FIELDS =[
		("id", KnessetDataServiceSimpleField('PositionID', "integer", "the primary key")),
		("description", KnessetDataServiceSimpleField('Description', "string", "position description")),
		("gender_id", KnessetDataServiceSimpleField('GenderID', "integer", "gender id code")),
		("gender_description", KnessetDataServiceSimpleField('GenderDesc', "string", "gender description")),
		("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", "last updated"))
	]

class PersonToPosition(BaseKnessetDataServiceCollectionObject):
	SERVICE_NAME = "api"
	METHOD_NAME = "KNS_PersonToPosition"
	ORDERED_FIELDS =[
		("id", KnessetDataServiceSimpleField('PersonToPositionID', "integer", "the primary key")),
		("person_id", KnessetDataServiceSimpleField('PersonID', "integer", "the person id")),
		("position_id", KnessetDataServiceSimpleField('PositionID', "integer", "the position id")),
		("knnesset_num", KnessetDataServiceSimpleField('KnessetNum', "integer", "the knesset number")),
		("ministry_id", KnessetDataServiceSimpleField('GovMinistryID', "integer", "the ministry id code")),
		("ministry_name", KnessetDataServiceSimpleField('GovMinistryName', "string", "ministry name")),
		("duty_description", KnessetDataServiceSimpleField('DutyDesc', "string", "duty description")),
		("faction_id", KnessetDataServiceSimpleField('FactionID', "integer", "the party id code")),
		("faction_name", KnessetDataServiceSimpleField('FactionName', "string", "party name")),
		("gov_num", KnessetDataServiceSimpleField('GovernmentNum', "integer", "the government number")),
		("committee_id", KnessetDataServiceSimpleField('CommitteeID', "integer", "the committee id code")),
		("committee_name", KnessetDataServiceSimpleField('CommitteeName', "string", "committee name")),
		("start_update", KnessetDataServiceSimpleField('StartDate', "datetime", "start date")),
		("finish_update", KnessetDataServiceSimpleField('FinishDate', "datetime", "finish date")),
		("is_current", KnessetDataServiceSimpleField('IsCurrent', "string", "is current")),
		("last_update", KnessetDataServiceSimpleField('LastUpdatedDate', "datetime", "last updated"))
	]

class SiteCode(BaseKnessetDataServiceCollectionObject):
	SERVICE_NAME = "api"
	METHOD_NAME = "KNS_MkSiteCode"
	ORDERED_FIELDS =[
		("id", KnessetDataServiceSimpleField('MKSiteCode', "integer", "the primary key")),
		("kns_id", KnessetDataServiceSimpleField('KnsID', "integer", "KM code for the new api tables")),
		("site_id", KnessetDataServiceSimpleField('SiteId', "integer", "KM code from the old kneset website"))
	]