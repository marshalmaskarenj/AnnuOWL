"""Occupant head-position based definitions used for visualising OVNI-related data on Rhino viewports.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        H_P0: (if pre-cached) Head positions of the occupants
        H_P: (if live-sim) Head positions of the occupants
        runIt: A boolean toggle for this component. True =  Live, False = Precache.
    Output:
        Hd_Pts: Head positions of the occupants"""

import rhinoscriptsyntax as rs
self=ghenv.Component
self.Name = "SCALE_HdPts"
self.NickName = 'HdPts'
self.Message = 'AnnuOWL | HdPts\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass
if runIt==False:
    Hd_Pts=H_P0
else:
    Hd_Pts=H_P