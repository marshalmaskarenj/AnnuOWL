"""This component takes in the data to be visualised over the grid (Metric from CBDM_H) and converts that to rhino material for visualisation.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Lgnd_Posn: Legend Position as a point on Rhino.
        Lgnd_Scl: Slider to resize the legend.
        Lgnd_unit: CBDM-specific textual description. Takes data from CBDM_H component.
        sDAscore: sDA performance of the design for Minimum, Medium and High performance. Takes input from CBDM_H component.
        Data: The grid-based data to be visualised.
        palette: (0-5) a slider for different visualisaiton palettes. Default is 0.
    Output:
        Mat: Material for each geometry subpatch for visualisation through Custom Preview component.
        Lg_Geo: Geometry of the Legend.
        Lg_Mat: Material/colors of the legend. connects to Custom Preview along with Geometry"""

import rhinoscriptsyntax as rs
import ghpythonlib.components as gc
import math
import Rhino
import scriptcontext as sc
self=ghenv.Component
self.Name = "SCALE_HorzSMat"
self.NickName = 'HorzSMat'
self.Message = 'AnnuOWL | HorzSMat\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

def legendcaption(size,txt,pos):
    textsize= float(size)
    #print(textsize)
    sc.doc = Rhino.RhinoDoc.ActiveDoc
    rs.EnableRedraw(False)
    textsize=textsize*0.4
    txtObj = rs.AddText(txt,pos,textsize,"Stencil",1)
    txtCurves = rs.ExplodeText(txtObj)
    rs.DeleteObject(txtObj)
    list_lgn = []
    for i in range(len(txtCurves)):
        txtCurve = txtCurves[i]
        txtCurveGH = rs.coercecurve(txtCurve)
        list_lgn.append(txtCurveGH)
    rs.EnableRedraw(True)
    rs.DeleteObjects(txtCurves)
    sc.doc = ghdoc
    return list_lgn

def funcRed(i,illum,pV,delV):
    if delV==0:
        delV=0.0001
    x=(illum[i]-minV)/delV
    if pV==0:
        if x<0.1:
            return(230)
        elif x<0.2:
            return(235)
        elif x<0.3:
            return(240)
        elif x<0.4:
            return(245)
        elif x<0.5:
            return(250)
        elif x<0.6:
            return(255)
        elif x<0.7:
            return(251)
        elif x<0.8:
            return(167)
        elif x<0.9:
            return(84)
        elif x<0.95:
            return(42)
        else:
            return(0)
    if pV==1:
        return(int(0.95*(-514.96*x*x*x + 534.91*x*x + 228.79*x))) #inferno
    if pV==2:
        return(int((-10334)*(x**6) + 30183*(x**5) - 31427*(x**4) + 13563*(x**3) - 2396.3*(x**2) + 665.22*x + 0.2224)) #BlueRedYellow
    if pV==3:
        return(int(-5849.7*(x**6) + 16812*(x**5) - 16593*(x**4) + 6187.5*(x**3) - 793.56*(x**2) + 394.3*x + 77.368)) #BlueYellowRed
    if pV==4:
        return(int(-6437.9*(x**6) + 25115*(x**5) - 37770*(x**4) + 25002*(x**3) - 6257.1*(x**2) + 485.71*x + 2.7612))  #BlueGreenYellowRed

def funcGreen(i,illum,pV,delV):
    if delV==0:
        delV=0.0001
    x=(illum[i]-minV)/delV
    if pV==0:
        if x<0.1:
            return (0)
        elif x<0.2:
            return(42)
        elif x<0.3:
            return(85)
        elif x<0.4:
            return(128)
        elif x<0.5:
            return(171)
        elif x<0.6:
            return(214)
        elif x<0.7:
            return(255)
        elif x<0.8:
            return(245)
        elif x<0.9:
            return(235)
        elif x<0.95:
            return(228)
        else:
            return(225)
    if pV==1:
        return(int(162.59*x*x*x + 51.923*x*x + 39.196*x + 0.6084)) #inferno
    if pV==2:
        return(int(6163.2*(x**6) - 18876*(x**5) + 20028*(x**4) - 8372*(x**3) + 1382.2*(x**2) - 70.303*x - 0.1108)) #BlueRedYellow
    if pV==3:
        return(int(-7777.8*(x**6) + 22628*(x**5) - 22861*(x**4) + 9160.5*(x**3) - 1718.1*(x**2) + 497.55*x + 107.31)) #BlueYellowRed
    if pV==4:
        return(int(8995.1*(x**6) - 26873*(x**5) + 35110*(x**4) - 25796*(x**3) + 9247*(x**2) - 686.54*x + 21.309)) #BlueGreenYellowRed

