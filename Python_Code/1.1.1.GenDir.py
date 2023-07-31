"""This component creates a subfolder in your C:\OWL/annuowl/ folder for saving simulation data.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        casename: The name of this specific case, needs to be unique else it will overwrite previous simulation data
    Output:
        prompt: User text
        folder: location of folder for further processing"""

import rhinoscriptsyntax as rs
import os
self=ghenv.Component
self.Name = "SCALE_GenDir"
self.NickName = 'GenDir'
self.Message = 'AnnuOWL | GenDir\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

main_dir="C:\OWL/annuowl/"
work_dir=str(main_dir)+str(casename)+"/"

if not os.path.exists(work_dir):
    os.makedirs(work_dir)
    print ("created directory")
else:
    print("directory already exists")
    
prompt="The simulation data is stored in "+work_dir
folder=work_dir