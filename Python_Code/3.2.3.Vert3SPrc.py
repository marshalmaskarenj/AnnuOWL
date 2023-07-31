"""This component takes in the Annual sDGP for each hour (by reading CSV files for live or pre-cached simulations) for 4 orientations, takes in occupancy hours (SOB, COB, Days of week) and bins the glare protection performance into High, Medium, Minimum and non compliant based on the defined thresholds.
Further, at the occupant position level, if any positions glare protection performance for defined percent of occupied hours does not qualify for High, then it checks for Medium, and further for Low, and thus assigns performance evaluation for each occupant's position.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Ann_DGP_N0: (if precached) Link to CSV file from pre-cached folder containing Annual hourly DGP, facing north.
        Ann_DGP_E0: (if precached) Link to CSV file from pre-cached folder containing Annual hourly DGP, facing east.
        Ann_DGP_S0: (if precached) Link to CSV file from pre-cached folder containing Annual hourly DGP, facing south.
        Ann_DGP_W0: (if precached) Link to CSV file from pre-cached folder containing Annual hourly DGP, facing west.
        Ann_DGP_N: (if live simulation) Link to calculated CSV file containing Annual hourly DGP, facing north.
        Ann_DGP_E: (if live simulation) Link to calculated CSV file containing Annual hourly DGP, facing east.
        Ann_DGP_S: (if live simulation) Link to calculated CSV file containing Annual hourly DGP, facing south.
        Ann_DGP_W: (if live simulation) Link to calculated CSV file containing Annual hourly DGP, facing west.
        Time_SOB: Start of business each day (eg: 9)
        Time_COB: Close of business each day (eg: 18)
        Days_Week: Working days each week (eg: 5)
        Wknd_OfSt: (Weekend offset) definition of working weeks. If the first day of the year is Sunday, this parameter is 0. If any other day, this parameter is the difference between that day and Sunday (eg: 3, if 1 Jan was Wednesday). 
        thrG_min: Threshold for occupied-hourly glare protection performance - Minimum. Default is set at 0.45 (DGP) based on EN17037 but user can choose a different number for minimum threshold.
        thrG_med: Threshold for occupied-hourly glare protection performance - Medium. Default is set at 0.40 (DGP) based on EN17037 but user can choose a different number for medium threshold.
        thrG_high:Threshold for occupied-hourly glare protection performance - High. Default is 0.35 (DGP) based on EN17037 but user can choose a different number for high threshold.
        numHours: Percentage annual occupied hours as threshold for compliance. Default is set at 95 (as in, minimum 95% of occupied hours) based on EN17037, but user can choose a different time threshold.
        runIt: A boolean Toggle for running this component. True = Live, False = Precached
    Output:
        sDGP_N: The glare protection performance for each occupant-position, facing North (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)
        sDGP_E: The glare protection performance for each occupant-position, facing East (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)
        sDGP_S: The glare protection performance for each occupant-position, facing South (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)
        sDGP_W: The glare protection performance for each occupant-position, facing West (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)"""


import rhinoscriptsyntax as rs
import csv
import copy
import os
self=ghenv.Component
self.Name = "SCALE_Vert3SPrc"
self.NickName = 'Vert3SPrc'
self.Message = 'AnnuOWL | Vert3SPrc\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

if runIt==True:
    Ann_DGP_Files=[Ann_DGP_N,Ann_DGP_E,Ann_DGP_S,Ann_DGP_W]
    folder=os.path.dirname(Ann_DGP_N)+"/"
else:
    Ann_DGP_Files=[Ann_DGP_N0,Ann_DGP_E0,Ann_DGP_S0,Ann_DGP_W0]
    folder=os.path.dirname(Ann_DGP_N0)+"/"

OutFiles=['/AnnSGDP_N.csv','/AnnSGDP_E.csv','/AnnSGDP_S.csv','/AnnSGDP_W.csv']

