"""This component makes a legend for OVNIs performance in the defined palettes. The legend can be placed and rescaled based on user inputs. 5 Color palettes are supported. 
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Lgnd_Posn: Legend position on rhino viewport, defined through a 3D point.
        Lgnd_Scl: A slider input for rescaling legends.
        palette: Slider input for selecting color palettes. 5 supported options.
    Output:
        AllGeo: Geometry of legend, connects to CustomPreview.
        AllMat: Materials/Colors of legend, connects to CustomPreview."""

import rhinoscriptsyntax as rs
import ghpythonlib as gl
import math
import Rhino
import scriptcontext as sc
self=ghenv.Component
self.Name = "SCALE_OVNIlgnd"
self.NickName = 'OVNIlgnd'
self.Message = 'AnnuOWL | OVNIlgnd\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "2"
except: pass

def funcRed(inp,i,pV,minV,delV):
    x=(inp[i]-minV)/delV
    valh=int(inp[i])
    if pV==0: #Excel
        if valh==0:
            return(255)#248)
        if valh==1:
            return(255)#252)
        if valh==2:
            return(255)#204)
        if valh==3:
            return(0)#99)
    if pV==1:
        return(int(0.95*(-514.96*x*x*x + 534.91*x*x + 228.79*x))) #inferno
    if pV==2:
        return(int((-10334)*(x**6) + 30183*(x**5) - 31427*(x**4) + 13563*(x**3) - 2396.3*(x**2) + 665.22*x + 0.2224)) #BlueRedYellow
    if pV==3:
        return(int(-5849.7*(x**6) + 16812*(x**5) - 16593*(x**4) + 6187.5*(x**3) - 793.56*(x**2) + 394.3*x + 77.368)) #BlueYellowRed
    if pV==4:
        return(int(-6437.9*(x**6) + 25115*(x**5) - 37770*(x**4) + 25002*(x**3) - 6257.1*(x**2) + 485.71*x + 2.7612))  #BlueGreenYellowRed

def funcGreen(inp,i,pV,minV,delV):
    x=(inp[i]-minV)/delV
    valh=int(inp[i])
    if pV==0: #Excel
        if valh==0:
            return(0)#105)
        if valh==1:
            return(165)#191)
        if valh==2:
            return(255)#221)
        if valh==3:
            return(255)#190)
    if pV==1:
        return(int(162.59*x*x*x + 51.923*x*x + 39.196*x + 0.6084)) #inferno
    if pV==2:
        return(int(6163.2*(x**6) - 18876*(x**5) + 20028*(x**4) - 8372*(x**3) + 1382.2*(x**2) - 70.303*x - 0.1108)) #BlueRedYellow
    if pV==3:
        return(int(-7777.8*(x**6) + 22628*(x**5) - 22861*(x**4) + 9160.5*(x**3) - 1718.1*(x**2) + 497.55*x + 107.31)) #BlueYellowRed
    if pV==4:
        return(int(8995.1*(x**6) - 26873*(x**5) + 35110*(x**4) - 25796*(x**3) + 9247*(x**2) - 686.54*x + 21.309)) #BlueGreenYellowRed

def funcBlue(inp,i,pV,minV,delV):
    x=(inp[i]-minV)/delV
    valh=int(inp[i])
    if pV==0: #Excel
        if valh==0:
            return(0)#107)
        if valh==1:
            return(0)#123)
        if valh==2:
            return(0)#130)
        if valh==3:
            return(0)#123)
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

def GeomLgnd():
    pt2=gl.components.Move(point,gl.components.UnitY(2*size))[0]
    pt2b=gl.components.Move(pt2,gl.components.UnitX(3*size))[0]
    lgndGrd=gl.components.Rectangular(pt2b,30*size,6*size,4,1)[0]
    return lgndGrd