def funcBlue(i,illum,pV,delV):
    if delV==0:
        delV=0.0001
    x=(illum[i]-minV)/delV
    if pV==0:
        return(0)
    if pV==1:
        return(int(1228.4*x*x*x - 1928.1*x*x + 897.1*x)) #inferno
    if pV==2:
        return(int(7750.2*(x**6) - 22478*(x**5) + 22931*(x**4) - 9372.6*(x**3) + 1525.5*(x**2) - 607.58*x + 252.04)) #BlueRedYellow
    if pV==3:
        return(int(20825*(x**6) - 67331*(x**5) + 80585*(x**4) - 41998*(x**3) + 7857.6*(x**2) - 102.94*x + 168.91)) #BlueYellowRed
    if pV==4:
        return(int(3464.1*(x**6) - 18245*(x**5) + 29899*(x**4) - 18380*(x**3) + 2561.1*(x**2) + 553.21*x + 148.59)) #BlueGreenYellowRed


if True:
    Scl=Lgnd_Scl*4
    Ptx=Lgnd_Posn
    Pt=gc.Move(Ptx,gc.UnitY(Scl*-4))[0]
    Pt1=gc.Move(Pt,gc.UnitX(Scl*2))[0]
    Pt2=gc.Move(Pt1,gc.UnitY(Scl*-11))[0]
    lgndGrd=gc.Rectangular(Pt2,2*Scl,1*Scl,1,11)[0]
    illum=Data
    minV=min(illum)
    maxV=max(illum)
    delV=maxV-minV
    lenI=len(illum)
    Mat_Ar=[]
    MatL_Ar=[]
    clrAr=[[None,None,None] for i in range(lenI)]
    pV=4 if palette is None else int(palette)
    for i in range (0, lenI,1):
        clrAr[i]=[funcRed(i,illum,pV,delV),funcGreen(i,illum,pV,delV),funcBlue(i,illum,pV,delV)]
    for i in range (0, lenI,1):
        Mat_Ar.append(str(clrAr[i][0])+","+str(clrAr[i][1])+","+str(clrAr[i][2]))
    intV=(maxV-minV)/10
    intValues=[minV+(10*intV),minV+(9*intV),minV+(8*intV),minV+(7*intV),minV+(6*intV),minV+(5*intV),minV+(4*intV),minV+(3*intV),minV+(2*intV),minV+(1*intV),minV+(0*intV)]
    minVL=min(intValues)
    maxVL=max(intValues)
    delVL=maxVL-minVL
    lenIL=len(intValues)
    clrArL=[[None,None,None] for i in range(lenIL)]
#    for view in rs.ViewNames(): 
#        rs.ViewDisplayMode(view, 'Rendered')
    for i in range (0, lenIL,1):
        clrArL[i]=[funcRed(i,intValues,pV,delVL),funcGreen(i,intValues,pV,delVL),funcBlue(i,intValues,pV,delVL)]
    for i in range (0, lenIL,1):
        MatL_Ar.append(str(clrArL[i][0])+","+str(clrArL[i][1])+","+str(clrArL[i][2]))
    sizetxt=Scl
    txt_Max=str(int(maxVL))
    txt_Min=str(int(minVL))
    txt_Lgd=Lgnd_unit
    Pt3=gc.Move(gc.Move(Pt1,gc.UnitX(Scl*2.2))[0],gc.UnitY(Scl*-0.2))[0]
    Pt4=gc.Move(gc.Move(Pt2,gc.UnitX(Scl*2.2))[0],gc.UnitY(Scl*0.8))[0]
    Pt5=gc.Move(gc.Move(Pt,gc.UnitX(Scl*1.5))[0],gc.UnitY(Scl*1.8))[0]
    Pt6=gc.Move(gc.Move(Pt,gc.UnitX(Scl*5.5))[0],gc.UnitY(Scl*-2))[0]
    Lgnd_CapMin=legendcaption(sizetxt,txt_Min,Pt3)
    Lgnd_CapMax=legendcaption(sizetxt,txt_Max,Pt4)
    Lgnd_CapLgd=legendcaption(sizetxt*0.6,txt_Lgd,Pt5)
    Lgnd_Score=legendcaption(sizetxt*0.9,sDAscore,Pt6)
    Lgnd_Cap=Lgnd_CapMin+Lgnd_CapMax+Lgnd_CapLgd+Lgnd_Score
    LgndCpMtrl=[]
    for i in range(len(Lgnd_Cap)):
        LgndCpMtrl.append("0,0,0")
    Mat=Mat_Ar
    Lgnd=Lgnd_Cap
    Lg_Geo=lgndGrd+Lgnd_Cap
    Lg_Mat=MatL_Ar+LgndCpMtrl