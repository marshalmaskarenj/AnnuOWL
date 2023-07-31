"""(Live Simulation only) This component reads OBJfiles with material files (while also generating a Radiance skyfile), and renders Daylight Coefficient Matrices for 4 principal orientations and for the zenith facing vector for each occupant position, as precursor to Radiance grid-based illuminance simulations.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        caseName: Name for the specific case. 
        objFile: Takes location of .obj files. Connect to the output node of ExportOBJ component.
        mtlFile: Takes location of Material file (in .RAD format) from GenMat component.
        pointFile_H: pointfile for zenith-facing horizontal position.
        pointFile_N: pointfile for north-facing vertical view.
        pointFile_E: pointfile for east-facing vertical view.
        pointFile_S: pointfile for south-facing vertical view.
        pointFile_W: pointfile for west-facing vertical view.
        runIt: A boolean toggle to run this component. True = Live, False = Precache
    Output:
        DCmtx_H: Location of the saved .mtx file containing pointwise Daylight Coefficients for zenith-facing horizontal position.
        DCmtx_N: Location of the saved .mtx file containing pointwise Daylight Coefficients for north-facing vertical view.
        DCmtx_E: Location of the saved .mtx file containing pointwise Daylight Coefficients for east-facing vertical view.
        DCmtx_S: Location of the saved .mtx file containing pointwise Daylight Coefficients for south-facing vertical view.
        DCmtx_W: Location of the saved .mtx file containing pointwise Daylight Coefficients for west-facing vertical view."""

import rhinoscriptsyntax as rs
import os
from subprocess import call
self=ghenv.Component
self.Name = "SCALE_DCMtxV"
self.NickName = 'DCMtxV'
self.Message = 'AnnuOWL | DCMtxV\nAUG_15_2023'
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
    ptFileH=os.path.basename(pointFile_H)
    ptFileN=os.path.basename(pointFile_N)
    ptFileE=os.path.basename(pointFile_E)
    ptFileS=os.path.basename(pointFile_S)
    ptFileW=os.path.basename(pointFile_W)
    os.chdir(folder)   
    num_linesH = sum(1 for line in open(pointFile_H))
    call(["cmd","/C","rfluxmtx -I+ -y "+str(num_linesH)+" -lw 0.0001 -ab 5 -ad 10000 -n 16 - "+sfile+" -i scene.oct < "+ptFileH+" > "+str(caseName)+"_illumH.mtx"])
    num_linesN = sum(1 for line in open(pointFile_N))
    call(["cmd","/C","rfluxmtx -I+ -y "+str(num_linesN)+" -lw 0.0001 -ab 5 -ad 10000 -n 16 - "+sfile+" -i scene.oct < "+ptFileN+" > "+str(caseName)+"_illumN.mtx"])
    num_linesE = sum(1 for line in open(pointFile_E))
    call(["cmd","/C","rfluxmtx -I+ -y "+str(num_linesE)+" -lw 0.0001 -ab 5 -ad 10000 -n 16 - "+sfile+" -i scene.oct < "+ptFileE+" > "+str(caseName)+"_illumE.mtx"])
    num_linesS = sum(1 for line in open(pointFile_S))
    call(["cmd","/C","rfluxmtx -I+ -y "+str(num_linesS)+" -lw 0.0001 -ab 5 -ad 10000 -n 16 - "+sfile+" -i scene.oct < "+ptFileS+" > "+str(caseName)+"_illumS.mtx"])
    num_linesW = sum(1 for line in open(pointFile_W))
    call(["cmd","/C","rfluxmtx -I+ -y "+str(num_linesW)+" -lw 0.0001 -ab 5 -ad 10000 -n 16 - "+sfile+" -i scene.oct < "+ptFileW+" > "+str(caseName)+"_illumW.mtx"])
    return folder+str(caseName)+"_illumH.mtx",folder+str(caseName)+"_illumN.mtx",folder+str(caseName)+"_illumE.mtx",folder+str(caseName)+"_illumS.mtx",folder+str(caseName)+"_illumW.mtx"

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
    DCmtx_fnmH,DCmtx_fnmN,DCmtx_fnmE,DCmtx_fnmS,DCmtx_fnmW=Obj2HDR(sstr,objFile)
    if os.path.exists(DCmtx_fnmH):
        DCmtx_H=DCmtx_fnmH
    if os.path.exists(DCmtx_fnmN):
        DCmtx_N=DCmtx_fnmN
    if os.path.exists(DCmtx_fnmE):
        DCmtx_E=DCmtx_fnmE
    if os.path.exists(DCmtx_fnmS):
        DCmtx_S=DCmtx_fnmS
    if os.path.exists(DCmtx_fnmW):
        DCmtx_W=DCmtx_fnmW
