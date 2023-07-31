"""This component helps visualise pre-simulated data in case needed. While running live simulation for fresh cases, the 'Cached' button can be set to FALSE.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Folder: Link to the current folder
        Cache_Folder: (if selecting a pre-simulated solution) Any file in the pre-simulated folder
        Cached: YES if displaying presimulated results, NO if running live simulation
    Output:
        Prompt: Some information about data processing
        FolderName: Location of files to process, depending upon Cached or Live"""


import rhinoscriptsyntax as rs
import os
self=ghenv.Component
self.Name = "SCALE_PreCache"
self.NickName = 'PreCache'
self.Message = 'AnnuOWL | PreCache\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

if Cached is False:
    Prompt="Results are being displayed from the specified folder"
    FolderName=Folder
else:
    if Cache_Folder is None:
        Prompt="You have have NOT defined any folder containing pre-simulated files. If you'd like to visualise pre-simulated data, please specify folder location by selecting ANY FILE in that folder"
    else:
        FolderName=str(os.path.dirname(Cache_Folder))+'/'
        subfoldername=os.path.basename(os.path.dirname(Cache_Folder))
        Prompt="Pre-simulated data is being visualised from the subfolder " + str(subfoldername)