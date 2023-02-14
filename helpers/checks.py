from helpers.dbConnect import databaseClose, databaseConnect
from helpers.conversions import getRangeId

def rangeLogTableExist(rangeId):
    cnx = databaseConnect("RangeLog")
    tableName = "R"+rangeId
    if cnx!=None:
        cursor = cnx.cursor()
        query = "SELECT EXISTS (SELECT "+tableName+" FROM information_schema.TABLES"
        cursor.execute(query)
        answer = cursor.fetchone()
        if answer==None or answer[0]==0:
            return False
        return True
    else:
        return False

def rangeExist(rangeId):
    cnx = databaseConnect("QueryableCases")
    if cnx!=None:
        cursor = cnx.cursor()
        query = ("SHOW TABLES" )
        cursor.execute(query)
        ret = False
        for table in cursor:
            #a table exists, now check that it actually has rows (in case createNewRange stopped midway)
            if table[0] == rangeId:
                ret = True
        cursor.close()
        databaseClose(cnx)
        return ret

def checkType(petition_type, resultContent):
    case_types = ["I-485", 'I-140', 'I-765', 'I-821', 'I-131', 'I-129', 'I-539', 'I-130', 'I-90', 'N-400']
    first_line = resultContent[0:100]
    # print(first_line)
    true_type = petition_type
    res_has_type = False
    for case_type in case_types:
        if case_type in first_line: 
            res_has_type = True
            if case_type != true_type:
                true_type = case_type
            break
    if petition_type!="N-400" and res_has_type == False and "oath" in first_line:
        true_type = "N-400"
    return true_type


def fetchedButInvalid(cursor, caseNumber):
    query="Select LastFetched from "+getRangeId(caseNumber)+" WHERE CaseNumber = %s"
    cursor.execute(query, (caseNumber,))
    tuple =cursor.fetchone()
    print(tuple)
    if(tuple==None):
        return False
    if(tuple[0]==None):
        return False
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!UPDATED TODAY!!!!!!!!!!!!!!")
    return True


def caseInited(cursor, caseNumber):
    query="Select StatusCode from "+getRangeId(caseNumber)+" WHERE CaseNumber = %s"
    cursor.execute(query, (caseNumber,))
    tuple =cursor.fetchone()
    if(tuple==None):
        return False
    if(tuple[0]==None):
        return False
    return True

 
def rangeTablePopulated(rangeId):
    cnx=databaseConnect("QueryableCases")
    cursor=cnx.cursor()
    query="Select count(*) from "+rangeId
    cursor.execute(query)
    if cursor.fetchall()[0][0]>4900:
        print("rangeTablePopulated")
        return True
    print("rangeTable NOT populated")
    return False



def isLogUpdatedToday(cursor, rangeId):
    tableName = "R" + rangeId
    query = "select * from "+tableName+" where CollectionDate = CURDATE()" 
    cursor.execute(query)
    listTups= cursor.fetchall()
    if len(listTups)<11:
        return False
    return True