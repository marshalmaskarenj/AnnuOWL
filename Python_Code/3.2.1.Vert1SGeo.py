"""This component generates the OVNI inner hemisphere's Geometry. Output connects to Custom Preview Geometry.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        ViewPts: Points representing occupants' head positions.
        Rad: Radius of OVNI inner hemisphere. Can be rescaled.
    Output:
        HemS: Hemispherical Geometry, connects to Custom Preview"""


import rhinoscriptsyntax as rs
import math
import ghpythonlib as gl
import Rhino
self=ghenv.Component
self.Name = "SCALE_Vert1SGeo"
self.NickName = 'Vert1SGeo'
self.Message = 'AnnuOWL | Vert1SGeo\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

point=ViewPts

sph_all=[]
pln_all=[]
hms_all=[]
for pnt in point:
    sph=gl.components.Sphere(pnt, Rad)
    pln=gl.components.PlaneSurface(pnt,1,1)
    untx=gl.components.UnitX(-0.5)
    unty=gl.components.UnitY(-0.5)
    movPlnX=gl.components.Move(pln,untx)[0]
    movPlnY=gl.components.Move(movPlnX,unty)[0]
    HemS=gl.components.SplitBrep(sph,movPlnY)[0]
    sph_all.append(sph)
    pln_all.append(movPlnY)
    hms_all.append(HemS)

GridGeo_H=sph_all
GridPln=pln_all
HemS=hms_all 