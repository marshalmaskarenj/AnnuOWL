"""This component imports the 3DM file with divided floor/grid Surface as sub-patches, for further processing.
The subpatches are used for Rhino visualisation, and their central points are used for generating points for Radiance grid-based simulations. 
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        folder: Location of folder where live or cached files are stored.
        grdFile: Location of the 3DM file with divided surface geometry, for further Radiance processing and Rhino visualisation.
        live: A boolean toggle for this component. True = Live simulation, False = Precached data from folder.
    Output:
        carpet: Location of the .3DM file
        GeoSRF: List of individual sub-patches for Rhino grid-based visualisation.
        pnts: List of points for Radiance grid-based simulations"""

import rhinoscriptsyntax as rs
import os
import ghpythonlib.components as gc
self=ghenv.Component
self.Name = "SCALE_importSRF"
self.NickName = 'importSRF'
self.Message = 'AnnuOWL | importSRF\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

foldername=os.path.dirname(folder)+"/"
allfiles=[]

if live==False:
    carpet=foldername+"floorgrid.3dm"#allfiles
else:
    carpet=grdFile
GeoSRF=gc.Import3DM(carpet,'*','*')
pnts=gc.Area(GeoSRF)[1]

