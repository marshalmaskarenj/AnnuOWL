"""This component takes in the Annual CS for each hour (by reading CSV files for live or pre-cached simulations) for 4 orientations, takes in occupancy hours (SOB, COB, Days of week) and bins the circadian potential performance into High, Medium, Minimum and non compliant based on the defined thresholds.
For each occupied day, non-visual performance for each bin (High/Med/Min/NC) is defined as the percentage of occupied days in a year when CS exceeds defined threshold for at least 1 occupied hour in the morning (between 0800-1200 inclusive, depending also on SOB/COB).
Further, at the occupant position level, if any point, for defined percent of occupied hours does not qualify for High, then it checks for Medium, and further for Low, and thus assigns performance evaluation for each occupant's position.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Ann_CS_N0: (if precached) Link to CSV file from pre-cached folder containing Annual hourly CS, facing north.
        Ann_CS_E0: (if precached) Link to CSV file from pre-cached folder containing Annual hourly CS, facing east.
        Ann_CS_S0: (if precached) Link to CSV file from pre-cached folder containing Annual hourly CS, facing south.
        Ann_CS_W0: (if precached) Link to CSV file from pre-cached folder containing Annual hourly CS, facing west.
        Ann_CS_N: (if live simulation) Link to calculated CSV file containing Annual hourly CS, facing north.
        Ann_CS_E: (if live simulation) Link to calculated CSV file containing Annual hourly CS, facing east.
        Ann_CS_S: (if live simulation) Link to calculated CSV file containing Annual hourly CS, facing south.
        Ann_CS_W: (if live simulation) Link to calculated CSV file containing Annual hourly CS, facing west.
        Time_SOB: Start of business each day (eg: 9)
        Time_COB: Close of business each day (eg: 18)
        Days_Week: Working days each week (eg: 5)
        Wknd_OfSt: (Weekend offset) definition of working weeks. If the first day of the year is Sunday, this parameter is 0. If any other day, this parameter is the difference between that day and Sunday (eg: 3, if 1 Jan was Wednesday). 
        thrCS_min: Threshold for Non visual performance - Minimum. Default is set at 0.35 (CS) but user can choose a different number for minimum threshold.
        thrCS_med: Threshold for Non visual performance - Medium. Default is set at 0.50 (CS) but user can choose a different number for medium threshold.
        thrCS_high:Threshold for Non visual performance - High. Default is 0.65 (CS) but user can choose a different number for high threshold.
        numDays: Percentage annual occupied days as threshold for compliance. Default is set at 75 (as in, minimum 75% of occupied days) but user can choose a different time threshold.
        runIt: A boolean Toggle for running this component. True = Live, False = Precached
    Output:
        CS_Aut_N: The non-visual potential/performance of each occupant-position, facing North (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)
        CS_Aut_E: The non-visual potential/performance of each occupant-position, facing East (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)
        CS_Aut_S: The non-visual potential/performance of each occupant-position, facing South (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)
        CS_Aut_W: The non-visual potential/performance of each occupant-position, facing West (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)"""


import rhinoscriptsyntax as rs
import csv
import copy
import os
import random
self=ghenv.Component
self.Name = "SCALE_Vert2SPrc"
self.NickName = 'Vert2SPrc'
self.Message = 'AnnuOWL | Vert2SPrc\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

if runIt==True:
    Ann_CS_Files=[Ann_CS_N,Ann_CS_E,Ann_CS_S,Ann_CS_W]
    folder=os.path.dirname(Ann_CS_N)
else:
    Ann_CS_Files=[Ann_CS_N0,Ann_CS_E0,Ann_CS_S0,Ann_CS_W0]
    folder=os.path.dirname(Ann_CS_N0)

print(folder)
os.chdir(folder)
if  os.path.isfile(folder+"/annualR_N.ill")==True:
    print ("Removing the .ill file")
    os.remove("annualR_N.ill")
else:
    print("No .ill file to remove")
if  os.path.isfile(folder+"/annualR_E.ill")==True:
    print ("Removing the .ill file")
    os.remove("annualR_E.ill")
else:
    print("No .ill file to remove")
if  os.path.isfile(folder+"/annualR_S.ill")==True:
    print ("Removing the .ill file")
    os.remove("annualR_S.ill")
