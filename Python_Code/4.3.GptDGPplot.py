import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import matplotlib.pyplot as plt 
from matplotlib import cm
from matplotlib.cm import ScalarMappable
plt.style.use('dark_background')
import math
import csv
import os

if True:
    folder=os.path.dirname(DGP_AnnVis_N)
    rows_DGPN = []
    with open(DGP_AnnVis_N, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_DGPN.append(row)
    r_DGPN=list(map(list, zip(*rows_DGPN)))
    x=np.linspace(1,365,365)
    y=np.linspace(1,24,24)
    x,y=np.meshgrid(x,y)
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.contourf(x,y,r_DGPN,levels=np.linspace(0.184,0.42,10),cmap=cm.hot)
    plt.colorbar()
#    plt.axis('off')
    plt.xlabel('Day of Year')
    plt.ylabel('Hour of Day')
    plt.title("Daylight Glare Probability at selected position, facing North, through the year")
    #plt.show()
    plt.savefig(folder+'/DGP_North_graph.png',bbox_inches='tight')
    plt.close()

    rows_DGPE = []
    with open(DGP_AnnVis_E, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_DGPE.append(row)
    r_DGPE=list(map(list, zip(*rows_DGPE)))
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.contourf(x,y,r_DGPE,levels=np.linspace(0.184,0.42,10),cmap=cm.hot)
    plt.colorbar()
#    plt.axis('off')
    plt.xlabel('Day of Year')
    plt.ylabel('Hour of Day')
    plt.title("Daylight Glare Probability at selected position, facing East, through the year")
    plt.savefig(folder+'/DGP_East_graph.png',bbox_inches='tight')
    plt.close()

    rows_DGPS = []
    with open(DGP_AnnVis_S, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_DGPS.append(row)
    r_DGPS=list(map(list, zip(*rows_DGPS)))
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.contourf(x,y,r_DGPS,levels=np.linspace(0.184,0.42,10),cmap=cm.hot)
    plt.colorbar()
#    plt.axis('off')
    plt.xlabel('Day of Year')
    plt.ylabel('Hour of Day')
    plt.title("Daylight Glare Probability at selected position, facing South, through the year")
    plt.savefig(folder+'/DGP_South_graph.png',bbox_inches='tight')
    plt.close()

    rows_DGPW = []
    with open(DGP_AnnVis_W, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_DGPW.append(row)
    r_DGPW=list(map(list, zip(*rows_DGPW)))
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.contourf(x,y,r_DGPW,levels=np.linspace(0.184,0.42,10),cmap=cm.hot)
    plt.colorbar()
    plt.axis('off')
    plt.xlabel('Day of Year')
    plt.ylabel('Hour of Day')
    plt.title("Daylight Glare Probability at selected position, facing West, through the year")
    plt.savefig(folder+'/DGP_West_graph.png',bbox_inches='tight')
    plt.close()

    Plot_N=folder+'/DGP_North_graph.png'
    Plot_E=folder+'/DGP_East_graph.png'
    Plot_S=folder+'/DGP_South_graph.png'
    Plot_W=folder+'/DGP_West_graph.png'