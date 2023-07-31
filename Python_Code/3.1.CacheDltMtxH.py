"""A pre-cached alternative of the DltMtxH component.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        folder: Location of pre-simulated folder.
        runIt: A toggle switch
    Output:
        DltMtx: Location of a pre-calculated CSV file with various daylight metrices (DA/cDA/UDI/Average-Illuminance) for each grid-point, and Occupancy hours of the year.
        OccupHrs: Occupied hours of the year, calculated based on user inputs (SOB, COB, Days of Week, etc.)"""

import rhinoscriptsyntax as rs
import csv
self=ghenv.Component
self.Name = "SCALE_CacheDltMtxH"
self.NickName = 'CacheDltMtxH'
self.Message = 'AnnuOWL | CacheDltMtxH\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

if runIt==False:
    Matrix=folder+'/ann_metrics.csv'
    rows_dltmtx=[]
    with open(Matrix, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_dltmtx.append(row)
    OHr=rows_dltmtx[4][0]
    print(OHr)
    DltMtx=Matrix
    OccupHrs=OHr
