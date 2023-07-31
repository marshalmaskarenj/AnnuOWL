"""Grid definitions from live simulations, extracted from live-simulated folder.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        GPT_File: location of Grid definition file.
        runIt: A boolean toggle. True=Live, False=Precached.
    Output:
        GridSpc_X: Grid Spacing in the X-direction.
        GridSpc_Y: Grid Spacing in the Y-direction.
        GridPln_Ht: Height of grid plane above floor level"""

import rhinoscriptsyntax as rs
import os
import csv
self=ghenv.Component
self.Name = "SCALE_GrDef"
self.NickName = 'GrDef'
self.Message = 'AnnuOWL | GrDef\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

if runIt==True:
    rows_GPT=[]
    with open(GPT_File, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_GPT.append(row)
    print(len(rows_GPT[0]))
    GridSpc_X=rows_GPT[0][0]
    GridSpc_Y=rows_GPT[1][0]
    GridPln_Ht=rows_GPT[2][0]