if True:
    Time_SOB=9 if Time_SOB is None else int(Time_SOB)
    Time_COB=17 if Time_COB is None else int(Time_COB)
    Days_Week=5 if Days_Week is None else int(Days_Week)
    Wknd_OfSt=0 if Wknd_OfSt is None else int(Wknd_OfSt)
    thrG_min = 0.45 if thrG_min is None else float(thrG_min)
    thrG_med = 0.40 if thrG_med is None else float(thrG_med)
    thrG_high = 0.35 if thrG_high is None else float(thrG_high)
    numHours=0.95 if numHours is None else float(numHours)/100
    hrthresh=numHours
    if Wknd_OfSt>6:
        Wknd_OfSt=6
    if Wknd_OfSt<0:
        Wknd_OfSt=0
    Hours_business=(Time_COB)-(Time_SOB)
    Annual_Hours=365*Hours_business

    for ii in range(0,4,1):
        Ann_DGP=Ann_DGP_Files[ii]
        OutFile=OutFiles[ii]
#        folder=os.path.dirname(Ann_DGP)+"/"
        DGP_data=Ann_DGP
        rows_DGPlumx = []
        with open(DGP_data, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows_DGPlumx.append(row)
        rows_DGPlum=[[float(i) for i in j] for j in rows_DGPlumx]
        DGP_A=[[0 for i in j] for j in rows_DGPlumx]
        DGP_Amin=[[0 for i in j] for j in rows_DGPlumx]
        DGP_Amed=[[0 for i in j] for j in rows_DGPlumx]
        DGP_Ahigh=[[0 for i in j] for j in rows_DGPlumx]
        OpenHourCount=0
        for i in range (len(rows_DGPlum)):
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
            for j in range (len(rows_DGPlum[0])):
                if rows_DGPlum[i][j]>0.4199: #DGP is disturbing above 0.42, refer https://www.radiance-online.org/community/workshops/2014-london/presentations/day1/Wienold_glare_rad.pdf
                    DGP_A[i][j]=1
                else:
                    DGP_A[i][j]=0

            if Days_Week>(Md_DWk-1):
                if (Time_SOB-1)<HourNum<(Time_COB+1):
                    OpenHourCount=OpenHourCount+1
#                    print(OpenHourCount,"This is counted as an Occupancy hour")
                    for j in range (len(rows_DGPlum[0])):
                        if rows_DGPlum[i][j]<thrG_high: #thrG_high = 0.35
                            DGP_Amin[i][j]=1
                            DGP_Amed[i][j]=1
                            DGP_Ahigh[i][j]=1
                        elif rows_DGPlum[i][j]<thrG_med: #thrG_med = 0.40
                            DGP_Amin[i][j]=1
                            DGP_Amed[i][j]=1
                            DGP_Ahigh[i][j]=0
                        elif rows_DGPlum[i][j]<thrG_min: #thrG_min = 0.45
                            DGP_Amin[i][j]=1
                            DGP_Amed[i][j]=0
                            DGP_Ahigh[i][j]=0
                        else:
                            DGP_Amin[i][j]=0
                            DGP_Amed[i][j]=0
                            DGP_Ahigh[i][j]=0
                else:
                    for j in range (len(rows_DGPlum[0])):
                        DGP_Amin[i][j]=0
                        DGP_Amed[i][j]=0
                        DGP_Ahigh[i][j]=0
            else:
                for j in range (len(rows_DGPlum[0])):
                    DGP_Amin[i][j]=0
                    DGP_Amed[i][j]=0
                    DGP_Ahigh[i][j]=0
        ann_DGPA= [0 for i in range (len(rows_DGPlum[0]))]
        ann_DGPAmin= [0 for i in range (len(rows_DGPlum[0]))]
        ann_DGPAmed= [0 for i in range (len(rows_DGPlum[0]))]
        ann_DGPAhigh= [0 for i in range (len(rows_DGPlum[0]))]
        for i in range (len(rows_DGPlum[0])):
            for j in range (8760):
                ann_DGPA[i]=ann_DGPA[i]+DGP_A[j][i]
                ann_DGPAmin[i]=ann_DGPAmin[i]+DGP_Amin[j][i]
                ann_DGPAmed[i]=ann_DGPAmed[i]+DGP_Amed[j][i]
                ann_DGPAhigh[i]=ann_DGPAhigh[i]+DGP_Ahigh[j][i]
        metrix_DGP=[]
        metrix_DGPmin=[]
        metrix_DGPmed=[]
        metrix_DGPhigh=[]
        metrix_DGP.append(ann_DGPA)
        metrix_DGPmin.append(ann_DGPAmin)
        metrix_DGPmed.append(ann_DGPAmed)
        metrix_DGPhigh.append(ann_DGPAhigh)
        with open(folder+OutFile, 'wb') as f: 
            write = csv.writer(f) 
            write.writerows(metrix_DGP)
            write.writerows(metrix_DGPmin)
            write.writerows(metrix_DGPmed)
            write.writerows(metrix_DGPhigh)

    OccupHrs=OpenHourCount


    DGPN_dat=[]
    with open(folder+'/AnnSGDP_N.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            DGPN_dat.append(row)
    sDGParrN=DGPN_dat[0]
    sDGParrN_min=DGPN_dat[1]
    sDGParrN_med=DGPN_dat[2]
    sDGParrN_high=DGPN_dat[3]
    GNa=[float(i)/OpenHourCount for i in sDGParrN_min]
    GNb=[float(i)/OpenHourCount for i in sDGParrN_med]
    GNc=[float(i)/OpenHourCount for i in sDGParrN_high]
    GcNa=[0 for i in range (len(GNa))]
    GcNb=[0 for i in range (len(GNb))]
    GcNc=[0 for i in range (len(GNc))]
    GCr_N=[0 for i in range (len(GNc))]
    for i in range(len(GNa)):
        if GNa[i]>hrthresh:  #more than 95% occupancy hours NOT having instances of glare (respectively 0.35, 0.4 or 0.45) according to EN17037, which is the same as less than 5% occupancy hours having respective instances of glare
            GcNa[i]=1
        else:
            GcNa[i]=0
        if GNb[i]>hrthresh: 
            GcNb[i]=1
        else:
            GcNb[i]=0
        if GNc[i]>hrthresh: 
            GcNc[i]=1
        else:
            GcNc[i]=0
    for i in range(len(GNa)):
        if GcNc[i]==1:
            GCr_N[i]=3
        elif GcNb[i]==1:
            GCr_N[i]=2
        elif GcNa[i]==1:
            GCr_N[i]=1
        else:
            GCr_N[i]=0
    sDGP_N=[int(i) for i in GCr_N]

    DGPE_dat=[]
    with open(folder+'/AnnSGDP_E.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            DGPE_dat.append(row)
    sDGParrE=DGPE_dat[0]
    sDGParrE_min=DGPE_dat[1]
    sDGParrE_med=DGPE_dat[2]
    sDGParrE_high=DGPE_dat[3]
    GEa=[float(i)/OpenHourCount for i in sDGParrE_min]
    GEb=[float(i)/OpenHourCount for i in sDGParrE_med]
    GEc=[float(i)/OpenHourCount for i in sDGParrE_high]
    GcEa=[0 for i in range (len(GEa))]
    GcEb=[0 for i in range (len(GEb))]
    GcEc=[0 for i in range (len(GEc))]
    GCr_E=[0 for i in range (len(GEc))]
    for i in range(len(GEa)):
        if GEa[i]>hrthresh:  #more than 95% occupancy hours NOT having instances of glare (respectively 0.35, 0.4 or 0.45) according to EE17037, which is the same as less than 5% occupancy hours having respective instances of glare
            GcEa[i]=1
        else:
            GcEa[i]=0
        if GEb[i]>hrthresh: 
            GcEb[i]=1
        else:
            GcEb[i]=0
        if GEc[i]>hrthresh: 
            GcEc[i]=1
        else:
            GcEc[i]=0
    for i in range(len(GEa)):
        if GcEc[i]==1:
            GCr_E[i]=3
        elif GcEb[i]==1:
            GCr_E[i]=2
        elif GcEa[i]==1:
            GCr_E[i]=1
        else:
            GCr_E[i]=0
    sDGP_E=[int(i) for i in GCr_E]

    DGPS_dat=[]
    with open(folder+'/AnnSGDP_S.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            DGPS_dat.append(row)
    sDGParrS=DGPS_dat[0]
    sDGParrS_min=DGPS_dat[1]
    sDGParrS_med=DGPS_dat[2]
    sDGParrS_high=DGPS_dat[3]
    GSa=[float(i)/OpenHourCount for i in sDGParrS_min]
    GSb=[float(i)/OpenHourCount for i in sDGParrS_med]
    GSc=[float(i)/OpenHourCount for i in sDGParrS_high]
    GcSa=[0 for i in range (len(GSa))]
    GcSb=[0 for i in range (len(GSb))]
    GcSc=[0 for i in range (len(GSc))]
    GCr_S=[0 for i in range (len(GSc))]
    for i in range(len(GSa)):
        if GSa[i]>hrthresh:  #more than 95% occupancy hours NOT having instances of glare (respectively 0.35, 0.4 or 0.45) according to ES17037, which is the same as less than 5% occupancy hours having respective instances of glare
            GcSa[i]=1
        else:
            GcSa[i]=0
        if GSb[i]>hrthresh: 
            GcSb[i]=1
        else:
            GcSb[i]=0
        if GSc[i]>hrthresh: 
            GcSc[i]=1
        else:
            GcSc[i]=0
    for i in range(len(GSa)):
        if GcSc[i]==1:
            GCr_S[i]=3
        elif GcSb[i]==1:
            GCr_S[i]=2
        elif GcSa[i]==1:
            GCr_S[i]=1
        else:
            GCr_S[i]=0
    sDGP_S=[int(i) for i in GCr_S]

    DGPW_dat=[]
    with open(folder+'/AnnSGDP_W.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            DGPW_dat.append(row)
    sDGParrW=DGPW_dat[0]
    sDGParrW_min=DGPW_dat[1]
    sDGParrW_med=DGPW_dat[2]
    sDGParrW_high=DGPW_dat[3]
    GWa=[float(i)/OpenHourCount for i in sDGParrW_min]
    GWb=[float(i)/OpenHourCount for i in sDGParrW_med]
    GWc=[float(i)/OpenHourCount for i in sDGParrW_high]
    GcWa=[0 for i in range (len(GWa))]
    GcWb=[0 for i in range (len(GWb))]
    GcWc=[0 for i in range (len(GWc))]
    GCr_W=[0 for i in range (len(GWc))]
    for i in range(len(GWa)):
        if GWa[i]>hrthresh:  #more than 95% occupancy hours NOT having instances of glare (respectively 0.35, 0.4 or 0.45) according to EW17037, which is the same as less than 5% occupancy hours having respective instances of glare
            GcWa[i]=1
        else:
            GcWa[i]=0
        if GWb[i]>hrthresh: 
            GcWb[i]=1
        else:
            GcWb[i]=0
        if GWc[i]>hrthresh: 
            GcWc[i]=1
        else:
            GcWc[i]=0
    for i in range(len(GWa)):
        if GcWc[i]==1:
            GCr_W[i]=3
        elif GcWb[i]==1:
            GCr_W[i]=2
        elif GcWa[i]==1:
            GCr_W[i]=1
        else:
            GCr_W[i]=0
    sDGP_W=[int(i) for i in GCr_W]