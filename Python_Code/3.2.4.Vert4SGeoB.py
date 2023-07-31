"""The second of the two related components, that takes in the geometry of the OVNI outer ring (View Quality) in four orientations from Vert4SGeoA, and merges these geometries. Its Output connects to Custom Preview Geometry.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        G_N: Geometry of OVNI outer ring, facing North
        G_E: Geometry of OVNI outer ring, facing East
        G_S: Geometry of OVNI outer ring, facing South
        G_W: Geometry of OVNI outer ring, facing West
    Output:
        G: Merged Geometry of OVNI outer ring (View Quality), connects to Custom Preview Geometry."""

import rhinoscriptsyntax as rs
self=ghenv.Component
self.Name = "SCALE_Vert4SGeoB"
self.NickName = 'Vert4SGeoB'
self.Message = 'AnnuOWL\nVert4SGeoB\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass
G=N+E+S+W