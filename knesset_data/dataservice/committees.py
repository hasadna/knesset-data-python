# -*- coding: utf-8 -*-
import logging

from base import (
    BaseKnessetDataServiceCollectionObject, BaseKnessetDataServiceFunctionObject,
    KnessetDataServiceSimpleField, KnessetDataServiceLambdaField
)
from knesset_data.protocols.committee import CommitteeMeetingProtocol

logger = logging.getLogger('knesset_data.dataservice.committees')

IS_COMMITTEE_ACTIVE = 'committee_end_date eq null'
COMMITTEE_HAS_PORTAL_LINK = 'committee_portal_link ne null'


class Committee(BaseKnessetDataServiceCollectionObject):
    SERVICE_NAME = "committees"
    METHOD_NAME = "View_committee"
    DEFAULT_ORDER_BY_FIELD = "id"

    ORDERED_FIELDS = [
        ("id", KnessetDataServiceSimpleField('committee_id', "integer", "the primary key")),
        ("type_id", KnessetDataServiceSimpleField('committee_type_id', "integer", "linked to committee types dataservice")),
        ("parent_id", KnessetDataServiceSimpleField('committee_parent_id', "integer", "used for sub-committees, not sure if reliable")),
        ("name", KnessetDataServiceSimpleField('committee_name', "string", "hebrew name")),
        ("name_eng", KnessetDataServiceSimpleField('committee_name_eng', "string")),
        ("name_arb", KnessetDataServiceSimpleField('committee_name_arb', "string")),
        ("begin_date", KnessetDataServiceSimpleField('committee_begin_date', "datetime")),
        ("end_date", KnessetDataServiceSimpleField('committee_end_date', "datetime", "we assume empty end_date means committee is active in current Knesset")),
        ("description", KnessetDataServiceSimpleField('committee_desc', "string", "hebrew description")),
        ("description_eng", KnessetDataServiceSimpleField('committee_desc_eng', "string")),
        ("description_arb", KnessetDataServiceSimpleField('committee_desc_arb', "string")),
        ("note", KnessetDataServiceSimpleField('committee_note', "string")),
        ("note_eng", KnessetDataServiceSimpleField('committee_note_eng', "string")),
        ("portal_link", KnessetDataServiceSimpleField('committee_portal_link', "string", "can be used to link to the dedicated page in knesset website")),
    ]

    @classmethod
    def get_all_active_committees(cls, has_portal_link=True, proxies=None):
        if has_portal_link:
            query = ' '.join((IS_COMMITTEE_ACTIVE, 'and', COMMITTEE_HAS_PORTAL_LINK))
        else:
            query = IS_COMMITTEE_ACTIVE
        params = {'$filter': query}
        return cls._get_all_pages(cls._get_url_base(), params, proxies=proxies)


