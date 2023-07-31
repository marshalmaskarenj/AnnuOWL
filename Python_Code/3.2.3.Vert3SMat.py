"""This component takes in the glare protection performance for each orientation, and calculates the color (material) for visualisation, depending upon the selected palette.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        DGP_N: The glare protection performance of each occupant-position, facing North (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)
        DGP_E: The glare protection performance of each occupant-position, facing East (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)
        DGP_S: The glare protection performance of each occupant-position, facing South (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)
        DGP_W: The glare protection performance of each occupant-position, facing West (0 = Non Compliant, 1=Minimum, 2=Medium, 3=High)
    Output:
        DGP_Mat: Combined materials for all orientations. Connects to Custom Preview"""

import rhinoscriptsyntax as rs
import ghpythonlib as gl
import math
import Rhino
self=ghenv.Component
self.Name = "SCALE_Vert3SMat"
self.NickName = 'Vert3SMat'
self.Message = 'AnnuOWL | Vert3SMat\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "3"
except: pass

def funcRed(inp,i,pV,minV,delV):
    if delV==0:
        delV=0.0001
    x=(inp[i]-minV)/delV
    valh=int(inp[i])
    if pV==0: #Excel
        if valh==0:
            return(255)
        if valh==1:
            return(255)
        if valh==2:
            return(255)
        if valh==3:
            return(0)
    if pV==1:
        return(int(0.95*(-514.96*x*x*x + 534.91*x*x + 228.79*x))) #inferno
    if pV==2:
        return(int((-10334)*(x**6) + 30183*(x**5) - 31427*(x**4) + 13563*(x**3) - 2396.3*(x**2) + 665.22*x + 0.2224)) #BlueRedYellow
    if pV==3:
        return(int(-5849.7*(x**6) + 16812*(x**5) - 16593*(x**4) + 6187.5*(x**3) - 793.56*(x**2) + 394.3*x + 77.368)) #BlueYellowRed
    if pV==4:
        return(int(-6437.9*(x**6) + 25115*(x**5) - 37770*(x**4) + 25002*(x**3) - 6257.1*(x**2) + 485.71*x + 2.7612))  #BlueGreenYellowRed

def funcGreen(inp,i,pV,minV,delV):
    if delV==0:
        delV=0.0001
    x=(inp[i]-minV)/delV
    valh=int(inp[i])
    if pV==0: #Excel
        if valh==0:
            return(0)
        if valh==1:
            return(165)
        if valh==2:
            return(255)
        if valh==3:
            return(255)
    if pV==1:
        return(int(162.59*x*x*x + 51.923*x*x + 39.196*x + 0.6084)) #inferno
    if pV==2:
        return(int(6163.2*(x**6) - 18876*(x**5) + 20028*(x**4) - 8372*(x**3) + 1382.2*(x**2) - 70.303*x - 0.1108)) #BlueRedYellow
    if pV==3:
        return(int(-7777.8*(x**6) + 22628*(x**5) - 22861*(x**4) + 9160.5*(x**3) - 1718.1*(x**2) + 497.55*x + 107.31)) #BlueYellowRed
    if pV==4:
        return(int(8995.1*(x**6) - 26873*(x**5) + 35110*(x**4) - 25796*(x**3) + 9247*(x**2) - 686.54*x + 21.309)) #BlueGreenYellowRed

def funcBlue(inp,i,pV,minV,delV):
    if delV==0:
        delV=0.0001
    x=(inp[i]-minV)/delV
    valh=int(inp[i])
    if pV==0: #Excel
        if valh==0:
            return(0)
        if valh==1:
            return(0)
        if valh==2:
            return(0)
        if valh==3:
            return(0)
    if pV==1:
        return(int(1228.4*x*x*x - 1928.1*x*x + 897.1*x)) #inferno
    if pV==2:
        return(int(7750.2*(x**6) - 22478*(x**5) + 22931*(x**4) - 9372.6*(x**3) + 1525.5*(x**2) - 607.58*x + 252.04)) #BlueRedYellow
    if pV==3:
        return(int(20825*(x**6) - 67331*(x**5) + 80585*(x**4) - 41998*(x**3) + 7857.6*(x**2) - 102.94*x + 168.91)) #BlueYellowRed
    if pV==4:
        return(int(3464.1*(x**6) - 18245*(x**5) + 29899*(x**4) - 18380*(x**3) + 2561.1*(x**2) + 553.21*x + 148.59)) #BlueGreenYellowRed

def illum2mat(inp,scl,uT):
    if scl==False:
        minV=0
        maxV=uT
    else:
        minV=min(inp)
        maxV=max(inp)
    delV=maxV-minV
    lenI=len(inp)
    clrAr=[[None,None,None] for i in range(lenI)]
    pV=4 if palette is None else int(palette)
    Mat_II=[]
    for i in range (0, lenI,1):
        clrAr[i]=[funcRed(inp,i,pV,minV,delV),funcGreen(inp,i,pV,minV,delV),funcBlue(inp,i,pV,minV,delV)]
        Mat_II.append("("+str(clrAr[i][0])+","+str(clrAr[i][1])+","+str(clrAr[i][2])+")")
    return (Mat_II,minV,maxV)

if True:
    if DGP_N:
        maxvalN=3
    if DGP_E:
        maxvalE=3
    if DGP_S:
        maxvalS=3
    if DGP_W:
        maxvalW=3
    upperThres=max(maxvalN,maxvalE,maxvalS,maxvalW)
    #print(maxvalN,maxvalE,maxvalS,maxvalW,upperThres)
    if DGP_N:
        Mat_N,minN,maxN=illum2mat(DGP_N,False,3)
    else:
        Mat_N="No input found for Annual simplified Daylight Glare Probability (N)"
    if DGP_E:
        Mat_E,minE,maxE=illum2mat(DGP_E,False,3)
    else:
        Mat_E="No input found for Annual simplified Daylight Glare Probability (E)"
    if DGP_S:
        Mat_S,minS,maxS=illum2mat(DGP_S,False,3)
    else:
        Mat_S="No input found for Annual simplified Daylight Glare Probability (S)"
    if DGP_W:
        Mat_W,minW,maxW=illum2mat(DGP_W,False,3)
    else:
        Mat_W="No input found for Annual simplified Daylight Glare Probability (W)"
    DGP_min=str(minN)+","+str(minE)+","+str(minS)+","+str(minW)
    DGP_max=str(maxN)+","+str(maxE)+","+str(maxS)+","+str(maxW)
    #print(minN,minE,minS,minW,maxN,maxE,maxS,maxW)
    DGP_Mat=Mat_N + Mat_E + Mat_S + Mat_W
#    print(Mat_N)
    print(Mat_W)

