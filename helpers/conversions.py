import random

def getCasePrefix(rangeId):
    rangeToCasePrefixMap = {"A":"EAC","B":"VSC","C":"WAC", "D":"CSC","E":"LIN","F":"NSC","G":"SRC","H":"TSC",
    "I":"MSC","J":"NBC","K":"IOE","L":"YSC"}
    return rangeToCasePrefixMap[rangeId[0:1]]

def getRangeId(case_number):
    RangeIdPrefixByFo = {"EAC":"A", "VSC":"B","WAC":"C", "CSC":"D","LIN":"E","NSC":"F","SRC":"G","TSC":"H",
    "MSC":"I","NBC":"J","IOE":"K","YSC":"L"}
    RangeIdPrefix = RangeIdPrefixByFo.get(case_number[0:3])
    if len(case_number)!=13 or RangeIdPrefix==None:
        return None
    lastFourDigs=case_number[9:]
    RangeIdSuffix = "0" if int(lastFourDigs)<4999 else "1"
    return RangeIdPrefix + case_number[3:9] + RangeIdSuffix

def getStatusCode(resultTitle):

    if "Case Was Received" in resultTitle:
        return 1
    if "Actively Reviewed" in resultTitle:
        return 2
    if "Review" in resultTitle:
        return 2
    if "Evidence" in resultTitle:
        if "Sent" in resultTitle:
            return 3
        if "Received" in resultTitle:
            return 4
    if "Interview" in resultTitle:
        if "Case is Ready" in resultTitle:
            return 5
        if "Scheduled" in resultTitle:
            return 6
    if "Denied" in resultTitle:
        return 7
    if "Rejected" in resultTitle:
        return 7
    if "Case Was Updated" in resultTitle:
        return 8
    if "Case Was Approved" in resultTitle: 
        return 9
    if "Benefit Received By Other Means" in resultTitle:
        return 9
    if "Picked Up" in resultTitle:
        return 10
    if "Delivered" in resultTitle:
        return 11
    if "Mailed" in resultTitle:
        return 11
    if "Certificate Of Naturalization" in resultTitle:
        return 13
    if "New Card" in resultTitle:
        return 15
    if "Transferred" in resultTitle:
        return 16
    return 14

def getStatusText(status_code):
    status_types = {1:"Case Received & Notice Sent",
                    2:"Case Actively Reviewed", 
                    3:"RFE Requested", 
                    4:"RFE Received",
                    5:"Ready For Interview",
                    6:"Interview Scheduled", 
                    7:"Denied", 
                    8:"Fingerprints were taken",
                    9:"Case Approved", 
                    10:"Card Picked Up",
                    11: "Card Delivered", 
                    12:"Oath Ceremony Notice Mailed",
                    13:"Certificate Of Naturalization Issued",
                    14:"Other",
                    15: "New Card Is Being Produced"
                    }
    return status_types.get(status_code)

def getRangeText(rangeId):
    casePrefix = getCasePrefix(rangeId)
    caseMiddle = rangeId[1:7]
    caseTailBegin = "0000" if rangeId[7] =="0" else "5000"
    caseTailEnd = "4999" if rangeId[7] =="0" else "9999"
 
    return casePrefix+caseMiddle+caseTailBegin + "-" + casePrefix+caseMiddle+caseTailEnd

def parseUserRequest(request):
    case_number = request.form['case_number']
    petition_date = request.form['petition_date']
    petition_type = request.form['petition_type']
    home_country = request.form['country']
    state = request.form['state']
    return {"case_number":case_number, "petition_date":petition_date, "petition_type":petition_type, "home_country":home_country, "state":state} 

def scrapeAll(probab):
    return random.random() < probab

def handleUnknownCaseType(statusCode, caseType):
    if statusCode in [9, 10, 11, 15] and caseType == "":
        return "ApprovedUnknown"
    if statusCode in [14] and caseType=="":
        return "OtherStatusUnknown"
    return caseType

