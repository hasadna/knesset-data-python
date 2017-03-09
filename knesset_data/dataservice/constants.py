# see https://github.com/hasadna/knesset-data/blob/master/docs/dataservice/README.md

SERVICE_URLS = {
    # following services have some problems with the urls
    # see https://github.com/hasadna/knesset-data/issues/124
    # currently they only work from the very old knesset apis but only from whitelisted ip
    'laws': "http://online.knesset.gov.il/WsinternetSps/KnessetDataService/LawsData.svc",
    'members': "http://online.knesset.gov.il/WsinternetSps/KnessetDataService/KnessetMembersData.svc",
    'committees': "http://online.knesset.gov.il/WsinternetSps/KnessetDataService/CommitteeScheduleData.svc",

    # this services use the old urls
    # see https://github.com/hasadna/knesset-data/blob/master/docs/dataservice/README.md
    'bills': "http://knesset.gov.il/KnessetOdataService/BillsData.svc",
    'final_laws': "http://knesset.gov.il/KnessetOdataService/FinalLawsData.svc",
    'votes': "http://knesset.gov.il/KnessetOdataService/VotesData.svc",
    'messages': "http://knesset.gov.il/KnessetOdataService/KnessetMessagesData.svc",
    'mmm': "http://knesset.gov.il/KnessetOdataService/MMMData.svc",
    'lobbyists': "http://knesset.gov.il/KnessetOdataService/LobbyistData.svc",
}
