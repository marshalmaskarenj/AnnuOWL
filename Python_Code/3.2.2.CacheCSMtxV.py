"""A pre-cached alternative of the CSMtxV component.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        folder: Location of pre-simulated folder.
        runIt: A toggle switch. False = Precache, True = Live
    Output:
        Ann_CS_N: A pre-simulated csv file containing Annual hourly CS (vertical plane) for each occupant position, facing North. 
        Ann_CS_E: A pre-simulated csv file containing Annual hourly CS (vertical plane) for each occupant position, facing East. 
        Ann_CS_S: A pre-simulated csv file containing Annual hourly CS (vertical plane) for each occupant position, facing South. 
        Ann_CS_W: A pre-simulated csv file containing Annual hourly CS (vertical plane) for each occupant position, facing West. """

import rhinoscriptsyntax as rs
import csv
self=ghenv.Component
self.Name = "SCALE_CacheCSMtxV"
self.NickName = 'CacheCSMtxV'
self.Message = 'AnnuOWL | CacheCSMtxV\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

if runIt==False:
    Ann_CS_N=folder+'/ann_CS_N.csv'
    Ann_CS_E=folder+'/ann_CS_E.csv'
    Ann_CS_S=folder+'/ann_CS_S.csv'
    Ann_CS_W=folder+'/ann_CS_W.csv'
