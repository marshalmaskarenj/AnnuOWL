"""Each simulation run generates multiple interim files, many of which are not useful for data visualisationand processing. 
This component removes such heavy files from the simulation folder.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        objFiles: This links to the (merged) objFiles generated each simulation.
        CleanUp: A toggle button, set TRUE for cleaning the residual bulky interim files.
    Output:
        a: The a output variable"""

import rhinoscriptsyntax as rs
import os
self=ghenv.Component
self.Name = "SCALE_CleanUp"
self.NickName = 'CleanUp'
self.Message = 'AnnuOWL | CleanUp\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

folder=os.path.dirname(objFiles[0])
print(folder)
os.chdir(folder)
if CleanUp==True:
    for file in objFiles:
        fnm=os.path.basename(file)
        rtnm=os.path.splitext(fnm)[0]
        rtm_fl=rtnm+".rtm"
        print(rtm_fl)
        if  os.path.isfile(folder+"/"+rtm_fl)==True:
            print ("Removing RTM files")
            os.remove(rtm_fl)
        else:
            print("RTM files don't exist")
    
    if  os.path.isfile(folder+"/annualR_Hrz.ill")==True:
        print ("Removing the annualR_Hrz.ill file")
        os.remove(folder+"/annualR_Hrz.ill")
    else:
        print("The annualR_Hrz.ill file doesn't exist")

    if  os.path.isfile(folder+"/location.smx")==True:
        print ("Removing the location.smx file")
        os.remove(folder+"/location.smx")
    else:
        print("The location.smx file doesn't exist")