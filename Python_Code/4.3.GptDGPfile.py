"""This component extracts the DGP data for a specific position over the year for 4 orientations. This data can then be plotted as heatmaps for visualisation.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Ann_DGP_N0: (if Cached) the location of CSV file containing annual sDGP data for each grid point facing North
        Ann_DGP_E0: (if Cached) the location of CSV file containing annual sDGP data for each grid point facing East
        Ann_DGP_S0: (if Cached) the location of CSV file containing annual sDGP data for each grid point facing South
        Ann_DGP_W0: (if Cached) the location of CSV file containing annual sDGP data for each grid point facing West
        Ann_DGP_N: (if Live) the location of CSV file containing annual sDGP data for each grid point facing North
        Ann_DGP_E: (if Live) the location of CSV file containing annual sDGP data for each grid point facing East
        Ann_DGP_S: (if Live) the location of CSV file containing annual sDGP data for each grid point facing South
        Ann_DGP_W: (if Live) the location of CSV file containing annual sDGP data for each grid point facing West
        GridPt: Index of gridpoint (Occupant Position) under investigation.
        Live: A boolean Toggle. OFF = Cached, ON = Live
        plotIt: A boolean Toggle to plot heatmaps.
    Output:
        DGP_AnnVis_N: Link to the CSV file containing Extracted Annual hourly sDGP for the specified occupant position, Facing North.
        DGP_AnnVis_E: Link to the CSV file containing Extracted Annual hourly sDGP for the specified occupant position, Facing East.
        DGP_AnnVis_S: Link to the CSV file containing Extracted Annual hourly sDGP for the specified occupant position, Facing South.
        DGP_AnnVis_W: Link to the CSV file containing Extracted Annual hourly sDGP for the specified occupant position, Facing West."""

__author__ = "marshal"
__version__ = "2022.03.29"

import rhinoscriptsyntax as rs

import csv
import copy
import os
self=ghenv.Component
self.Name = "SCALE_GptDGPfile"
self.NickName = 'GptDGPfile'
self.Message = 'AnnuOWL | GptDGPfile\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "2"
except: pass

if Live==True:
    Ann_DGP_Files=[Ann_DGP_N,Ann_DGP_E,Ann_DGP_S,Ann_DGP_W]
else:
    Ann_DGP_Files=[Ann_DGP_N0,Ann_DGP_E0,Ann_DGP_S0,Ann_DGP_W0]
#OutFiles=['/DGPautonomyN.csv','/DGPautonomyE.csv','/DGPautonomyS.csv','/DGPautonomyW.csv']
GridPt=0 if GridPt is None else int(GridPt)

if plotIt==True:
    for i in range(0,4,1):
        Ann_DGP=Ann_DGP_Files[i]
#        OutFile=OutFiles[i]
        folder=os.path.dirname(Ann_DGP)+"/"
        DGP_data=Ann_DGP
        rows_Cillumx = []
        with open(DGP_data, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows_Cillumx.append(row)
        rows_Cillum=[[float(ic) for ic in jc] for jc in rows_Cillumx]
        pt_Cillum=[[None for ir in range (24)] for jr in range(365)]
        for ix in range (0,365,1):
            for iy in range(0,24,1):
                hrcnt=24*ix+iy
                pt_Cillum[ix][iy]=rows_Cillum[hrcnt][GridPt]
        if i==0:
            pt_Cillum_N=pt_Cillum
        if i==1:
            pt_Cillum_E=pt_Cillum
        if i==2:
            pt_Cillum_S=pt_Cillum
        if i==3:
            pt_Cillum_W=pt_Cillum

    with open(folder+'/DGPA_N.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(pt_Cillum_N) 
    with open(folder+'/DGPA_E.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(pt_Cillum_E) 
    with open(folder+'/DGPA_S.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(pt_Cillum_S) 
    with open(folder+'/DGPA_W.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(pt_Cillum_W) 
        
    DGP_AnnVis_N=folder+'/DGPA_N.csv'
    DGP_AnnVis_E=folder+'/DGPA_E.csv'
    DGP_AnnVis_S=folder+'/DGPA_S.csv'
    DGP_AnnVis_W=folder+'/DGPA_W.csv'