"""A pre-cached alternative of the DltMtxV component.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        folder: Location of pre-simulated folder.
        runIt: A toggle switch
    Output:
        DltMtx: Location of a pre-calculated CSV file with various daylight metrices (DA/cDA/UDI/Average-Illuminance) and compliance metrics (EN17037 Minimum, Medium, High for each occupant-position on horizonal plane, and Occupancy hours of the year.
        OccupHrs: Occupied hours of the year, calculated based on user inputs (SOB, COB, Days of Week, etc.).
        OpenSched: Occupancy state through the 8760 annual hours (0=Unoccupied, 1=Occupied)"""

import rhinoscriptsyntax as rs
import csv
self=ghenv.Component
self.Name = "SCALE_CacheDltMtxV"
self.NickName = 'CacheDltMtxV'
self.Message = 'AnnuOWL | CacheDltMtxV\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass


if runIt==False:
    Matrix=folder+'/ann_Ptmetrics.csv'
    rows_dltmtx=[]
    with open(Matrix, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_dltmtx.append(row)
    OHr=rows_dltmtx[7][0]
    print(OHr)
    DltMtx=Matrix
    OccupHrs=OHr

    rows_OcAr=[]
    with open(folder+'/Occupancy.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_OcAr.append(row)
    
    OpenSched=rows_OcAr[0]
