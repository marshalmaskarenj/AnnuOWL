"""
This component exports selected rhino geometry as .obj files for further processing in Radiance commandline.
Groups of objects with similar material compositions (eg: Walls, or Glazing, etc) should be selected together in the geometry for parallel export -- ideally using Rhino layers.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        selectgeo: Connect to a grasshopper Geometry object, which has Rhino objects/Layers via 'Set Multiple Geometries'. 
        folder: Location of the folder where the .obj files are to be saved.
        caseName: Name for the specific case
        mtlName: case-specific name for the objects with same material (eg: Walls, Glazing, etc). Look at GenMat options for the possible material names.
        runIt: A boolean toggle to run this component.
    Output:
        objFile: Location of the saved object file for further processing."""


import rhinoscriptsyntax as rs
import Rhino 
import os
self=ghenv.Component
self.Name = "SCALE_ExportOBJ"
self.NickName = 'ExportOBJ'
self.Message = 'AnnuOWL | ExportOBJ\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass

def ExportObj():
    objcs=[]
    for i in range(selectgeo.BranchCount):
        for n in range(selectgeo.Branches[i].Count):
            geom = selectgeo.Branches[i][n]
            objc=Rhino.RhinoDoc.ActiveDoc.Objects.Add(geom)
            objcs.append(objc)
    for objval in objcs:
        Rhino.RhinoDoc.ActiveDoc.Objects.Select(objval)
    filepath = folder + caseName+"_"+mtlName+".obj"
    cmd = "_-Export " + "\"" + filepath + "\"" + " _Enter _Enter"
    Rhino.RhinoApp.RunScript(cmd, False)
    Rhino.RhinoDoc.ActiveDoc.Objects.Delete(objcs,True)
    
    with open(filepath, 'r') as file :
        filedata = file.read()
    filedata = filedata.replace('diffuse_0', str(mtlName))
    with open(filepath, 'w') as file:
        file.write(filedata)
    print('done')
    os.remove(folder + caseName+"_"+mtlName+".mtl")
    return filepath

if runIt==True:
    objFile=ExportObj()