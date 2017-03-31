# see https://github.com/hasadna/knesset-data/blob/master/docs/dataservice/README.md

SERVICE_URLS = {
    # these are the new old apis
    'laws': "http://knesset.gov.il/Odata_old/LawsData.svc",
    'members': "http://knesset.gov.il/Odata_old/KnessetMembersData.svc",
    'committees': "http://knesset.gov.il/Odata_old/CommitteeScheduleData.svc",
    'api': 'http://knesset.gov.il/Odata/ParliamentInfo.svc/',
    # this services use the old urls
    'bills': "http://knesset.gov.il/KnessetOdataService/BillsData.svc",
    'final_laws': "http://knesset.gov.il/KnessetOdataService/FinalLawsData.svc",
    'votes': "http://knesset.gov.il/KnessetOdataService/VotesData.svc",
    'messages': "http://knesset.gov.il/KnessetOdataService/KnessetMessagesData.svc",
    'mmm': "http://knesset.gov.il/KnessetOdataService/MMMData.svc",
    'lobbyists': "http://knesset.gov.il/KnessetOdataService/LobbyistData.svc",
}
