"""This component saves the head positions for occupants, for each simulation as a cache for further pre-cached visualisation. The data to be cached as CSV includes the positions of occupants on the floorplane.
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
self.Name = "SCALE_HptFile"
self.NickName = 'HptFile'
self.Message = 'AnnuOWL | HptFile\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

if runIt==True:
    GsX=1
    GsY=1
    Ghtt=1
    Head_Pnts=Headpts
    hdptln=len(Headpts)
    print(hdptln)
    Gx=[float(GsX) for i in range(hdptln)]
    Gy=[float(GsY) for i in range(hdptln)]
    Ght=[float(Ghtt) for i in range(hdptln)]
    flcnt=[]
    flcnt.append(Gx)
    flcnt.append(Gy)
    flcnt.append(Ght)
    Hpt_x=[float(ii[0]) for ii in Headpts]
    Hpt_y=[float(ii[1]) for ii in Headpts]
    Hpt_z=[float(ii[2]) for ii in Headpts]
    flcnt.append(Hpt_x)
    flcnt.append(Hpt_y)
    flcnt.append(Hpt_z)
    with open(folder+'/geom_pointsHd.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(flcnt) 
    GPT_File=folder+'/geom_pointsHd.csv'