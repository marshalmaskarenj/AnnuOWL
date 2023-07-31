"""The second of the two related components, that takes in the geometry of the OVNI first ring (Well-being/Circadian) in four orientations from Vert2SGeoA, and merges these geometries. Its Output connects to Custom Preview Geometry.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        G_N: Geometry of OVNI inner ring, facing North
        G_E: Geometry of OVNI inner ring, facing East
        G_S: Geometry of OVNI inner ring, facing South
        G_W: Geometry of OVNI inner ring, facing West
    Output:
        G: Merged Geometry of OVNI first ring (Well-being/Circadian), connects to Custom Preview Geometry."""


import rhinoscriptsyntax as rs
self=ghenv.Component
self.Name = "SCALE_Vert2SGeoB"
self.NickName = 'Vert2SGeoB'
self.Message = 'AnnuOWL\nVert2SGeoB\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

G=N+E+S+W