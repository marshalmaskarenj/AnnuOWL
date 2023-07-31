"""(Live Simulation only) This component takes the DC matrix (from SCALE_DCMatrix) along with EPW file, to generate annual illuminance distribution via 2-phase DC method. 
The Annual illuminance data in .csv form then connects to SCALE_IllumAnnInst component to isolate point-in-time data as needed.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LOCI, UCLouvain.
    Inputs:
        DCMatrix_H: Location of the saved .mtx file containing pointwise Daylight Coefficients for zenith-facing horizontal position.
        DCMatrix_N: Location of the saved .mtx file containing pointwise Daylight Coefficients for north-facing vertical view.
        DCMatrix_E: Location of the saved .mtx file containing pointwise Daylight Coefficients for east-facing vertical view.
        DCMatrix_S: Location of the saved .mtx file containing pointwise Daylight Coefficients for south-facing vertical view.
        DCMatrix_W: Location of the saved .mtx file containing pointwise Daylight Coefficients for west-facing vertical view.
        epwFile: Connect to the EPW file of the location.
        runIt: A boolean toggle to run this component. True = Live, False = Precache.
    Output:
        Ann_illumH: Location of the csv file generated, which contains annual illuminance values for zenith-facing horizontal position.
        Ann_illumN: Location of the csv file generated, which contains annual illuminance values for north-facing vertical view.
        Ann_illumE: Location of the csv file generated, which contains annual illuminance values for east-facing vertical view.
        Ann_illumS: Location of the csv file generated, which contains annual illuminance values for south-facing vertical view.
        Ann_illumW: Location of the csv file generated, which contains annual illuminance values for west-facing vertical view."""

import rhinoscriptsyntax as rs
import os
import csv
from subprocess import call
self=ghenv.Component
self.Name = "SCALE_AnnIllV"
self.NickName = 'AnnIllV'
self.Message = 'AnnuOWL | AnnIllV\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

def AnnualR():
    os.chdir(folder)
    call(["cmd","/C","epw2wea "+epwFile+" location.wea"])
    call(["cmd","/C","gendaymtx -m 1 location.wea > location.smx"])
    call(["cmd","/C","dctimestep "+str(DCMtxH)+" location.smx > annualR_H.mtx"])
    call(["cmd","/C","dctimestep "+str(DCMtxN)+" location.smx > annualR_N.mtx"])
    call(["cmd","/C","dctimestep "+str(DCMtxE)+" location.smx > annualR_E.mtx"])
    call(["cmd","/C","dctimestep "+str(DCMtxS)+" location.smx > annualR_S.mtx"])
    call(["cmd","/C","dctimestep "+str(DCMtxW)+" location.smx > annualR_W.mtx"])
    call(["cmd","/C","rmtxop -fa -t -c 47.4 119.9 11.6 annualR_H.mtx > annualR_H.ill"])
    call(["cmd","/C","rmtxop -fa -t -c 47.4 119.9 11.6 annualR_N.mtx > annualR_N.ill"])
    call(["cmd","/C","rmtxop -fa -t -c 47.4 119.9 11.6 annualR_E.mtx > annualR_E.ill"])
    call(["cmd","/C","rmtxop -fa -t -c 47.4 119.9 11.6 annualR_S.mtx > annualR_S.ill"])
    call(["cmd","/C","rmtxop -fa -t -c 47.4 119.9 11.6 annualR_W.mtx > annualR_W.ill"])
    os.remove("annualR_H.mtx")
    os.remove("annualR_N.mtx")
    os.remove("annualR_E.mtx")
    os.remove("annualR_S.mtx")
    os.remove("annualR_W.mtx")
    print (folder)
    fldr=folder.replace(os.sep, '/')
    print (fldr)

    illfH=fldr+"/annualR_H.ill"
    reader = list(csv.reader(open(illfH), delimiter="\t"))
    del(reader[0:12])
    newarr = [[None for _ in range(len(reader[0])-1)] for _ in range(len(reader))]
    for i in range (0,len(reader),1):
        for j in range (0, len(reader[0])-1,1):
            newarr[i][j]=int(float(reader[i][j]))
    with open(fldr+"/annualillumH.csv", 'wb') as f:
        write = csv.writer(f)
        write.writerows(newarr)

    illfN=fldr+"/annualR_N.ill"
    reader = list(csv.reader(open(illfN), delimiter="\t"))
    del(reader[0:12])
    newarr = [[None for _ in range(len(reader[0])-1)] for _ in range(len(reader))]
    for i in range (0,len(reader),1):
        for j in range (0, len(reader[0])-1,1):
            newarr[i][j]=int(float(reader[i][j]))
    with open(fldr+"/annualillumN.csv", 'wb') as f:
        write = csv.writer(f)
        write.writerows(newarr)

    illfE=fldr+"/annualR_E.ill"
    reader = list(csv.reader(open(illfE), delimiter="\t"))
    del(reader[0:12])
    newarr = [[None for _ in range(len(reader[0])-1)] for _ in range(len(reader))]
    for i in range (0,len(reader),1):
        for j in range (0, len(reader[0])-1,1):
            newarr[i][j]=int(float(reader[i][j]))
    with open(fldr+"/annualillumE.csv", 'wb') as f:
        write = csv.writer(f)
        write.writerows(newarr)

    illfS=fldr+"/annualR_S.ill"
    reader = list(csv.reader(open(illfS), delimiter="\t"))
    del(reader[0:12])
    newarr = [[None for _ in range(len(reader[0])-1)] for _ in range(len(reader))]
    for i in range (0,len(reader),1):
        for j in range (0, len(reader[0])-1,1):
            newarr[i][j]=int(float(reader[i][j]))
    with open(fldr+"/annualillumS.csv", 'wb') as f:
        write = csv.writer(f)
        write.writerows(newarr)

    illfW=fldr+"/annualR_W.ill"
    reader = list(csv.reader(open(illfW), delimiter="\t"))
    del(reader[0:12])
    newarr = [[None for _ in range(len(reader[0])-1)] for _ in range(len(reader))]
    for i in range (0,len(reader),1):
        for j in range (0, len(reader[0])-1,1):
            newarr[i][j]=int(float(reader[i][j]))
    with open(fldr+"/annualillumW.csv", 'wb') as f:
        write = csv.writer(f)
        write.writerows(newarr)

    return fldr+"/annualillumH.csv",fldr+"/annualillumN.csv",fldr+"/annualillumE.csv",fldr+"/annualillumS.csv",fldr+"/annualillumW.csv"

if runIt==True:
    folder=os.path.dirname(DCMatrix_N)
    DCMtxH=os.path.basename(DCMatrix_H)
    DCMtxN=os.path.basename(DCMatrix_N)
    DCMtxE=os.path.basename(DCMatrix_E)
    DCMtxS=os.path.basename(DCMatrix_S)
    DCMtxW=os.path.basename(DCMatrix_W)
    Ann_illumH,Ann_illumN,Ann_illumE,Ann_illumS,Ann_illumW =AnnualR()