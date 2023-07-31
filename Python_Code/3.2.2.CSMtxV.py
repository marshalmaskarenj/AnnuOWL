"""(if running live simulation) This component takes the annual sky SPD data (.aowl file) which includes pre-calculated CIE_z value for each annual hour in addition to spectral data -- along with vertical illuminance data at each occupant position at eye level in 4 orientations, and uses Truong's approximation to evaluate CS for each point over the year. 
Truong's approximation makes the code atleast 900X fast (tested to be 1826sec vs 2.7sec for a specific case, for regular calculation as in OWL1 approach and with Truong's approximation, respectively).
For more info on this approximation, refer to DOI: 10.1177/1477153519887423 and DOI: 10.1177/14771535211044664
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Ann_illumN: Location of the csv file with calculated annual hourly illuminance data for each occupant's position, on eye level at the vertical plane, facing North.
        Ann_illumE: Location of the csv file with calculated annual hourly illuminance data for each occupant's position, on eye level at the vertical plane, facing East.
        Ann_illumS: Location of the csv file with calculated annual hourly illuminance data for each occupant's position, on eye level at the vertical plane, facing South.
        Ann_illumW: Location of the csv file with calculated annual hourly illuminance data for each occupant's position, on eye level at the vertical plane, facing West.
        spdFile: Location of the annual SPD data file (.aowl format) which also has CIE x y z, spectral data and CCT values, with CIEz being the relevant data for each annual hour.
        runIt: A boolean toggle for this component. True =  Live, False = Precache.
    Output:
        Ann_CS_N: A csv file containing Annual hourly CS (vertical plane) for each occupant position, facing North. 
        Ann_CS_E: A csv file containing Annual hourly CS (vertical plane) for each occupant position, facing East. 
        Ann_CS_S: A csv file containing Annual hourly CS (vertical plane) for each occupant position, facing South. 
        Ann_CS_W: A csv file containing Annual hourly CS (vertical plane) for each occupant position, facing West. """

import rhinoscriptsyntax as rs
import csv
import math
import copy
import os
import os.path
self=ghenv.Component
self.Name = "SCALE_CSMtxV"
self.NickName = 'CSMtxV'
self.Message = 'AnnuOWL | CSMtxV\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

illumFiles=[Ann_illumN,Ann_illumE,Ann_illumS,Ann_illumW]
outFiles=['/ann_CS_N.csv','/ann_CS_E.csv','/ann_CS_S.csv','/ann_CS_W.csv']

if runIt==True:
    for i in range(0,4,1):
        illumFile=illumFiles[i]
        outFile=outFiles[i]
        folder=os.path.dirname(illumFile)+"/"
        print folder
        rows_illumx = []
        rows_spdx = []
        with open(illumFile, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows_illumx.append(row)
            
        with open(spdFile, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            fields = next(csvreader)
            for row in csvreader:
                rows_spdx.append(row)
        
        rows_illum=[[float(i) for i in j] for j in rows_illumx]
        rows_circillumS=copy.deepcopy(rows_illum)
        
        for i in range (0,8760,1): #8760
            inst_zval=rows_spdx[i]
            z_valueS=inst_zval[9]
            if z_valueS=='-':
                z_valueS=0.000
            # print(z_valueS)
            z_value=float(z_valueS)
            if z_value<0:
                z_value=0.000
            inst_illum=rows_illum[i]
            numpts=len(inst_illum)
            for j in range (0,numpts,1):
                illum_v=float(inst_illum[j])
                if z_value>0.195:
                    CStim=0.7-(0.7/(1+0.016781*(z_value*(illum_v**0.509265))**2.268904)) 
                else:
                    CStim=0.7-(0.7/(1+0.011376*(z_value*illum_v)**1.109998))
                rows_circillumS[i][j]= "{:.3f}".format(CStim)
        
        with open(folder+outFile, 'wb') as f: 
            write = csv.writer(f) 
            write.writerows(rows_circillumS) 
    
    if os.path.exists(folder+'ann_CS_N.csv')==True:
        Ann_CS_N=folder+'ann_CS_N.csv'
    if os.path.exists(folder+'ann_CS_E.csv')==True:
        Ann_CS_E=folder+'ann_CS_E.csv'
    if os.path.exists(folder+'ann_CS_S.csv')==True:
        Ann_CS_S=folder+'ann_CS_S.csv'
    if os.path.exists(folder+'ann_CS_W.csv')==True:
        Ann_CS_W=folder+'ann_CS_W.csv'
