"""The second one of the two components designed to display pre-cached geometry of the scene on the Rhino canvas.
If Display is set to TRUE, Objects such as windows, ceiling, glazing, etc, saved as .obj files in each pre-simulated (or live) folder, are imported and displayed. 
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        paths: the paths of each .obj file in the pre-simulated folder. This node takes data from the first Show-Geometry component
        Display: A True/False button for displaying geometry in Rhino Canvas. Set TRUE to display, FALSE to hide.
    Output:
        Geo: The geometry imported from the pre-simulated folder."""

import Rhino.Geometry as rg
self=ghenv.Component
self.Name = "SCALE_ShowGeomB"
self.NickName = 'ShowGeomB'
self.Message = 'AnnuOWL | ShowGeomB\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "1"
except: pass
file = open(paths)
lines = file.readlines()

if Display==True:
    mesh = rg.Mesh()
    for line in lines:
        if line.find("v")==0 and line.find("n")==-1 and line.find("t")==-1:
            #print line.split(' ')
            mesh.Vertices.Add(rg.Point3d(float((line.split(' '))[1]),float((line.split(' '))[2]),float((line.split(' '))[3])))
        if line.find("f")==0:
            if line.split(' ').Count==4:
                mesh.Faces.AddFace(rg.MeshFace(int(line.split(' ')[1].split('/')[0])-1,int(line.split(' ')[2].split('/')[0])-1,int(line.split(' ')[3].split('/')[0])-1))
            if line.split(' ').Count==5:
                mesh.Faces.AddFace(rg.MeshFace(int(line.split(' ')[1].split('/')[0])-1,int(line.split(' ')[2].split('/')[0])-1,int(line.split(' ')[3].split('/')[0])-1,int(line.split(' ')[4].split('/')[0])-1))
    mesh.Normals.ComputeNormals()
    mesh.Compact()
    Geo = mesh