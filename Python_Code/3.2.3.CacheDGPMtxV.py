"""A pre-cached alternative of the DGPMtxV component.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        folder: Location of pre-simulated folder.
        runIt: A toggle switch. False = Precache, True = Live
    Output:
        Ann_DGP_N: A pre-simulated csv file containing Annual hourly DGP (vertical plane) for each occupant position, facing North. 
        Ann_DGP_E: A pre-simulated csv file containing Annual hourly DGP (vertical plane) for each occupant position, facing East. 
        Ann_DGP_S: A pre-simulated csv file containing Annual hourly DGP (vertical plane) for each occupant position, facing South. 
        Ann_DGP_W: A pre-simulated csv file containing Annual hourly DGP (vertical plane) for each occupant position, facing West. """

import rhinoscriptsyntax as rs
import csv
self=ghenv.Component
self.Name = "SCALE_CacheDGPMtxV"
self.NickName = 'CacheDGPMtxV'
self.Message = 'AnnuOWL | CacheDGPMtxV\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass


if runIt==False:
    Ann_DGP_N=folder+'/ann_DGP_N.csv'
    Ann_DGP_E=folder+'/ann_DGP_E.csv'
    Ann_DGP_S=folder+'/ann_DGP_S.csv'
    Ann_DGP_W=folder+'/ann_DGP_W.csv'
