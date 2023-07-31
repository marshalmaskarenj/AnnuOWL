"""This component converts defined occupant positions as points into point-files in four principal orientations, for use in radiance grid-based simulations.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        points: Takes a list of points, as x,y,z coordinates. 
        OVNI_grdHt: Height above floor level for evaluating sDA (typically table height, around 0.7m above floor level)
        OVNI_hdHt: Vertical distance between an observer's eyes and the floor level, for evaluating visual/non-visual metrics (typically around 1.2m above floor level)
        folder: Takes location of the folder, for saving the point files.
    Output:
        ViewPtFile_H: pointfile for zenith-facing horizontal position.
        ViewPtFile_N: pointfile for north-facing vertical view.
        ViewPtFile_E: pointfile for east-facing vertical view.
        ViewPtFile_S: pointfile for south-facing vertical view.
        ViewPtFile_W: pointfile for west-facing vertical view.
        ViewPts: list of points as x,y,z coordinates."""


import rhinoscriptsyntax as rs
import ghpythonlib as gl
self=ghenv.Component
self.Name = "SCALE_DefVptFile"
self.NickName = 'DefVptFile'
self.Message = 'AnnuOWL | DefVptFile\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

aval=points
OVNI_grdHt = 0.7 if OVNI_grdHt is None else float(OVNI_grdHt)
OVNI_hdHt = 1.2 if OVNI_hdHt is None else float(OVNI_hdHt)
nwpts=gl.components.Move(points,gl.components.UnitZ(OVNI_hdHt))[0]
ViewPts=nwpts
if runIt==True:
    filepathH = folder + "ViewPtsH.txt"
    filepathN = folder + "ViewPtsN.txt"
    filepathE = folder + "ViewPtsE.txt"
    filepathS = folder + "ViewPtsS.txt"
    filepathW = folder + "ViewPtsW.txt"
    with open(filepathH, 'w') as fileH:
        for item in aval:
            fileH.write((str(round(item[0],3))+' '+str(round(item[1],3))+' '+str(float(round(item[2],3))+OVNI_grdHt)+' 0 0 1\n'))
    with open(filepathN, 'w') as fileN:
        for item in aval:
            fileN.write((str(round(item[0],3))+' '+str(round(item[1],3))+' '+str(float(round(item[2],3))+OVNI_hdHt)+' 0 1 0\n'))
    with open(filepathE, 'w') as fileE:
        for item in aval:
            fileE.write((str(round(item[0],3))+' '+str(round(item[1],3))+' '+str(float(round(item[2],3))+OVNI_hdHt)+' 1 0 0\n'))
    with open(filepathS, 'w') as fileS:
        for item in aval:
            fileS.write((str(round(item[0],3))+' '+str(round(item[1],3))+' '+str(float(round(item[2],3))+OVNI_hdHt)+' 0 -1 0\n'))
    with open(filepathW, 'w') as fileW:
        for item in aval:
            fileW.write((str(round(item[0],3))+' '+str(round(item[1],3))+' '+str(float(round(item[2],3))+OVNI_hdHt)+' -1 0 0\n'))
    ViewPtFile_H=filepathH
    ViewPtFile_N=filepathN
    ViewPtFile_E=filepathE
    ViewPtFile_S=filepathS
    ViewPtFile_W=filepathW