class CommitteeMeeting(BaseKnessetDataServiceFunctionObject):

    ORDERED_FIELDS = [
        (
        "id", KnessetDataServiceSimpleField('Committee_Agenda_id', 'integer', "the primary key of committee meetings")),
        ("committee_id", KnessetDataServiceSimpleField('Committee_Agenda_committee_id', 'integer',
                                                       "id of the committee (linked to Committee object)")),
        ("datetime",
         KnessetDataServiceSimpleField('committee_agenda_date', 'datetime', "date/time when the meeting started")),
        ("title", KnessetDataServiceSimpleField('title', 'string', "title of the meeting")),
        ("session_content", KnessetDataServiceSimpleField('committee_agenda_session_content', 'string',
                                                          "seems like in some committee meetings, the title field is empty, in that case title can be taken from this field")),
        ("url", KnessetDataServiceSimpleField('url', 'string', "url to download the protocol")),
        # a CommitteeMeetingProtocol object which allows to get data from the protocol
        # because parsing the protocol requires heavy IO and processing - we provide it as a generator
        # see tests/test_meetings.py for usage example
        ("protocol", KnessetDataServiceLambdaField(lambda obj, entry:
                                                   CommitteeMeetingProtocol.get_from_url(obj.url, proxies=obj._proxies)
                                                   if obj.url else None)),
        ("location ", KnessetDataServiceSimpleField('committee_location', 'string',
                                                    "this seems like a shorter name of the place where meeting took place")),
        ("place ", KnessetDataServiceSimpleField('Committee_Agenda_place', 'string',
                                                 "this looks like a longer field with the specific details of where the meeting took place")),
        ("meeting_stop ", KnessetDataServiceSimpleField('meeting_stop', 'string',
                                                        "date/time when the meeting ended - this is not always available, in some meetings it's empty")),
        ### following fields seem less interesting ###
        ("agenda_canceled ", KnessetDataServiceSimpleField('Committee_Agenda_canceled')),
        ("agenda_sub ", KnessetDataServiceSimpleField('Committee_agenda_sub')),
        ("agenda_associated ", KnessetDataServiceSimpleField('Committee_agenda_associated')),
        ("agenda_associated_id ", KnessetDataServiceSimpleField('Committee_agenda_associated_id')),
        ("agenda_special ", KnessetDataServiceSimpleField('Committee_agenda_special')),
        ("agenda_invited1 ", KnessetDataServiceSimpleField('Committee_agenda_invited1')),
        ("agenda_invite ", KnessetDataServiceSimpleField('sd2committee_agenda_invite')),
        ("note ", KnessetDataServiceSimpleField('Committee_agenda_note')),
        ("start_datetime ", KnessetDataServiceSimpleField('StartDateTime')),
        ("topid_id ", KnessetDataServiceSimpleField('Topic_ID')),
        ("creation_date ", KnessetDataServiceSimpleField('Date_Creation')),
        ("streaming_url ", KnessetDataServiceSimpleField('streaming_url')),
        ("meeting_start ", KnessetDataServiceSimpleField('meeting_start')),
        ("is_paused ", KnessetDataServiceSimpleField('meeting_is_paused')),
        ("date_order ", KnessetDataServiceSimpleField('committee_date_order')),
        ("date ", KnessetDataServiceSimpleField('committee_date')),
        ("day ", KnessetDataServiceSimpleField('committee_day')),
        ("month ", KnessetDataServiceSimpleField('committee_month')),
        ("material_id ", KnessetDataServiceSimpleField('material_id')),
        ("material_committee_id ", KnessetDataServiceSimpleField('material_comittee_id')),
        ("material_expiration_date ", KnessetDataServiceSimpleField('material_expiration_date')),
        ("material_hour ", KnessetDataServiceSimpleField('committee_material_hour')),
        ("old_url ", KnessetDataServiceSimpleField('OldUrl')),
        ("background_page_link ", KnessetDataServiceSimpleField('CommitteeBackgroundPageLink')),
        ("agenda_invited ", KnessetDataServiceSimpleField('Committee_agenda_invited')),
    ]

    @classmethod
    def _get_url_base(cls):
        return "http://online.knesset.gov.il/WsinternetSps/KnessetDataService/CommitteeScheduleData.svc/CommitteeAgendaSearch"

    @classmethod
    def get(cls, committee_id, from_date, to_date=None, proxies=None):
        """
        # example usage:
        >>> from datetime import datetime
        # get all meetings of committee 1 from Jan 01, 2016
        >>> CommitteeMeeting.get(1, datetime(2016, 1, 1))
        # get all meetings of committee 2 from Feb 01, 2015 to Feb 20, 2015
        >>> CommitteeMeeting.get(2, datetime(2015, 2, 1), datetime(2015, 2, 20))
        """
        params = {
            "CommitteeId": "'%s'" % committee_id,
            "FromDate": "'%sT00:00:00'" % from_date.strftime('%Y-%m-%d')
        }
        if to_date:
            params["ToDate"] = "'%sT00:00:00'" % to_date.strftime('%Y-%m-%d')
        return super(CommitteeMeeting, cls).get(params, proxies=proxies)