else:
    print("No .ill file to remove")
if  os.path.isfile(folder+"/annualR_W.ill")==True:
    print ("Removing the .ill file")
    os.remove("annualR_W.ill")
else:
    print("No .ill file to remove")

OutFiles=['/CSautonomyN.csv','/CSautonomyE.csv','/CSautonomyS.csv','/CSautonomyW.csv']

if True:
    Time_SOB=9 if Time_SOB is None else int(Time_SOB)
    Time_COB=17 if Time_COB is None else int(Time_COB)
    Days_Week=5 if Days_Week is None else int(Days_Week)
    Wknd_OfSt=0 if Wknd_OfSt is None else int(Wknd_OfSt)
    thrCS_min=0.3499 if thrCS_min is None else float(thrCS_min)
    thrCS_med=0.4999 if thrCS_med is None else float(thrCS_med)
    thrCS_high=0.6499 if thrCS_high is None else float(thrCS_high)
    numDays=0.75 if numDays is None else float(numDays)/100
    hrthresh=numDays
    if Wknd_OfSt>6:
        Wknd_OfSt=6
    if Wknd_OfSt<0:
        Wknd_OfSt=0
    Hours_business=(Time_COB)-(Time_SOB)
    Annual_Hours=365*Hours_business
    for i in range(0,4,1):
        Ann_CS=Ann_CS_Files[i]
        OutFile=OutFiles[i]
        folder=os.path.dirname(Ann_CS)+"/"
        CS_data=Ann_CS
        rows_Cillumx = []
        with open(CS_data, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows_Cillumx.append(row)
        rows_Cillum=[[float(i) for i in j] for j in rows_Cillumx]
        CS_Amin=[[0 for i in j] for j in rows_Cillumx]
        CS_Amed=[[0 for i in j] for j in rows_Cillumx]
        CS_Ahigh=[[0 for i in j] for j in rows_Cillumx]
        OpenHourCount=0
        OpenDayCount=0
        print(len(rows_Cillum))
        for i in range (len(rows_Cillum)):
            DayNum=int(i/24)+1
            WeekNum=int((DayNum-1)/7)+1
            #print(DayNum)
            DayofWeek=(DayNum-1)-(7*(WeekNum-1))+1
            HourNum=i-(24*(DayNum-1))
            mod_DWk=DayofWeek+Wknd_OfSt
            if mod_DWk>7:
                Md_DWk=mod_DWk-7
            else:
                Md_DWk=mod_DWk
            #print(DayNum,WeekNum,DayofWeek,Md_DWk,HourNum)
            if Days_Week>(Md_DWk-1):
                OpenDayCount=OpenDayCount+1
                if (Time_SOB-1)<HourNum<(Time_COB+1):
                    OpenHourCount=OpenHourCount+1
#                    print(OpenHourCount,"This is counted as an Occupancy hour")
                    for j in range (len(rows_Cillum[0])):
                        if rows_Cillum[i][j]>thrCS_high:
                            CS_Ahigh[i][j]=1
                            CS_Amed[i][j]=1
                            CS_Amin[i][j]=1
                        elif rows_Cillum[i][j]>thrCS_med:
                            CS_Ahigh[i][j]=0
                            CS_Amed[i][j]=1
                            CS_Amin[i][j]=1
                        elif rows_Cillum[i][j]>thrCS_min:
                            CS_Ahigh[i][j]=0
                            CS_Amed[i][j]=0
                            CS_Amin[i][j]=1
                        else:
                            CS_Ahigh[i][j]=0
                            CS_Amed[i][j]=0
                            CS_Amin[i][j]=0
                else:
                    for j in range (len(rows_Cillum[0])):
                        CS_Amin[i][j]=0
                        CS_Amed[i][j]=0
                        CS_Ahigh[i][j]=0
            else:
                for j in range (len(rows_Cillum[0])):
                    CS_Amin[i][j]=0
                    CS_Amed[i][j]=0
                    CS_Ahigh[i][j]=0
        daily_CSAmin=[[0 for i in range (len(rows_Cillum[0]))]for j in range(365)] 
        daily_CSAmed=[[0 for i in range (len(rows_Cillum[0]))]for j in range(365)] 
        daily_CSAhigh=[[0 for i in range (len(rows_Cillum[0]))]for j in range(365)] 

    
        for i in range (len(rows_Cillum[0])):
            for j in range (365):
                for k in range(8,13,1):
                    hcount=24*j+k
                    daily_CSAmin[j][i]=daily_CSAmin[j][i]+CS_Amin[hcount][i]
                    daily_CSAmed[j][i]=daily_CSAmed[j][i]+CS_Amed[hcount][i]
                    daily_CSAhigh[j][i]=daily_CSAhigh[j][i]+CS_Ahigh[hcount][i]
    
        daily_CSAmin_credit=[[0 for i in range (len(rows_Cillum[0]))]for j in range(365)] 
        daily_CSAmed_credit=[[0 for i in range (len(rows_Cillum[0]))]for j in range(365)] 
        daily_CSAhigh_credit=[[0 for i in range (len(rows_Cillum[0]))]for j in range(365)] 
        
        for i in range (len(rows_Cillum[0])):
            for j in range(365):
                if daily_CSAmin[j][i]>0:
                    daily_CSAmin_credit[j][i]=1
                if daily_CSAmed[j][i]>0:
                    daily_CSAmed_credit[j][i]=1
                if daily_CSAhigh[j][i]>0:
                    daily_CSAhigh_credit[j][i]=1

        ann_CSAmin= [0 for i in range (len(rows_Cillum[0]))]
        ann_CSAmed= [0 for i in range (len(rows_Cillum[0]))]
        ann_CSAhigh= [0 for i in range (len(rows_Cillum[0]))]
        ann_CSA_cred= [0 for i in range (len(rows_Cillum[0]))]
    
        for i in range(len(rows_Cillum[0])):
            for j in range(365):
                ann_CSAmin[i]=(ann_CSAmin[i]+daily_CSAmin_credit[j][i]) 
                ann_CSAmed[i]=(ann_CSAmed[i]+daily_CSAmed_credit[j][i]) 
                ann_CSAhigh[i]=(ann_CSAhigh[i]+daily_CSAhigh_credit[j][i]) 

        ann_CSAminnorm=[float(i) for i in ann_CSAmin]
        ann_CSAmednorm=[float(i) for i in ann_CSAmed]
        ann_CSAhighnorm=[float(i) for i in ann_CSAhigh]
        metrix_CS=[]
        metrix_CS.append(ann_CSAminnorm)
        metrix_CS.append(ann_CSAmednorm)
        metrix_CS.append(ann_CSAhighnorm)
        with open(folder+OutFile, 'wb') as f: 
            write = csv.writer(f) 
            write.writerows(metrix_CS) 

    print(OpenHourCount)
    print(OpenDayCount)
    Open_DayCount=int(OpenDayCount/24)
    print(Open_DayCount)

#    DayCount=365
    CSN_dat=[]
    with open(folder+'/CSautonomyN.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            CSN_dat.append(row)
    CSarrN_min=CSN_dat[0]
    CSarrN_med=CSN_dat[1]
    CSarrN_high=CSN_dat[2]
    CSNa=[float(i)/Open_DayCount for i in CSarrN_min]
    CSNb=[float(i)/Open_DayCount for i in CSarrN_med]
    CSNc=[float(i)/Open_DayCount for i in CSarrN_high]
    CScNa=[0 for i in range (len(CSNa))]
    CScNb=[0 for i in range (len(CSNb))]
    CScNc=[0 for i in range (len(CSNc))]
    CSCr_N=[0 for i in range (len(CSNc))]
    for i in range(len(CSNa)):
        if CSNa[i]>hrthresh:  
            CScNa[i]=1
        else:
            CScNa[i]=0
        if CSNb[i]>hrthresh: 
            CScNb[i]=1
        else:
            CScNb[i]=0
        if CSNc[i]>hrthresh: 
            CScNc[i]=1
        else:
            CScNc[i]=0
    for i in range(len(CSNa)):
        if CScNc[i]==1:
            CSCr_N[i]=3
        elif CScNb[i]==1:
            CSCr_N[i]=2
        elif CScNa[i]==1:
            CSCr_N[i]=1
        else:
            CSCr_N[i]=0
    CS_Aut_N=[float(i) for i in CSCr_N]

    CSE_dat=[]
    with open(folder+'/CSautonomyE.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            CSE_dat.append(row)
    CSarrE_min=CSE_dat[0]
    CSarrE_med=CSE_dat[1]
    CSarrE_high=CSE_dat[2]
    CSEa=[float(i)/Open_DayCount for i in CSarrE_min]
    CSEb=[float(i)/Open_DayCount for i in CSarrE_med]
    CSEc=[float(i)/Open_DayCount for i in CSarrE_high]
    CScEa=[0 for i in range (len(CSEa))]
    CScEb=[0 for i in range (len(CSEb))]
    CScEc=[0 for i in range (len(CSEc))]
    CSCr_E=[0 for i in range (len(CSEc))]
    for i in range(len(CSEa)):
        if CSEa[i]>hrthresh:  
            CScEa[i]=1
        else:
            CScEa[i]=0
        if CSEb[i]>hrthresh: 
            CScEb[i]=1
        else:
            CScEb[i]=0
        if CSEc[i]>hrthresh: 
            CScEc[i]=1
        else:
            CScEc[i]=0
    for i in range(len(CSEa)):
        if CScEc[i]==1:
            CSCr_E[i]=3
        elif CScEb[i]==1:
            CSCr_E[i]=2
        elif CScEa[i]==1:
            CSCr_E[i]=1
        else:
            CSCr_E[i]=0
    CS_Aut_E=[float(i) for i in CSCr_E]

    CSS_dat=[]
    with open(folder+'/CSautonomyS.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            CSS_dat.append(row)
    CSarrS_min=CSS_dat[0]
    CSarrS_med=CSS_dat[1]
    CSarrS_high=CSS_dat[2]
    CSSa=[float(i)/Open_DayCount for i in CSarrS_min]
    CSSb=[float(i)/Open_DayCount for i in CSarrS_med]
    CSSc=[float(i)/Open_DayCount for i in CSarrS_high]
    CScSa=[0 for i in range (len(CSSa))]
    CScSb=[0 for i in range (len(CSSb))]
    CScSc=[0 for i in range (len(CSSc))]
    CSCr_S=[0 for i in range (len(CSSc))]
    for i in range(len(CSSa)):
        if CSSa[i]>hrthresh:  
            CScSa[i]=1
        else:
            CScSa[i]=0
        if CSSb[i]>hrthresh: 
            CScSb[i]=1
        else:
            CScSb[i]=0
        if CSSc[i]>hrthresh: 
            CScSc[i]=1
        else:
            CScSc[i]=0
    for i in range(len(CSSa)):
        if CScSc[i]==1:
            CSCr_S[i]=3
        elif CScSb[i]==1:
            CSCr_S[i]=2
        elif CScSa[i]==1:
            CSCr_S[i]=1
        else:
            CSCr_S[i]=0
    CS_Aut_S=[float(i) for i in CSCr_S]

    CSW_dat=[]
    with open(folder+'/CSautonomyW.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            CSW_dat.append(row)
    CSarrW_min=CSW_dat[0]
    CSarrW_med=CSW_dat[1]
    CSarrW_high=CSW_dat[2]
    CSWa=[float(i)/Open_DayCount for i in CSarrW_min]
    CSWb=[float(i)/Open_DayCount for i in CSarrW_med]
    CSWc=[float(i)/Open_DayCount for i in CSarrW_high]
    CScWa=[0 for i in range (len(CSWa))]
    CScWb=[0 for i in range (len(CSWb))]
    CScWc=[0 for i in range (len(CSWc))]
    CSCr_W=[0 for i in range (len(CSWc))]
    for i in range(len(CSWa)):
        if CSWa[i]>hrthresh:  
            CScWa[i]=1
        else:
            CScWa[i]=0
        if CSWb[i]>hrthresh: 
            CScWb[i]=1
        else:
            CScWb[i]=0
        if CSWc[i]>hrthresh: 
            CScWc[i]=1
        else:
            CScWc[i]=0
    for i in range(len(CSWa)):
        if CScWc[i]==1:
            CSCr_W[i]=3
        elif CScWb[i]==1:
            CSCr_W[i]=2
        elif CScWa[i]==1:
            CSCr_W[i]=1
        else:
            CSCr_W[i]=0
    CS_Aut_W=[float(i) for i in CSCr_W]