import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import matplotlib.pyplot as plt 
from matplotlib import cm
plt.style.use('dark_background')
import math
import csv
import os

if True:
    folder=os.path.dirname(CS_AnnVis_N)
    rows_CSN = []
    with open(CS_AnnVis_N, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_CSN.append(row)
    r_CSN=list(map(list, zip(*rows_CSN)))
    x=np.linspace(1,365,365)
    y=np.linspace(1,24,24)
    x,y=np.meshgrid(x,y)
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.contourf(x,y,r_CSN, cmap=cm.jet)
    plt.colorbar()
#    plt.axis('off')
    plt.xlabel('Day of Year')
    plt.ylabel('Hour of Day')
    plt.title("Circadian Stimulus at selected position, facing North, through the year")
    #plt.show()
    plt.savefig(folder+'/CS_North_graph.png',bbox_inches='tight')
    plt.close()

    rows_CSE = []
    with open(CS_AnnVis_E, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_CSE.append(row)
    r_CSE=list(map(list, zip(*rows_CSE)))
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.contourf(x,y,r_CSE, cmap=cm.jet)
    plt.colorbar()
#    plt.axis('off')
    plt.xlabel('Day of Year')
    plt.ylabel('Hour of Day')
    plt.title("Circadian Stimulus at selected position, facing East, through the year")
    plt.savefig(folder+'/CS_East_graph.png',bbox_inches='tight')
    plt.close()

    rows_CSS = []
    with open(CS_AnnVis_S, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_CSS.append(row)
    r_CSS=list(map(list, zip(*rows_CSS)))
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.contourf(x,y,r_CSS, cmap=cm.jet)
    plt.colorbar()
#    plt.axis('off')
    plt.xlabel('Day of Year')
    plt.ylabel('Hour of Day')
    plt.title("Circadian Stimulus at selected position, facing South, through the year")
    plt.savefig(folder+'/CS_South_graph.png',bbox_inches='tight')
    plt.close()

    rows_CSW = []
    with open(CS_AnnVis_W, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_CSW.append(row)
    r_CSW=list(map(list, zip(*rows_CSW)))
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.contourf(x,y,r_CSW, cmap=cm.jet)
    plt.colorbar()
    plt.xlabel('Day of Year')
    plt.ylabel('Hour of Day')
    plt.title("Circadian Stimulus at selected position, facing West, through the year")
#    plt.axis('off')
    plt.savefig(folder+'/CS_West_graph.png',bbox_inches='tight')
    plt.close()

    Plot_N=folder+'/CS_North_graph.png'
    Plot_E=folder+'/CS_East_graph.png'
    Plot_S=folder+'/CS_South_graph.png'
    Plot_W=folder+'/CS_West_graph.png'

    #os.remove(CS_AnnVis_N)
    #os.remove(CS_AnnVis_E)
    #os.remove(CS_AnnVis_S)
    #os.remove(CS_AnnVis_W)