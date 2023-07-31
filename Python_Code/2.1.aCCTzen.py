"""
Hemispherical CCT using Zenith Luminance.  This component takes in the annual zenith luminance data from the weather file (in this case, the pre-simulated .aowl file, but can also take from the EPW file) and evaluates the Annual CCT for the zenith patch. The zenith-patch CCT is assumed as hemispherical CCT. For better resolution, use the aCCThem component's output. 
The luminance to CCT conversion is done using the Diakite-Knoop 2021 model (Refer to https://doi.org/10.1177%2F1477153520982265 by Diakite-Kortlever and Knoop for more about this model).
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        ASO_file: Link to the Annual Spectral output file in the .aowl format for extracting zenith luminance through the annual hours. 
    Output:
        MCCT_Zen: The CCT of the zenith patch through each hour of the year. Zenith CCT is being assumed equal to hemishperical CCT, use the [aCCThem] component for higher complexity in calculations"""

import rhinoscriptsyntax as rs
import os
import csv
import ghpythonlib as gl
import Rhino
import math
import scriptcontext as sc
self=ghenv.Component
self.Name = "SCALE_aCCTzen"
self.NickName = 'aCCTzen'
self.Message = 'AnnuOWL | aCCTzen\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "2"
except: pass

def CCTtoRGB(CCT,Cschm):
    CCT=float(CCT)
    if CCT<0:
        CCT=0
    if Cschm == 0:
        if CCT<10000:
            Rd = -0.00000000000000001795*(CCT**5) + 0.00000000000044588538*(CCT**4) - 0.00000000372232456327*(CCT**3) + 0.0000109864090986002*(CCT**2) - 0.0137001932551949*CCT + 260.769111669703
            Gn = -0.00000000000000000527*(CCT**5) + 0.00000000000003655271*(CCT**4) + 0.00000000167614975728*(CCT**3) - 0.0000275671281750254*(CCT**2) + 0.153377592369099*CCT - 46.8338890434172
            Bl = -0.00000000000000008737*(CCT**5) + 0.00000000000273034705*(CCT**4) - 0.00000003194049197454*(CCT**3) + 0.00016733122602172*(CCT**2) - 0.33493947880853*CCT + 218.478923481698
        else:
            Rd = -0.000000000000000000005641*(CCT**5) + 0.0000000000000008097902099*(CCT**4) - 0.0000000000415000000072372*(CCT**3) + 0.000000911876457055929*(CCT**2) - 0.0101362470877943*CCT + 208.166666664777
            Gn= 0.0000000000000000000002051*(CCT**5) - 0.0000000000000000424242424*(CCT**4) + 0.0000000000042773892786236*(CCT**3) - 0.000000203181818235956*(CCT**2) + 0.00334748251954915*CCT + 228.999999971494
            Bl= -0.0000000000000000000006154*(CCT**5) + 0.000000000000000103962704*(CCT**4) - 0.0000000000065198135206772*(CCT**3) + 0.000000168310023306091*(CCT**2) - 0.000724498832868009*CCT + 226.999999970977
    else:
        if 1<CCT<1000:
            CCT=1000
        if CCT>12000:
            CCT=12000
        if CCT<6500:
            Rd=255
            Gn=0.00000000132815332815*(CCT**3) - 0.0000211135531135532*(CCT**2) + 0.126411218411213*CCT - 43.6184926184615
            Bl=0.00000000000121445221*(CCT**4) - 0.00000001993654493653*(CCT**3) + 0.000109645104895004*(CCT**2) - 0.177071807821103*CCT + 83.5205905193757
        else:
            Rd=-0.000000000144004144*(CCT**3) + 0.00000596514596515146*(CCT**2) - 0.0843394013394504*CCT + 590.103119103286
            Gn= -0.00000000013053613054*(CCT**3) + 0.00000463936063936288*(CCT**2) - 0.0589843489843631*CCT + 472.266733266794
            Bl=255
    if CCT==0:
        Rd=0
        Gn=0
        Bl=63
    if Rd<0:
        Rd=0
    if Rd>255:
        Rd=255
    if Gn<0:
        Gn=0
    if Gn>255:
        Gn=255
    if Bl<0:
        Bl=0
    if Bl>255:
        Bl=255
    RedVal=int(Rd)
    GrnVal=int(Gn)
    BluVal=int(Bl)
    RGB_out=str(RedVal)+","+str(GrnVal)+","+str(BluVal)
    return RedVal,GrnVal,BluVal

def GeomCCT():
    geoval=gl.components.Rectangular(point,size*1,size*4,365,24)[0]
    return geoval

def GeomLgnd():
    pt2=gl.components.Move(point,gl.components.UnitX(380*size))[0]
    lgndGrd=gl.components.Rectangular(pt2,8*size,4*size,1,24)[0]
    return lgndGrd