if True:
    point=Lgnd_Posn
    size=Lgnd_Scl/2
    LgndNum=[0,1,2,3]
    Lgnd_Mtl,dlt1,dlt2=illum2mat(LgndNum,False,3)
    Lgnd_Geo=GeomLgnd()
    Lgnd_Mat=Lgnd_Mtl
    txt1="[INNER HEMISPHERE] Daylight Performance according to EN-17037"
    txt2="SUFFICIENCY       ||      TARGET ILLUMINANCE: 0=Insufficient, 1=Minimum, 2=Medium, 3=High"
    txt3="[INNER RING] NON VISUAL POTENTIAL (CIRCADIAN STIMULUS AUTONOMY)"
    txt4="WELL-BEING       ||      Ensuring Circadian Autonomy: 0=Insufficient, 1=Min, 2=Med, 3=High"
    txt5="[MIDDLE RING] Protection from DISCOMFORT GLARE according to EN-17037"
    txt6="COMFORT       ||      Avoidance of Glare Risk : 0=Insufficient, 1=Min, 2=Med, 3=High"
    txt7="[OUTER RING] View Quality according to EN-17037"
    txt8="SATISFACTION      ||     QUALITY OF VIEW: 0=Insufficient, 1=Min, 2=Med, 3=High"
    txt9="0"
    txt10="1"
    txt11="2"
    txt12="3"
    pt_org=point
    pos1a=gl.components.Move(pt_org,gl.components.UnitY(40*size))[0]
    pos1=gl.components.Move(pos1a,gl.components.UnitX(-12*size))[0]
    pos2a=gl.components.Move(pt_org,gl.components.UnitY(36*size))[0]
    pos2=gl.components.Move(pos2a,gl.components.UnitX(-10*size))[0]
    pos3a=gl.components.Move(pt_org,gl.components.UnitY(32*size))[0]
    pos3=gl.components.Move(pos3a,gl.components.UnitX(-14*size))[0]
    pos4a=gl.components.Move(pt_org,gl.components.UnitY(28*size))[0]
    pos4=gl.components.Move(pos4a,gl.components.UnitX(-12*size))[0]
    pos5a=gl.components.Move(pt_org,gl.components.UnitY(24*size))[0]
    pos5=gl.components.Move(pos5a,gl.components.UnitX(-21*size))[0]
    pos6a=gl.components.Move(pt_org,gl.components.UnitY(20*size))[0]
    pos6=gl.components.Move(pos6a,gl.components.UnitX(-4*size))[0]
    pos7a=gl.components.Move(pt_org,gl.components.UnitY(16*size))[0]
    pos7=gl.components.Move(pos7a,gl.components.UnitX(3*size))[0]
    pos8a=gl.components.Move(pt_org,gl.components.UnitY(12*size))[0]
    pos8=gl.components.Move(pos8a,gl.components.UnitX(-4*size))[0]
    pos9=gl.components.Move(pt_org,gl.components.UnitX(15*size))[0]
    pos10=gl.components.Move(pt_org,gl.components.UnitX(45*size))[0]
    pos11=gl.components.Move(pt_org,gl.components.UnitX(75*size))[0]
    pos12=gl.components.Move(pt_org,gl.components.UnitX(105*size))[0]
    sizetxt=5*size
    Lgnd_Cap1=legendcaption(sizetxt,txt1,pos1)
    Lgnd_Cap2=legendcaption(0.75*sizetxt,txt2,pos2)
    Lgnd_Cap3=legendcaption(sizetxt,txt3,pos3)
    Lgnd_Cap4=legendcaption(0.75*sizetxt,txt4,pos4)
    Lgnd_Cap5=legendcaption(sizetxt,txt5,pos5)
    Lgnd_Cap6=legendcaption(0.75*sizetxt,txt6,pos6)
    Lgnd_Cap7=legendcaption(sizetxt,txt7,pos7)
    Lgnd_Cap8=legendcaption(0.75*sizetxt,txt8,pos8)
    Lgnd_Cap9=legendcaption(2*sizetxt,txt9,pos9)
    Lgnd_Cap10=legendcaption(2*sizetxt,txt10,pos10)
    Lgnd_Cap11=legendcaption(2*sizetxt,txt11,pos11)
    Lgnd_Cap12=legendcaption(2*sizetxt,txt12,pos12)
    Lgnd_Cap=Lgnd_Cap1+Lgnd_Cap2+Lgnd_Cap3+Lgnd_Cap4+Lgnd_Cap5+Lgnd_Cap6+Lgnd_Cap7+Lgnd_Cap8+Lgnd_Cap9+Lgnd_Cap10+Lgnd_Cap11+Lgnd_Cap12
    LgndCpMtrl=[]
    for i in range(len(Lgnd_Cap1)):
        LgndCpMtrl.append("120,80,80")
    for i in range(len(Lgnd_Cap2)):
        LgndCpMtrl.append("150,100,100")
    for i in range(len(Lgnd_Cap3)):
        LgndCpMtrl.append("80,80,120")
    for i in range(len(Lgnd_Cap4)):
        LgndCpMtrl.append("100,100,150")
    for i in range(len(Lgnd_Cap5)):
        LgndCpMtrl.append("80,80,80")
    for i in range(len(Lgnd_Cap6)):
        LgndCpMtrl.append("100,100,100")
    for i in range(len(Lgnd_Cap7)):
        LgndCpMtrl.append("80,120,80")
    for i in range(len(Lgnd_Cap8)):
        LgndCpMtrl.append("100,150,100")
    for i in range(len(Lgnd_Cap9)):
        LgndCpMtrl.append("180,180,180")
    for i in range(len(Lgnd_Cap10)):
        LgndCpMtrl.append("120,120,120")
    for i in range(len(Lgnd_Cap11)):
        LgndCpMtrl.append("60,60,60")
    for i in range(len(Lgnd_Cap12)):
        LgndCpMtrl.append("0,0,0")
    AllGeo=Lgnd_Geo+Lgnd_Cap
    AllMat=Lgnd_Mat+LgndCpMtrl