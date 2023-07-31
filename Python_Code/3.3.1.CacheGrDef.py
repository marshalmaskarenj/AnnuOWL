"""Precached grid definitions, extracted from a pre-simulated folder.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        folder: location of folder containing all simulated files.
        runIt: A boolean toggle. True=Live, False=Precached.
    Output:
        GridSpc_X: Grid Spacing in the X-direction.
        GridSpc_Y: Grid Spacing in the Y-direction.
        GridPln_Ht: Height of grid plane above floor level"""

import rhinoscriptsyntax as rs
import os
import csv
self=ghenv.Component
self.Name = "SCALE_CacheGrDef"
self.NickName = 'CacheGrDef'
self.Message = 'AnnuOWL | CacheGrDef\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

if runIt==False:
    GPT_File=folder+'/geom_points.csv'
    rows_GPT=[]
    with open(GPT_File, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_GPT.append(row)
    print(len(rows_GPT[0]))
    GridSpc_X=rows_GPT[0][0]
    GridSpc_Y=rows_GPT[1][0]
    GridPln_Ht=rows_GPT[2][0]
#    HParray=[[0,0,0]for i in range(len(rows_GPT[0]))]
#    for i in range (len(rows_GPT[0])):
#        HParray[i][0]=float(rows_GPT[3][i])
#        HParray[i][1]=float(rows_GPT[4][i])
#        HParray[i][2]=float(rows_GPT[5][i])
##    print(HParray)
#    HParr=[]
#    for i in range (len(rows_GPT[0])):
#        HParr.append(str(HParray[i][0])+','+str(HParray[i][1])+','+str(HParray[i][2]))
#    Head_Pnts=HParr