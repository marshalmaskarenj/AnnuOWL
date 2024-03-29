"""This component isolates Daylight Metrics from the computed CSV file into various thresholds, and processes the data to evaluate how each occupant position performs, as High, Medium or Low Performance, or as Non-compliant. 
If any gridpoint, for defined percent of occupied hours does not qualify for High, then it checks for Medium, and firther for Low, and thus assigns performance evaluation for each occupant's position.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        DltMtx_0: (if pre-cached) Link to CSV file from pre-cached folder containing threshold binned data, generated by DltMtxV component.
        OccupHrs_0: (if pre-cached) Number of occupied hours of the pre-simulated data.
        DltMtx: (if live simulation) Link to CSV file containing threshold-binned data, generated by DltMtxV component.
        OccupHrs: (if live simulation) Number of occupied hours calculated from user defined parameters (SOB, COB, Days of Week).
        numHours: Percentage annual occupied hours as threshold for compliance (eg: 50 for EN17037 Target, 95 for EN17037 Minimum 
        runIt: a boolean switch for running this component. Set to TRUE.
    Output:
        ENperf: Performance of each occupant's position. 0=Non compliant, 1=Minimum, 2=Medium, 3=High"""


import rhinoscriptsyntax as rs
import csv
import os
self=ghenv.Component
self.Name = "SCALE_Vert1SPrc"
self.NickName = 'Vert1SPrc'
self.Message = 'AnnuOWL | Vert1SPrc\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

if runIt==True:
    DltMtxF=DltMtx
    OccupHrsN=OccupHrs
else:
    DltMtxF=DltMtx_0
    OccupHrsN=OccupHrs_0

folder=os.path.dirname(DltMtxF)
numHours=50 if numHours is None else float(numHours) # percentage annual hours as user input variable
print(folder)
os.chdir(folder)
if  os.path.isfile(folder+"/annualR_H.ill")==True:
    print ("Removing the .ill file")
    os.remove("annualR_H.ill")
else:
    print("The .ill file does not exist, nothing to remove")

rows_dltmtx=[]
with open(DltMtxF, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        rows_dltmtx.append(row)

minDA=rows_dltmtx[4] #Following further on the EN17037 logic, the binned min, med, and high credits are then normalised with annual occupancy hours. 
medDA=rows_dltmtx[5]
highDA=rows_dltmtx[6]

minDA_norm=[int(100*float(i)/OccupHrsN) for i in minDA]
medDA_norm=[int(100*float(i)/OccupHrsN) for i in medDA]
highDA_norm=[int(100*float(i)/OccupHrsN) for i in highDA]

minDA_cred= [0 for i in range (len(minDA_norm))]
medDA_cred= [0 for i in range (len(medDA_norm))]
highDA_cred= [0 for i in range (len(highDA_norm))]
perfDA_cred=[0 for i in range (len(highDA_norm))]

for i in range (len(perfDA_cred)): #following EN17037 logic, the credits for min, med and high target are then checked for % annual occupied hours
    if minDA_norm[i]>numHours: #allowing users to vary this threshold
        minDA_cred[i]=1
    else:
        minDA_cred[i]=0
    if medDA_norm[i]>numHours:
        medDA_cred[i]=1
    else:
        medDA_cred[i]=0
    if highDA_norm[i]>numHours:
        highDA_cred[i]=1
    else:
        highDA_cred[i]=0

for i in range (len(perfDA_cred)): # the overall EN17037 recommendation for each gridpoint, where "3"=High, "2"=Medium, "1"=Minimum and "0"=Not satisfactory
    if highDA_cred[i]==1:
        perfDA_cred[i]=3
    elif medDA_cred[i]==1:
        perfDA_cred[i]=2
    elif minDA_cred[i]==1:
        perfDA_cred[i]=1
    else:
        perfDA_cred[i]=0

ENperf=perfDA_cred