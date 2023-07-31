"""This component takes the list of points, and saves it as a point-file in the defined folder. This point-file is used by Radiance for further processing.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Pts: List of gridpoints
        fldr: Folder to save the pointfile in.
    Output:
        ptFile: Location of the point-file"""

import rhinoscriptsyntax as rs
self=ghenv.Component
self.Name = "SCALE_GptFile"
self.NickName = 'GptFile'
self.Message = 'AnnuOWL | GptFile\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

if runIt==True:
    filepathH = fldr + "GrdPtsH.txt"
    with open(filepathH, 'w') as fileH:
        for item in Pts:
            fileH.write((str(round(item[0],3))+' '+str(round(item[1],3))+' '+str(round(item[2],3))+' 0 0 1\n'))
    ptFile=filepathH