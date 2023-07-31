"""A logical component that feeds into the runIt of ExportOBJ components, taking inputs both from dedicated toggle button, but also from PreCache component's Toggle.
If Precache is True, this results into 'False' output irrespective of dedicated toggle key. If PreCache is False, it results into True or False depending upon state of dedicated Toggle key.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        cached: The toggle key of PreCache. This is the dominant key input.
        Export_OBJ: The dedicated toggle key. This is the secondary key input.
    Output:
        exportOBJ: This connects to the runIt node of ExportOBJ component(s)."""

__author__ = "marshal"
__version__ = "2023.07.16"

import rhinoscriptsyntax as rs
self=ghenv.Component
self.Name = "SCALE_KeyCacheOBJ"
self.NickName = 'KeyCacheOBJ'
self.Message = 'AnnuOWL | KeyCacheOBJ\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass


if cached==False:
    if Export_OBJ==True:
        exportOBJ=True
    else:
        exportOBJ=False
else:
    exportOBJ=False