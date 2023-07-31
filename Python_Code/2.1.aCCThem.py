"""Extraction of pre-calculated Hemispherical CCT from the .aowl file.  
The accompanying python-based utility can be used to convert the EPW weather data for any defined location to respective Annual Spectal data for unobstructed sky hemisphere. 
The utility follows the approach recommended in doi.org/10.1016/j.enbuild.2022.112012.
A combination of Perez model with spectral sky models (doi.org/10.1177/1477153520982265) calculates hourly patch CCT, which is then converted to patch SPD following CIE015 standard.
Merging patch SPD with cosine correction generates relative combined SPD of sky hemisphere. Tristimulus X,Y,Z values are evaluated and then chromaticity coordinates x, and y (and complementary z) are derived by factoring. 
McCamy's equation (1992) is used to derive CCT from chromaticity coordinates x and y for each hour.
--
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        ASO_file: Link to the Annual Spectral output file in the .aowl format for extracting zenith luminance through the annual hours. 
    Output:
        MCCT_Hem: The hemispherical CCT through each hour of the year."""
        

import rhinoscriptsyntax as rs
import os
import csv
import ghpythonlib as gl
import Rhino
import scriptcontext as sc
self=ghenv.Component
self.Name = "SCALE_aCCThem"
self.NickName = 'aCCThem'
self.Message = 'AnnuOWL | aCCThem\nAUG_15_2023'
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
    folder=os.path.dirname(ASO)+"/"
    Spect_data=ASO
    rows_Cillumx = []
    with open(Spect_data, 'r') as csvfile:
        next(csvfile)
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_Cillumx.append(row)
    rows_CCT=[None for i in range (8760)]
    for i in range (0,8760,1):
        rows_CCT[i]=rows_Cillumx[i][10]
    for i in range (0,8760,1):
        if rows_CCT[i]=='-':
            rows_CCT[i]=0
    rows_CCT=[float(ic) for ic in rows_CCT]
    for i in range (0,8760,1):
        if rows_CCT[i]<-1:
            rows_CCT[i]=1225
    MtlCCT=rows_CCT
    MCCT_Hem=MtlCCT