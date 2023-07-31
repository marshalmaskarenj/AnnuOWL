"""The second of the two related components, that takes in the geometry of the OVNI middle ring (Glare Protection) in four orientations from Vert3SGeoA, and merges these geometries. Its Output connects to Custom Preview Geometry.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        G_N: Geometry of OVNI middle ring, facing North
        G_E: Geometry of OVNI middle ring, facing East
        G_S: Geometry of OVNI middle ring, facing South
        G_W: Geometry of OVNI middle ring, facing West
    Output:
        G: Merged Geometry of OVNI middle ring (Glare Protection), connects to Custom Preview Geometry."""

import rhinoscriptsyntax as rs
self=ghenv.Component
self.Name = "SCALE_Vert3SGeoB"
self.NickName = 'Vert3SGeoB'
self.Message = 'AnnuOWL\nVert3SGeoB\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

G=N+E+S+W