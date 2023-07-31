import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import matplotlib.pyplot as plt 
from matplotlib import cm
plt.style.use('dark_background')
import math
import csv
import os

if True:
    folder=os.path.dirname(OccupH_f)
    rows_Oz = []
    with open(OccupH_f, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rows_Oz.append(row)
    r_Oz=list(map(list, zip(*rows_Oz)))
    x=np.linspace(1,365,365)
    y=np.linspace(1,24,24)
    x,y=np.meshgrid(x,y)
    fig, ax = plt.subplots(figsize=(12, 4))
    plt.contourf(x,y,r_Oz,cmap=cm.hot) #levels=np.linspace(-1,1,3),
    plt.colorbar()
#    plt.axis('off')
    plt.xlabel('Day of Year')
    plt.ylabel('Hour of Day')
    plt.title("Occupancy Hours defined for this simulation [0=Vacant,1=Occupied]")
    #plt.show()
    plt.savefig(folder+'/Occupancy_graph.png',bbox_inches='tight')
    plt.close()



    OccupH_G=folder+'/Occupancy_graph.png'

    #os.remove(CS_AnnVis_N)
    #os.remove(CS_AnnVis_E)
    #os.remove(CS_AnnVis_S)
    #os.remove(CS_AnnVis_W)