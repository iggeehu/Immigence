from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show
from helpers.dbConnect import DatabaseConnect, databaseConnect
from bokeh.embed import components
from constants import CASE_TYPES
from bokeh.models import DatetimeTickFormatter, Legend, LegendItem
import numpy as np
import pandas as pd
from bokeh.palettes import Category20_10

def getStatusDataPerType(rangeId, caseType):

    with DatabaseConnect("RangeLog") as (cnx, cursor):
        tableName = "R"+rangeId
        query = "Select * from "+tableName +" where caseType = %s"
        try:
            cursor.execute(query, (caseType,))
            result = cursor.fetchall()
            collectionDates = []
            approved = []
            received = []
            activeReview =[]
            denied = []
            RFEreq = []
            IntSched = []
            FingTaken =[]
            Transferred=[]
            IntReady=[]
            RFErec = []
            Other = []
            for tup in result:
                collectionDates.append(tup[1])
                approved.append(tup[3])
                received.append(tup[4])
                activeReview.append(tup[5])
                denied.append(tup[6])
                RFEreq.append(tup[7])
                IntSched.append(tup[8])
                Other.append(tup[9])
                IntReady.append(tup[(10)])
                RFErec.append(tup[11])
                FingTaken.append(tup[12])
                Transferred.append(tup[13])
                
            return [collectionDates, approved,received,activeReview,denied,RFEreq, IntSched, Other, IntReady,RFErec,FingTaken, Transferred]
        except:
            return None


def outputStatusPerTypeDictAndGraph(rangeId):
    dictOfGraphs = {}
    
    for caseType in CASE_TYPES:    
        statusCount = getStatusDataPerType(rangeId, caseType)
        if statusCount==None:
            return None
       
        dates = pd.to_datetime(statusCount[0])
        labels=["Case Received", "Active Review",  "RFE requested", "RFE received",
                "Interview Ready", "Interview Scheduled", "Approved", "Denied", 
                "Fingerprints Taken", "Transferred", "Other"]
        data = {"Approved":statusCount[1], "Case Received":statusCount[2], "date": dates, 
                "Active Review":statusCount[3], "Denied":statusCount[4], "RFE requested":statusCount[5], 
                "Interview Scheduled":statusCount[6], "Other":statusCount[7], "Interview Ready":statusCount[8], 
                "RFE received":statusCount[9], "Fingerprints Taken": statusCount[10],
                "Transferred": statusCount[11]
                }
        

        source = ColumnDataSource(data=data)
        
        dictOfGraphs[caseType] = figure(height=300, width=800,
           x_axis_type="datetime",
           background_fill_color="#efefef")
        dictOfGraphs[caseType].title.text = 'Number of Cases by Status, Over Time'
        legendItems = []

        for i in range(10):
            r= dictOfGraphs[caseType].line(dates, data[labels[i]], line_color=Category20_10[i])
            item= LegendItem(label=labels[i], renderers=[r], index=i)
            legendItems.append(item)

        legend = Legend(items=legendItems)
        legend.click_policy="mute"
        dictOfGraphs[caseType].add_layout(legend, 'right')
    
        #give color to legend items
      
        
       
    return dictOfGraphs
