"""A logical component that feeds into the runIt of Vertical Metrics components, taking inputs both from dedicated toggle button ("Start Vertical Simulation?"), but also from PreCache component's Toggle.
If Precache is True, this results into 'False' output irrespective of dedicated toggle key. If PreCache is False, it results into True or False depending upon state of dedicated Toggle key.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        cached: The toggle key of PreCache. This is the dominant key input.
        Start_Vert_Sim: The dedicated toggle key. This is the secondary key input.
    Output:
        Vert_Sim: This connects to the runIt node of various horizontal simulation component(s)."""

import rhinoscriptsyntax as rs
self=ghenv.Component
self.Name = "SCALE_KeyVertSim"
self.NickName = 'KeyVertSim'
self.Message = 'AnnuOWL | KeyVertSim\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

if cached==False:
    if Start_Vert_Sim==True:
        Vert_Sim=True
    else:
        Vert_Sim=False
else:
    Vert_Sim=False