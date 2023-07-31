"""This component saves the divided floor/grid Surface as a .3DM file, to be imported for live and cached simulations later.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        Geo: Geometry of sub-patches imported from DefGpts.
        folder: Location of folder where live or cached files are stored.
        runIt: A boolean switch for this component. 
    Output:
        grdFile: Location of the 3DM file with divided surface geometry, for further Radiance processing and Rhino visualisation."""

import Rhino
import System
self=ghenv.Component
self.Name = "SCALE_exportSRF"
self.NickName = 'exportSRF'
self.Message = 'AnnuOWL | exportSRF\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

if runIt==True:
    target_layer="new layer"
    file_path = folder+"floorgrid.3dm"
    new_file = Rhino.FileIO.File3dm()
    layers = new_file.AllLayers
    layer_index = layers.AddLayer(target_layer, System.Drawing.Color.Aqua)
    new_attributes = Rhino.DocObjects.ObjectAttributes()
    new_attributes.LayerIndex = layer_index
    for brep in Geo:  
        new_file.Objects.AddBrep(brep, new_attributes)
    
    print new_file.Write(file_path, 0)
    grdFile=file_path