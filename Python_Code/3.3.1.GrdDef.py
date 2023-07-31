"""Grid definitions used for visualising grid-based data (such as CBDMs) on Rhino viewports.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        G_X0: (if pre-cached)  Grid Spacing in the X-direction.
        G_Y0: (if pre-cached)  Grid Spacing in the Y-direction.
        G_Ht0: (if pre-cached)  Height of grid plane above floor level.
        G_X: (if live-sim)  Grid Spacing in the X-direction.
        G_Y: (if live-sim)  Grid Spacing in the Y-direction.
        G_Ht: (if live-sim)  Height of grid plane above floor level.
        runIt: A boolean toggle for this component. True =  Live, False = Precache.
    Output:
        Grd_X: Grid Spacing in the X-direction.
        Grd_Y: Grid Spacing in the Y-direction.
        Grd_Ht: Height of grid plane above floor level."""

import rhinoscriptsyntax as rs
self=ghenv.Component
self.Name = "SCALE_GrdDef"
self.NickName = 'GrdDef'
self.Message = 'AnnuOWL | GrdDef\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

if runIt==False:
    Grd_X=G_X0
    Grd_Y=G_Y0
    Grd_Ht=G_Ht0
else:
    Grd_X=G_X
    Grd_Y=G_Y
    Grd_Ht=G_Ht