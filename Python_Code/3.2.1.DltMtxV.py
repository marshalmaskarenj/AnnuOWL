"""[If running Live simulation] This component takes the horizontal illuminance data for each occupant's position for each hour of the year (from AnnIllV component), along with occupancy hours parameters (SoB, CoB, etc), as well as user defined thresholds for minimum, medium and high targets (such as for EN17037), and evaluates the spatial daylight autonomy (Target - Min/Med/High or custom) for each occupant's position.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Ann_illH: The CSV file containing hourly annual illuminance, generated for each occpant's position by the AnnIllV component.
        Time_SOB: Start of business each day (eg: 9)
        Time_COB: Close of business each day (eg: 18)
        Days_Week: Working days each week (eg: 5)
        Wknd_OfSt: (Weekend offset) definition of working weeks. If the first day of the year is Sunday, this parameter is 0. If any other day, this parameter is the difference between that day and Sunday (eg: 3, if 1 Jan was Wednesday). 
        thr_min: Threshold for Daylight Autonomy - Minimum (eg: by EN17037 Target/Minimum). Default is 300 (lux) but user can choose a different number for minimum threshold.
        thr_med: Threshold for Daylight Autonomy - Medium (eg: by EN17037 Target/Medium). Default is 500 (lux) but user can choose a different number for medium threshold.
        thr_high: Threshold for Daylight Autonomy - High (eg: by EN17037 Target/High). Default is 750 (lux) but user can choose a different number for high threshold.        
        runIt: A boolean Toggle for running this component. FALSE = cached data (this component does not run)
    Output:
        DltMtx: Link to the CSV file containing calculated sDA parameters for the defined minimum, medium, high thresholds.
        OccupHrs: Occupied hours of the year, depending upon user defined parameters (SOB, COB, etc.)
        OpenSched: Occupancy schedule through the 8760 hours, where 1 = occupied and 0 = unoccupied"""


import rhinoscriptsyntax as rs
import csv
import copy
import os
self=ghenv.Component
self.Name = "SCALE_DltMtxV"
self.NickName = 'DltMtxV'
self.Message = 'AnnuOWL | DltMtxV\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

