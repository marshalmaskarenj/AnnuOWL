"""This component extracts the CS data for a specific position over the year for 4 orientations. This data can then be plotted as heatmaps for visualisation.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Ann_CS_N0: (if Cached) the location of CSV file containing annual CS data for each grid point facing North
        Ann_CS_E0: (if Cached) the location of CSV file containing annual CS data for each grid point facing East
        Ann_CS_S0: (if Cached) the location of CSV file containing annual CS data for each grid point facing South
        Ann_CS_W0: (if Cached) the location of CSV file containing annual CS data for each grid point facing West
        Ann_CS_N: (if Live) the location of CSV file containing annual CS data for each grid point facing North
        Ann_CS_E: (if Live) the location of CSV file containing annual CS data for each grid point facing East
        Ann_CS_S: (if Live) the location of CSV file containing annual CS data for each grid point facing South
        Ann_CS_W: (if Live) the location of CSV file containing annual CS data for each grid point facing West
        GridPt: Index of gridpoint (Occupant Position) under investigation.
        Live: A boolean Toggle. OFF = Cached, ON = Live
        plotIt: A boolean Toggle to plot heatmaps.
    Output:
        CS_AnnVis_N: Link to the CSV file containing Extracted Annual hourly Circadian Stimulus for the specified occupant position, Facing North.
        CS_AnnVis_E: Link to the CSV file containing Extracted Annual hourly Circadian Stimulus for the specified occupant position, Facing East.
        CS_AnnVis_S: Link to the CSV file containing Extracted Annual hourly Circadian Stimulus for the specified occupant position, Facing South.
        CS_AnnVis_W: Link to the CSV file containing Extracted Annual hourly Circadian Stimulus for the specified occupant position, Facing West."""

import rhinoscriptsyntax as rs

import csv
import copy
import os
self=ghenv.Component
self.Name = "SCALE_GptCSfile"
self.NickName = 'GptCSfile'
self.Message = 'AnnuOWL | GptCSfile\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "2"
except: pass


if Live==True:
    Ann_CS_Files=[Ann_CS_N,Ann_CS_E,Ann_CS_S,Ann_CS_W]
else:
    Ann_CS_Files=[Ann_CS_N0,Ann_CS_E0,Ann_CS_S0,Ann_CS_W0]
#OutFiles=['/CSautonomyN.csv','/CSautonomyE.csv','/CSautonomyS.csv','/CSautonomyW.csv']
GridPt=0 if GridPt is None else int(GridPt)

if plotIt==True:
    for i in range(0,4,1):
        Ann_CS=Ann_CS_Files[i]
#        OutFile=OutFiles[i]
        folder=os.path.dirname(Ann_CS)+"/"
        CS_data=Ann_CS
        rows_Cillumx = []
        with open(CS_data, 'r') as csvfile:
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

    with open(folder+'/CSA_N.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(pt_Cillum_N) 
    with open(folder+'/CSA_E.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(pt_Cillum_E) 
    with open(folder+'/CSA_S.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(pt_Cillum_S) 
    with open(folder+'/CSA_W.csv', 'wb') as f: 
        write = csv.writer(f) 
        write.writerows(pt_Cillum_W) 
        
    CS_AnnVis_N=folder+'/CSA_N.csv'
    CS_AnnVis_E=folder+'/CSA_E.csv'
    CS_AnnVis_S=folder+'/CSA_S.csv'
    CS_AnnVis_W=folder+'/CSA_W.csv'