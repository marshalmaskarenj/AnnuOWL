"""(if running live simulation) This component takes the vertical illuminance data at each occupant position at eye level in 4 orientations, -- and uses simplified DGP approach to evaluate DGPs for each point over the year. 
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        Ann_illumN: Location of the csv file with calculated annual hourly illuminance data for each occupant's position, on eye level at the vertical plane, facing North.
        Ann_illumE: Location of the csv file with calculated annual hourly illuminance data for each occupant's position, on eye level at the vertical plane, facing East.
        Ann_illumS: Location of the csv file with calculated annual hourly illuminance data for each occupant's position, on eye level at the vertical plane, facing South.
        Ann_illumW: Location of the csv file with calculated annual hourly illuminance data for each occupant's position, on eye level at the vertical plane, facing West.
        runIt: A boolean toggle for this component. True =  Live, False = Precache.
    Output:
        Ann_DGP_N: A csv file containing Annual hourly sDGP (vertical plane) for each occupant position, facing North. 
        Ann_DGP_E: A csv file containing Annual hourly sDGP (vertical plane) for each occupant position, facing East. 
        Ann_DGP_S: A csv file containing Annual hourly sDGP (vertical plane) for each occupant position, facing South. 
        Ann_DGP_W: A csv file containing Annual hourly sDGP (vertical plane) for each occupant position, facing West."""

self=ghenv.Component
self.Name = "SCALE_DGPMtxV"
self.NickName = 'DGPMtxV'
self.Message = 'AnnuOWL | DGPMtxV\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

import rhinoscriptsyntax as rs
import csv
import math
import copy
import os
import os.path

illumFiles=[Ann_illumN,Ann_illumE,Ann_illumS,Ann_illumW]
outFiles=['/ann_DGP_N.csv','/ann_DGP_E.csv','/ann_DGP_S.csv','/ann_DGP_W.csv']

if runIt==True:
    for i in range(0,4,1):
        illumFile=illumFiles[i]
        outFile=outFiles[i]
        folder=os.path.dirname(illumFile)+"/"
        print folder
        rows_illumx = []
        with open(illumFile, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows_illumx.append(row)
            
        rows_illum=[[float(i) for i in j] for j in rows_illumx]
        rows_DGPs=copy.deepcopy(rows_illum)
        
        for i in range (0,8760,1): #8760
            inst_illum=rows_illum[i]
            numpts=len(inst_illum)
            for j in range (0,numpts,1):
                illum_v=float(inst_illum[j])
                DGPs_dat=(illum_v*6.22*0.00001)+0.184
                rows_DGPs[i][j]= "{:.3f}".format(DGPs_dat)
        
        with open(folder+outFile, 'wb') as f: 
            write = csv.writer(f) 
            write.writerows(rows_DGPs) 
    
    if os.path.exists(folder+'ann_DGP_N.csv')==True:
        Ann_DGP_N=folder+'ann_DGP_N.csv'
    if os.path.exists(folder+'ann_DGP_E.csv')==True:
        Ann_DGP_E=folder+'ann_DGP_E.csv'
    if os.path.exists(folder+'ann_DGP_S.csv')==True:
        Ann_DGP_S=folder+'ann_DGP_S.csv'
    if os.path.exists(folder+'ann_DGP_W.csv')==True:
        Ann_DGP_W=folder+'ann_DGP_W.csv'
