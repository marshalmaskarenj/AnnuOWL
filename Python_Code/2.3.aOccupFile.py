"""This component takes the list of annual occupied hours, and tabulates into a CSV file for further plotting and visualisation.
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        folder: location of the active folder for saving simulation data
        Occup_H0: (if displaying a pre-cached simulation) list of annual hours in 1s (occupied) and 0s (unoccupied)
        Occup_H: (if running live simulation) list of annual hours in 1s (occupied) and 0s (unoccupied)
        Live: a boolean toggle. False = Precache. True = Live 
    Output:
        OccupH_f: The location of the CSV file with annual occupancy data. This connects to aOccupPlot for plotting in 24x365 annual heatmap"""

import rhinoscriptsyntax as rs
import csv
self=ghenv.Component
self.Name = "SCALE_aOccupFile"
self.NickName = 'aOccupFile'
self.Message = 'AnnuOWL | aOccupFile\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "2"
except: pass

if Live==True:
    Occup_HF=Occup_H
else:
    Occup_HF=Occup_H0


occup_daily=[[0 for i in range (24)] for j in range (365)]

for i in range (8760):
    daycount=int(i/24)
    hourcount=i-24*daycount
    occup_daily[daycount][hourcount]=int(Occup_HF[i])

with open(folder+'/OccupancySchedule.csv', 'wb') as f: 
    write = csv.writer(f) 
    write.writerows(occup_daily) 

OccupH_f=folder+'OccupancySchedule.csv'