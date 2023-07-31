"""This component saves the grid definition for each simulation as a cache for further pre-cached visualisation, and also for the live simulations. The data to be cached as CSV includes Grid-X, Grid-Y and Gridplane Height.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        folder: Location of folder for saving grid definition file as csv.
        GrdSpc_X: Grid spacing in X direction.
        GrdSpc_Y: Grid spacing in Y direction.
        GrdPln_Ht: Height of gridplane above floor level.
        Headpts: Position of observers (The points need to be defined AT FLOOR LEVEL).
        runIt: a boolean switch for this component. If YES, the CSV is saved to the folder.
    Output:
        GPT_File: Location of the grid definition CSV file."""

import rhinoscriptsyntax as rs
import os
import csv
self=ghenv.Component
self.Name = "SCALE_GrDefFile"
self.NickName = 'GrDefFile'
self.Message = 'AnnuOWL | GrDefFile\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

if runIt==True:
    GridSpc_X=GrdSpc_X
    GridSpc_Y=GrdSpc_Y
    GridPln_Ht=GrdPln_Ht
#    Head_Pnts=Headpts
#    hdptln=len(Headpts)
#    print(hdptln)
    Gx=[float(GrdSpc_X) for i in range(3)]
    Gy=[float(GrdSpc_Y) for i in range(3)]
    Ght=[float(GrdPln_Ht) for i in range(3)]
    flcnt=[]
    flcnt.append(Gx)
    flcnt.append(Gy)
    flcnt.append(Ght)
#    Hpt_x=[float(ii[0]) for ii in Headpts]
#    Hpt_y=[float(ii[1]) for ii in Headpts]
#    Hpt_z=[float(ii[2]) for ii in Headpts]
#    flcnt.append(Hpt_x)
#    flcnt.append(Hpt_y)
#    flcnt.append(Hpt_z)
    with open(folder+'/geom_points.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(flcnt) 
    GPT_File=folder+'/geom_points.csv'