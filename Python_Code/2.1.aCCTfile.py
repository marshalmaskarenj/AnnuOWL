"""This component reads the zenith-luminance-based and hemispherical precalculated CCTs through the year, and tabulates them into respective CSV files for plotting on annual heatmaps.
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        folder: location of the folder for saving simulation files.
        CCT_Zen: the annual zenith-based CCT calculated by aCCTzen component.
        CCT_Hem: precalculated annual hemispherical CCT extracted from .aowl file by the aCCThem component.
    Output:
        CCTz_f: CSV file with tabulated zenith-based annual CCT data (for further plotting)
        CCTh_f: CSV file with tabulated hemispherical annual CCT data (for further plotting)"""

import rhinoscriptsyntax as rs
import csv
self=ghenv.Component
self.Name = "SCALE_aCCTfile"
self.NickName = 'aCCTfile'
self.Message = 'AnnuOWL\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "2"
except: pass

zen_daily=[[0 for i in range (24)] for j in range (365)]
hem_daily=[[0 for i in range (24)] for j in range (365)]

for i in range (8760):
    daycount=int(i/24)
    hourcount=i-24*daycount
    zen_daily[daycount][hourcount]=int(CCT_Zen[i])
    hem_daily[daycount][hourcount]=int(CCT_Hem[i])

with open(folder+'/CCT_zA.csv', 'wb') as f: 
    write = csv.writer(f) 
    write.writerows(zen_daily) 
with open(folder+'/CCT_hA.csv', 'wb') as f: 
    write = csv.writer(f) 
    write.writerows(hem_daily) 

CCTz_f=folder+'CCT_zA.csv'
CCTh_f=folder+'CCT_hA.csv'