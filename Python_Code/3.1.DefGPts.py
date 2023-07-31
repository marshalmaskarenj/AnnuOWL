"""This component divides the defined floor/grid Surface into points and sub-patches, depending upon the X and Y grid spacing. The Gridplane height is also to be defined.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Surface: Surface for horizontal grid-based simulation. Generally the floor
        GrdSpc_X: X grid spacing in meters (eg: 0.5)
        GrdSpc_Y: Y grid spacing in meters (eg: 0.5)
        GrdPln_Ht: Height of gridplane above floor level, in meters (eg: 0.7)
    Output:
        Geo: Geometry of sub-patches
        Pts: List of points for further processing"""

import rhinoscriptsyntax as rs
import ghpythonlib.components as gc
self=ghenv.Component
self.Name = "SCALE_DefGPts"
self.NickName = 'DefGPts'
self.Message = 'AnnuOWL | DefGPts\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

GrdPln_Ht=0.7 if GrdPln_Ht is None else float(GrdPln_Ht)
srfc=Surface
GrdSpc_X=0.4 if GrdSpc_X is None else float(GrdSpc_X)
GrdSpc_Y=0.4 if GrdSpc_Y is None else float(GrdSpc_Y)
faces=gc.DeconstructBrep(srfc)[0]
hfaces=gc.Move(faces,gc.UnitZ(GrdPln_Ht))[0]
pnt=rs.CreatePoint(0,0,0)
XYPlane=gc.XYPlane(pnt)
boundbox=gc.BoundingBox(hfaces,XYPlane)
bxcrnr=gc.BoxCorners(boundbox[0])
cnr_A=bxcrnr[0]
cnr_B=bxcrnr[1]
cnr_C=bxcrnr[2]
cnr_D=bxcrnr[3]
Ln1=gc.Line(cnr_A,cnr_B)
Ln2=gc.Line(cnr_A,cnr_D)
dvL1=gc.DivideLength(Ln1,GrdSpc_X)[0]
dvL2=gc.DivideLength(Ln2,GrdSpc_Y)[0]
Vct1=gc.Vector2Pt(cnr_A,dvL1,False)[0]
Vct2=gc.Vector2Pt(cnr_A,dvL2,False)[0]
Mov1=gc.Move(Ln2,Vct1)[0]
Mov2=gc.Move(Ln1,Vct2)[0]
crvsS=Mov1+Mov2
srf_splt=gc.SurfaceSplit(hfaces,crvsS)
Geo=srf_splt
Pts=gc.Area(srf_splt)[1]