if runIt==True:
    Time_SOB=9 if Time_SOB is None else int(Time_SOB)
    Time_COB=17 if Time_COB is None else int(Time_COB)
    Days_Week=5 if Days_Week is None else int(Days_Week)
    Wknd_OfSt=0 if Wknd_OfSt is None else int(Wknd_OfSt)
    thr_min=300 if thr_min is None else int(thr_min)
    thr_med=500 if thr_med is None else int(thr_med)
    thr_high=750 if thr_high is None else int(thr_high)
    if Wknd_OfSt>6:
        Wknd_OfSt=6
    if Wknd_OfSt<0:
        Wknd_OfSt=0
    Hours_business=(Time_COB)-(Time_SOB)
    Annual_Hours=365*Hours_business
    print(Annual_Hours)
    print(Time_SOB, Time_COB)
    file1=Ann_ilH
    folder=os.path.dirname(Ann_ilH)+"/"
    rows_illumx = []
    with open(file1, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_illumx.append(row)
    rows_illum=[[float(i) for i in j] for j in rows_illumx]
    print(len(rows_illum), len(rows_illum[0]))
    DA=[[0 for i in range (len(rows_illum[0]))]for j in range (len(rows_illum))]
    cDA=[[0 for i in range (len(rows_illum[0]))]for j in range (len(rows_illum))]
    UDI=[[0 for i in range (len(rows_illum[0]))]for j in range (len(rows_illum))]
    minDA=[[0 for i in range (len(rows_illum[0]))]for j in range (len(rows_illum))]
    medDA=[[0 for i in range (len(rows_illum[0]))]for j in range (len(rows_illum))]
    highDA=[[0 for i in range (len(rows_illum[0]))]for j in range (len(rows_illum))]
    OpenHourCount=0
    Occupancy_Array=[0 for i in range (8760)]
    for i in range (len(rows_illum)):
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
            if (Time_SOB-1)<HourNum<(Time_COB+1):
                OpenHourCount=OpenHourCount+1
#                print(OpenHourCount,"This is counted as an Occupancy hour")
                Occupancy_Array[i]=1
                for j in range (len(rows_illum[0])):
                    if rows_illum[i][j]<=100:
                        DA[i][j]=0
                        cDA[i][j]=(rows_illum[i][j])/300
                        UDI[i][j]=0
                    elif 100<rows_illum[i][j]<=300:
                        DA[i][j]=0
                        cDA[i][j]=(rows_illum[i][j])/300
                        UDI[i][j]=1
                    elif 300<rows_illum[i][j]<=2000:
                        DA[i][j]=1
                        cDA[i][j]=1
                        UDI[i][j]=1
                    else: #more than 2000
                        DA[i][j]=1
                        cDA[i][j]=1
                        UDI[i][j]=0
                for j in range (len(rows_illum[0])): # the part below follows EN17037 logic of binning/credits based on point-in-time illuminance, for minimum(Target), medium(Target) and maximum(Target)
                    if rows_illum[i][j]<=thr_min:
                        minDA[i][j]=0
                        medDA[i][j]=0
                        highDA[i][j]=0
                    elif thr_min<rows_illum[i][j]<=thr_med:
                        minDA[i][j]=1
                        medDA[i][j]=0
                        highDA[i][j]=0
                    elif thr_med<rows_illum[i][j]<=thr_high:
                        minDA[i][j]=1
                        medDA[i][j]=1
                        highDA[i][j]=0
                    else:
                        minDA[i][j]=1
                        medDA[i][j]=1
                        highDA[i][j]=1
            else:
                for j in range (len(rows_illum[0])):
                    DA[i][j]=0
                    cDA[i][j]=0
                    UDI[i][j]=0
                    minDA[i][j]=0
                    medDA[i][j]=0
                    highDA[i][j]=0
        else:
            for j in range (len(rows_illum[0])):
                DA[i][j]=0
                cDA[i][j]=0
                UDI[i][j]=0
                minDA[i][j]=0
                medDA[i][j]=0
                highDA[i][j]=0
    ann_DA= [0 for i in range (len(rows_illum[0]))]
    ann_cDA= [0 for i in range (len(rows_illum[0]))]
    ann_UDI= [0 for i in range (len(rows_illum[0]))]
    ann_avgI=[0 for i in range (len(rows_illum[0]))]
    ann_minDA= [0 for i in range (len(rows_illum[0]))]
    ann_medDA= [0 for i in range (len(rows_illum[0]))]
    ann_highDA= [0 for i in range (len(rows_illum[0]))]
    OHC_array=[0 for i in range (len(rows_illum[0]))]
    metrix_m=[]
    for i in range (len(rows_illum[0])):
        for j in range (len(rows_illum)):
            ann_DA[i]=ann_DA[i]+DA[j][i]
            ann_cDA[i]=ann_cDA[i]+cDA[j][i]
            ann_UDI[i]=ann_UDI[i]+UDI[j][i]
            ann_avgI[i]=ann_avgI[i]+rows_illum[j][i]
            ann_minDA[i]=ann_minDA[i]+minDA[j][i]
            ann_medDA[i]=ann_medDA[i]+medDA[j][i]
            ann_highDA[i]=ann_highDA[i]+highDA[j][i]
            OHC_array[i]=OpenHourCount
    ann_cDA=[int(i) for i in ann_cDA]
    ann_avgI=[int(i/8760) for i in ann_avgI]
    metrix_m.append(ann_DA)
    metrix_m.append(ann_cDA)
    metrix_m.append(ann_UDI)
    metrix_m.append(ann_avgI)
    metrix_m.append(ann_minDA)
    metrix_m.append(ann_medDA)
    metrix_m.append(ann_highDA)
    metrix_m.append(OHC_array)
    OcAr=[]
    OcAr.append(Occupancy_Array)
    #print(Occupancy_Array)
    #print(OcAr)
    with open(folder+'/ann_PtMetrics.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(metrix_m) 
    with open(folder+'/Occupancy.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(OcAr) 
    DltMtx=folder+'/ann_PtMetrics.csv'
    OccupHrs=OpenHourCount
    
    rows_OcAr=[]
    with open(folder+'/Occupancy.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_OcAr.append(row)
    
    OpenSched=rows_OcAr[0]
    
#    OpenSched=Occupancy_Array

