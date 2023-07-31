"""This component reads OBJfiles with material files (while also generating an interim skyfile), and renders a Daylight Coefficient Matrix as precursor to Radiance grid-based evaluation.
[This is a customised case component for Horizontal-only]
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        caseName: Name for the specific case. 
        objFile: Takes location of .obj files. Connect to the output node of ExportOBJ component.
        mtlFile: Takes location of Material file (in .RAD format) from GenMat component.
        pointFile: Takes a point-file with a list of gridpoints.
        runIt: A boolean toggle to run this component.
    Output:
        DCmtx: Location of the saved .mtx file containing pointwise Daylight Coefficients."""

import rhinoscriptsyntax as rs
import os
from subprocess import call
self=ghenv.Component
self.Name = "SCALE_DCMtxH"
self.NickName = 'DCMtxH'
self.Message = 'AnnuOWL | DCMtxH\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "2"
except: pass

def Obj2HDR(sceneradfile,objfile):
    savefilepath=folder+"scene.rad"
    with open(savefilepath, "w") as f:
        f.write(sceneradfile)
    sfile="spectralSkyglow.sky" #os.path.basename(skyFile)
    os.chdir(folder)
    call(["cmd","/C","oconv "+str(sfile)+" scene.rad > scene.oct"])
    ptFileH=os.path.basename(ptFile)
    os.chdir(folder)   
    num_linesH = sum(1 for line in open(ptFile))
    call(["cmd","/C","rfluxmtx -I+ -y "+str(num_linesH)+" -lw 0.0001 -ab 5 -ad 10000 -n 16 - "+sfile+" -i scene.oct < "+ptFileH+" > "+str(caseName)+"_ill_Hrz.mtx"])
    return folder+str(caseName)+"_ill_Hrz.mtx"

def scenerad(caseName):
    sceneradstr=str("void mesh "+"model"+"\n" + \
                "1 "+caseName+".rtm\n" + \
                "0\n" +\
                "0\n" +\
                "\n")
    return(sceneradstr)

def obj2meshfn(objfile,caseName):
    strval=str("obj2mesh -a "+mtlFile+" "+objfile+" "+folder+caseName+".rtm")
    call(["cmd","/C",strval])

if runIt==True:
    folder=str(os.path.dirname(mtlFile))+'\\'
    outputFile=folder + "\spectralSkyglow.sky"
    skyStr = "#@rfluxmtx u=+Y h=u\nvoid glow groundglow\n0\n0\n4 1 1 1 0\n\ngroundglow source ground\n0\n0\n4 0 0 -1 180\n\n#@rfluxmtx u=+Y h=r1\nvoid glow skyglow\n0\n0\n4 1 1 1 0\n\nskyglow source skydome\n0\n0\n4 0 0 1 180"
    skyFile = open(outputFile, 'w')
    skyFile.write(skyStr)
    skyFile.close()
    sstr=""
    for iln in range (len(objFile)):
        bn=os.path.splitext(os.path.basename(objFile[iln]))[0]
        sceneradstr=scenerad(bn)
        obj2meshfn(objFile[iln],bn)
        sstr=sstr+sceneradstr
    DCmtx_fnmH=Obj2HDR(sstr,objFile)
    if os.path.exists(DCmtx_fnmH):
        DCmtx=DCmtx_fnmH