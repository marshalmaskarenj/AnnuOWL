"""This component takes the DC matrix (from SCALE_DCMtxH) along with EPW file, to generate annual illuminance distribution via 2-phase DC method. 
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        DCMatrix: Link to .mtx file output of SCALE_DCMtxH
        epwFile: Connect to the EPW file of the location
        runIt: A boolean toggle to run this component.
    Output:
        Ann_illum: Location of the annualillum.csv file generated, which contains annual illuminance values."""

import rhinoscriptsyntax as rs
import os
import csv
from subprocess import call
self=ghenv.Component
self.Name = "SCALE_AnnIllH"
self.NickName = 'AnnIllH'
self.Message = 'AnnuOWL | AnnIllH\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

def AnnualR():
    os.chdir(folder)
    call(["cmd","/C","epw2wea "+epwFile+" location.wea"])
    call(["cmd","/C","gendaymtx -m 1 location.wea > location.smx"])
    call(["cmd","/C","dctimestep "+str(DCMtxH)+" location.smx > annualR_Hrz.mtx"])
    call(["cmd","/C","rmtxop -fa -t -c 47.4 119.9 11.6 annualR_Hrz.mtx > annualR_Hrz.ill"])
    os.remove("annualR_Hrz.mtx")
    print (folder)
    fldr=folder.replace(os.sep, '/')
    print (fldr)

    illfH=fldr+"/annualR_Hrz.ill"
    reader = list(csv.reader(open(illfH), delimiter="\t"))
    del(reader[0:12])
    newarr = [[None for _ in range(len(reader[0])-1)] for _ in range(len(reader))]
    for i in range (0,len(reader),1):
        for j in range (0, len(reader[0])-1,1):
            newarr[i][j]=int(float(reader[i][j]))
    with open(fldr+"/annualillum_Hrz.csv", 'wb') as f:
        write = csv.writer(f)
        write.writerows(newarr)
    return fldr+"/annualillum_Hrz.csv"

if runIt==True:
    folder=os.path.dirname(DCMtx)
    DCMtxH=os.path.basename(DCMtx)
    Ann_IlH=AnnualR()