def mtakagi(lum):
    CCT=6500+((1.1985*10**8)/(lum**1.2))
    return CCT

def mchain99(lum):
    CCT=(10**6)/(-132.1+59.77*math.log10(lum))
    return CCT

def mchain04(lum):
    LCF=120
    CCT=(10**6)/(181.35233+LCF*(-4.22630+math.log10(lum)))
    return CCT

def mrusnak(lum):
    p=10.2
    q=0.26
    CCT=(10**6)/(p*(lum**q))
    return CCT

def legendcaption(size,txt,pos):
    textsize= float(size)
    print(textsize)
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

if True:
    ASO=ASO_file
#    point=rs.CreatePoint(0,0,0) if point is None else point
#    size=0.3 if size is None else float(size)
    #ColorSchm=False if ColorSchm is None else ColorSchm
#    if ColorSchm=="CIE 1931":
#        Cschm=0
#    else:
#        Cschm=1
#    print(size)
    folder=os.path.dirname(ASO)+"/"
    Spect_data=ASO
    rows_Cillumx = []
    with open(Spect_data, 'r') as csvfile:
        next(csvfile)
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_Cillumx.append(row)
    rows_zlum=[None for i in range (8760)]
    for i in range (0,8760,1):
        rows_zlum[i]=rows_Cillumx[i][2]

    rows_zlum=[float(ic) for ic in rows_zlum]
    rows_mCCT=[None for i in range (8760)]
    for i in range (0,8760,1):
        if float(rows_zlum[i])<250:
            rows_mCCT[i]=mchain99(250)
        elif 250<float(rows_zlum[i])<3172:
            rows_mCCT[i]=mchain99(float(rows_zlum[i]))
        elif 3172<float(rows_zlum[i])<5200:
            rows_mCCT[i]=mrusnak(float(rows_zlum[i]))
        elif float(rows_zlum[i])>5200:
            rows_mCCT[i]=mchain04(float(rows_zlum[i]))
        else:
            mval=float(rows_zlum[i])
            rows_mCCT[i]=5000
    for i in range (0,8760,1):
        if float(rows_zlum[i])==0:
            rows_mCCT[i]=0
    for i in range (0,8760,1):
        if rows_mCCT[i]>25000:
            rows_mCCT[i]=25000
    MLum=rows_zlum
    MCCT=rows_mCCT
#    CCT_Mtl=[]
#    for i in range(8760):
#        cvl=CCTtoRGB(rows_mCCT[i],Cschm)
#        CCT_Mtl.append(CCTtoRGB(rows_mCCT[i],Cschm))
#    Lgnd_Mtl=[]
#    for i in range(1000,13000,500):
#        LgndVal=i
#        Lgnd_Mtl.append(CCTtoRGB(LgndVal,Cschm))
#    CCT_Geo=GeomCCT()
#    CCT_Mtrl=CCT_Mtl
#    Lgnd_Geo=GeomLgnd()
#    Lgnd_Mat=Lgnd_Mtl
#    txt1="1000 K"
#    txt2="12000 K"
#    pos0=gl.components.Move(point,gl.components.UnitX(390*size))[0]
#    pos1=gl.components.Move(pos0,gl.components.UnitY(6*size))[0]
#    LgndCp=[]
#    sizetxt=10*size
#    Lgnd_Cap1=legendcaption(sizetxt,txt1,pos1)
#    pos2=gl.components.Move(pos1,gl.components.UnitY(90*size))[0]
#    Lgnd_Cap2=legendcaption(sizetxt,txt2,pos2)
#    pos3a=gl.components.Move(pos2,gl.components.UnitY(5*size))[0]
#    pos3=gl.components.Move(pos3a,gl.components.UnitX(-10*size))[0]
#    txt3="CCT in Kelvins"
#    Lgnd_Cap3=legendcaption(sizetxt/2,txt3,pos3)
#    pos4a=gl.components.Move(pos3,gl.components.UnitX(-360*size))[0]
#    pos4=gl.components.Move(pos4a,gl.components.UnitY(1*size))[0]
#    if Cschm==0:
#        txt4="Annual outdoor horizontal CCT (based on Zenith Luminance): represented in CIE 1931 RGB"
#    else:
#        txt4="Annual outdoor horizontal CCT (based on Zenith Luminance): in Blackbody Radiation RGB"
#    Lgnd_Cap4=legendcaption(sizetxt/1.3,txt4,pos4)
#    Lgnd_Cap=Lgnd_Cap1+Lgnd_Cap2+Lgnd_Cap3+Lgnd_Cap4#LgndCp
#    LgndCpMtrl=[]
#    for i in range(len(Lgnd_Cap)):
#        LgndCpMtrl.append((0,0,0))
#    AllGeo=CCT_Geo+Lgnd_Geo+Lgnd_Cap
#    AllMat=CCT_Mtrl+Lgnd_Mat+LgndCpMtrl
    MCCT_Zen=MCCT