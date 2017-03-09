
# this list is based on the list at the following url under ODATA:
# http://main.knesset.gov.il/Activity/Info/Pages/Databases.aspx
SERVICE_URLS = {
    # following services are not working at the moment due to knesse problems
    # see https://github.com/hasadna/knesset-data/issues/124
    # once they are fixed - need to uncomment and re-run the tests to make sure it works..
    # 'laws': "http://knesset.gov.il/Odata_old/LawsData.svc",
    # 'members': "http://knesset.gov.il/Odata_old/KnessetMembersData.svc",
    # 'committees': "http://knesset.gov.il/Odata_old/CommitteeScheduleData.svc",

    'bills': "http://knesset.gov.il/KnessetOdataService/BillsData.svc",
    'final_laws': "http://knesset.gov.il/KnessetOdataService/FinalLawsData.svc",
    'votes': "http://knesset.gov.il/KnessetOdataService/VotesData.svc",
    'messages': "http://knesset.gov.il/KnessetOdataService/KnessetMessagesData.svc",
    'mmm': "http://knesset.gov.il/KnessetOdataService/MMMData.svc",
    'lobbyists': "http://knesset.gov.il/KnessetOdataService/LobbyistData.svc",
}
