"""The first of two related components, that generates the OVNI middle ring (Glare Protection) Geometry. The second component -- Vert3SGeoB -- merges these geometries and its Output connects to Custom Preview Geometry.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        ViewPts: Points representing occupants' head positions.
        Rad: Radius of OVNI diagrams. Can be rescaled.
    Output:
        G_N: Geometry of OVNI middle ring, facing North
        G_E: Geometry of OVNI middle ring, facing East
        G_S: Geometry of OVNI middle ring, facing South
        G_W: Geometry of OVNI middle ring, facing West"""

import rhinoscriptsyntax as rs
import math
import ghpythonlib as gl
import Rhino
self=ghenv.Component
self.Name = "SCALE_Vert3SGeoA"
self.NickName = 'Vert3SGeoA'
self.Message = 'AnnuOWL | Vert3SGeoA\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

point=ViewPts
print(point)
angleV=[[0.0,0.69813,-0.69813,0.76794,-0.76794],[1.57079,2.26892,0.87266,2.33874,0.80285],[3.14159,3.83972,2.44346,3.90953,2.37364],[4.71238,5.41052,4.01425,5.48033,3.94444]]
aa=point

srf_all=[]
for i in range (0,4,1):
    ang=(angleV[i])
    angle=ang[0]
    angleP=ang[1]
    angleM=ang[2]
    anglePo=ang[3]
    angleMo=ang[4]
    p0=rs.CreatePoint(aa[0]+1.53*Rad*math.cos(angleMo),aa[1]+1.53*Rad*math.sin(angleMo),aa[2])
    p1=rs.CreatePoint(aa[0]+1.53*Rad*math.cos(angle),aa[1]+1.53*Rad*math.sin(angle),aa[2])
    p2=rs.CreatePoint(aa[0]+1.53*Rad*math.cos(anglePo),aa[1]+1.53*Rad*math.sin(anglePo),aa[2])
    p3=rs.CreatePoint(aa[0]+1.97*Rad*math.cos(angleM),aa[1]+1.97*Rad*math.sin(angleM),aa[2])
    p4=rs.CreatePoint(aa[0]+1.97*Rad*math.cos(angle),aa[1]+1.97*Rad*math.sin(angle),aa[2])
    p5=rs.CreatePoint(aa[0]+1.97*Rad*math.cos(angleP),aa[1]+1.97*Rad*math.sin(angleP),aa[2])
    arcS=gl.components.Arc3Pt(p0,p1,p2)[0],gl.components.Line(p2,p5),gl.components.Arc3Pt(p5,p4,p3)[0],gl.components.Line(p3,p0)
    srf=gl.components.ConnectCurves((arcS[0],arcS[1],arcS[2]),0,True,0)
    srf_all.append(srf)
GridGeo=Rhino.Geometry.Brep.CreatePlanarBreps(srf_all)

GN=[]
GE=[]
GS=[]
GW=[]
GN.append(GridGeo[1])
GE.append(GridGeo[0])
GS.append(GridGeo[3])
GW.append(GridGeo[2])
G_N=GN
G_E=GE
G_S=GS
G_W=GW

