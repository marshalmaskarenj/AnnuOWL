"""The first one of the two components designed to display pre-cached geometry of the scene on the Rhino canvas.
Objects such as windows, ceiling, glazing, etc, saved as .obj files in each pre-simulated (or live) folder, are imported and displayed. The output node connects to the second Show-Geometry component.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        folder: Location of the folder with the .obj files.
    Output:
        paths: the paths of each .obj file in the pre-simulated folder. This node connects to the second Show-Geometry component"""

import rhinoscriptsyntax as rs
import os
import glob
self=ghenv.Component
self.Name = "SCALE_ShowGeomA"
self.NickName = 'ShowGeomA'
self.Message = 'AnnuOWL | ShowGeomA\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass



foldername=os.path.dirname(folder)+"/"
allfiles=[]
os.chdir(foldername)
for file in glob.glob("*.obj"):
#    print(file)
    fullname=foldername+file
#    print(fullname)
    if "Glazing" in fullname:
        print("Glaz Found!")
    else:
        print("other")
        allfiles.append(fullname)
#print(allfiles)
paths=allfiles
