import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import matplotlib.pyplot as plt 
from matplotlib import cm
plt.style.use('dark_background')
import math
import csv
import os

if True:
    folder=os.path.dirname(CCTz_f)
    rows_Cz = []
    with open(CCTz_f, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_Cz.append(row)
    r_Cz=list(map(list, zip(*rows_Cz)))
    x=np.linspace(1,365,365)
    y=np.linspace(1,24,24)
    x,y=np.meshgrid(x,y)
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.contourf(x,y,r_Cz,levels=np.linspace(1500,15000,10),cmap=cm.coolwarm_r)
    plt.colorbar()
#    plt.axis('off')
    plt.xlabel('Day of Year')
    plt.ylabel('Hour of Day')
    plt.title("Annual outdoor horizontal hourly CCT based on Zenith Luminance(Kelvins)")
    #plt.show()
    plt.savefig(folder+'/Cz_graph.png',bbox_inches='tight')
    plt.close()

    rows_Ch = []
    with open(CCTh_f, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_Ch.append(row)
    r_Ch=list(map(list, zip(*rows_Ch)))
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.contourf(x,y,r_Ch,levels=np.linspace(1500,15000,10), cmap=cm.coolwarm_r)
    plt.colorbar()
#    plt.axis('off')
    plt.xlabel('Day of Year')
    plt.ylabel('Hour of Day')
    plt.title("Annual outdoor horizontal hourly CCT based on Hemispherical Luminance(Kelvins)")
    plt.savefig(folder+'/Ch_graph.png',bbox_inches='tight')
    plt.close()



    CCT_Zenith=folder+'/Cz_graph.png'
    CCT_Hemisp=folder+'/Ch_graph.png'

    os.remove(CCTz_f)
    os.remove(CCTh_f)
    #os.remove(CS_AnnVis_S)
    #os.remove(CS_AnnVis_W)