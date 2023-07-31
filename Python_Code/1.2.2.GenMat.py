"""
This component generates a 'materials.rad' file at the intended folder, for performing the obj2mesh function inside Obj2HDR component.
mtlFile connects to the Obj2HDR input, and options-output contains possible materials for using as mtlName in ExportOBJ component.
Regenerates the materials.rad file in su2rad repository (maintained by Thomas Bleicher) at https://github.com/tbleicher/su2rad/blob/master/su2rad/su2radlib/ray/materials.rad
Additional material data (3-channel) taken from spectral-database (spectraldb.com) maintained by Alstan Jakubiec and {Design for Climate & Comfort Lab} at UToronto.
---
OWL (Occupant Well-being through Lighting) is developed by Marshal Maskarenj, for SCALE project funded by FNRS @ LAB, UCLouvain.
    Inputs:
        folder: Location of the folder where the materials.rad file needs to be saved.
        runIt: A boolean toggle to run this component.
    Output:
        mtlFile: location of the generated materials.rad file to be connected with Obj2HDR component input.
        options: Connect to a panel to view the possible materials, which may be used as mtlName in the ExportOBJ component."""

import rhinoscriptsyntax as rs
self=ghenv.Component
self.Name = "SCALE_GenMat"
self.NickName = 'GenMat'
self.Message = 'AnnuOWL | GenMat\nAUG_15_2023'
self.IconDisplayMode = self.IconDisplayMode.application
try: self.AdditionalHelpFromDocStrings = "2"
except: pass

if runIt==True:
    material_def=str("void plastic diffuse_0\n0\n0\n5 0.85 0.83 0.92 0 0\n\n" + \
                    "void plastic Roof\n0\n0\n5 0.8394 0.8284 0.7931 0.0009 0.3000\n\nvoid plastic Ceiling\n0\n0\n5 0.8394 0.8284 0.7931 0.0009 0.3000\n\n" + \
                    "void plastic Walls\n0\n0\n5 0.6589 0.5826 0.4518 0.0015 0.2000\n\nvoid plastic Workstation\n0\n0\n5 0.6824 0.5060 0.2227 0.0055 0.2000\n\n" + \
                    "void plastic Monitor\n0\n0\n5 0.9278 0.5337 0.5139 0.9486 0.1000\n\nvoid plastic Carpet\n0\n0\n5 0.1555 0.1556 0.1461 0.0001 0.3000\n\n" + \
                    "void glass Glazing\n0\n0\n3 0.989889      1 0.984464\n\n" + \
                    "void plastic white_roughcast\n0\n0\n5 0.726 0.706 0.633     0     0\n\nvoid metal new_galvanised_sheet_metal\n0\n0\n5 0.623 0.672 0.692   0.5   0.1\n\n" + \
                    "void plastic bush_leaf\n0\n0\n5 0.1226 0.1773 0.0191 0.0000 0.0000\n \n" + \
                    "void plastic tree_foliage\n0\n0\n5 0.1176 0.1523 0.0558 0.0011 0.2000\n \n" + \
                    "void plastic red_brick\n0\n0\n5 0.1295 0.0967 0.0737 0.0000 0.3000\n \n" + \
                    "void plastic greenish-white_ALBA\n0\n0\n5 0.612 0.683 0.628     0     0\n\nvoid plastic cellular_concrete_YTONG\n0\n0\n5 0.576 0.549  0.53     0     0\n\n" + \
                    "void plastic maple_wood\n0\n0\n5 0.689 0.511 0.298     0     0\n\nvoid plastic poplar_wood\n0\n0\n5 0.653 0.497 0.291     0     0\n\n" + \
                    "void plastic white_pine_wood\n0\n0\n5 0.683 0.477  0.26     0     0\n\nvoid plastic light_painted_concrete\n0\n0\n5 0.493  0.51 0.499     0     0\n\n" + \
                    "void plastic hornbeam_wood\n0\n0\n5 0.619 0.473 0.286     0     0\n\nvoid plastic red_pine_wood\n0\n0\n5 0.667 0.452 0.231     0     0\n\n" + \
                    "void plastic chalky_silicate_brick\n0\n0\n5 0.499 0.487 0.458     0     0\n\nvoid metal oxidized_aluminium\n0\n0\n5 0.487 0.481 0.436   0.3   0.2\n\n" + \
                    "void plastic dirty-white_ALBA\n0\n0\n5  0.51 0.473 0.412     0     0\n\nvoid plastic Scots_pine_wood\n0\n0\n5  0.64 0.415 0.195     0     0\n\n" + \
                    "void plastic arolle_wood\n0\n0\n5 0.645 0.374 0.162     0     0\n\nvoid plastic linden_wood\n0\n0\n5 0.591 0.382 0.196     0     0\n\n" + \
                    "void plastic light_concrete\n0\n0\n5  0.47 0.403 0.337     0     0\n\nvoid plastic   ash_wood\n0\n0\n5 0.544 0.362 0.208     0     0\n\nvoid plastic blue-gray_ETERNIT\n0\n0\n5 0.287 0.429 0.372     0     0\n\n" + \
                    "void plastic Oregon_pine_wood\n0\n0\n5 0.588 0.329 0.154     0     0\n\nvoid plastic cream-white_gravel\n0\n0\n5 0.452 0.369 0.259     0     0\n\n" + \
                    "void plastic chesnut_wood\n0\n0\n5 0.525 0.344  0.19     0     0\n\nvoid plastic limba_wood\n0\n0\n5 0.485 0.344  0.17     0     0\n\nvoid plastic light_Simplon_granite\n0\n0\n5 0.355 0.361 0.348     0     0\n\n" + \
                    "void plastic birch_wood\n0\n0\n5 0.494 0.313 0.181     0     0\n\nvoid plastic hemlock_wood\n0\n0\n5 0.503 0.309 0.168     0     0\n\nvoid plastic larch_wood\n0\n0\n5 0.528 0.294  0.14     0     0\n\n" + \
                    "void plastic pink_ETERNIT\n0\n0\n5 0.473 0.287 0.259     0     0\n\nvoid plastic   elm_wood\n0\n0\n5  0.46 0.271 0.134     0     0\n\nvoid plastic light_blue_ETERNIT\n0\n0\n5 0.249   0.3 0.332     0     0\n\n" + \
                    "void plastic cement_brick_2\n0\n0\n5 0.356 0.269 0.225     0     0\n\nvoid plastic light_terra_cotta_brick\n0\n0\n5 0.427 0.242 0.146     0     0\n\nvoid metal old_galvanised_sheet_metal\n0\n0\n5 0.259 0.276  0.27   0.3   0.2\n\n" + \
                    "void plastic beech_wood\n0\n0\n5 0.413 0.214 0.125     0     0\n\nvoid plastic blue_ETERNIT\n0\n0\n5 0.234 0.251  0.26     0     0\n\nvoid plastic cement_block\n0\n0\n5  0.27 0.226 0.203     0     0\n\n" + \
                    "void plastic   oak_wood\n0\n0\n5 0.329 0.199   0.1     0     0\n\nvoid plastic textured_dark_terra_cotta_brick\n0\n0\n5 0.392 0.163 0.087     0     0\n\nvoid plastic dark_terra_cotta_brick\n0\n0\n5 0.364 0.155 0.097     0     0\n\n" + \
                    "void plastic medium_concrete\n0\n0\n5 0.244 0.194 0.145     0     0\n\nvoid plastic cherry_wood\n0\n0\n5 0.334  0.16 0.077     0     0\n\nvoid plastic cement_brick_1\n0\n0\n5 0.196   0.2 0.189     0     0\n\n" + \
                    "void plastic auburn_ETERNIT\n0\n0\n5 0.341 0.148 0.113     0     0\n\nvoid plastic parquet_wood\n0\n0\n5 0.309 0.165 0.083     0     0\n\nvoid plastic  teak_wood\n0\n0\n5  0.28 0.153 0.071     0     0\n\n" + \
                    "void plastic textured_light_terra_cotta_brick\n0\n0\n5 0.252 0.145 0.097     0     0\n\nvoid plastic violet_ETERNIT\n0\n0\n5 0.189 0.155 0.159     0     0\n\nvoid plastic dark_concrete\n0\n0\n5 0.216 0.145 0.106     0     0\n\n" + \
                    "void plastic dark_Ticino_granite\n0\n0\n5 0.194 0.143 0.123     0     0\n\nvoid plastic agglomerate_wood_fiber\n0\n0\n5  0.17 0.147 0.107     0     0\n\nvoid plastic  pear_wood\n0\n0\n5 0.246   0.1 0.068     0     0\n\n" + \
                    "void metal oxidized_copper\n0\n0\n5 0.136 0.102 0.083   0.3   0.2\n\nvoid plastic walnut_wood\n0\n0\n5 0.156 0.093 0.068     0     0\n\nvoid plastic shiny_black_granite\n0\n0\n5 0.101 0.098 0.103  0.03  0.01\n\n" + \
                    "void glass clear_glass_4\n0\n0\n3      1      1      1\n\nvoid glass float_glass_3\n0\n0\n3 0.989889      1 0.984464\n\nvoid glass float_glass_6\n0\n0\n3 0.982293      1 0.987719\n\n" + \
                    "void texfunc gran_tex\n4 gran_dx gran_dy gran_dz plink.cal\n0\n0\ngran_tex glass granular_glass_6\n0\n0\n3 0.982293      1 0.987719\n\n" + \
                    "void texfunc mar_tex\n4 mar_dx mar_dy mar_dz plink.cal\n0\n0\nmar_tex glass hammered_glass_4\n0\n0\n3 0.999655 0.999655 0.999655\n\n" + \
                    "void glass safety_glass_8\n0\n0\n3 0.982293      1 0.987719\n\nvoid brightfunc arm_pat\n2 arm_wire plink.cal\n0\n0\narm_pat glass rough_wire-reinforced_glass_7\n0\n0\n3 0.90304 0.97144 0.918244\n\n" + \
                    "void glass smooth_wire-reinforced_glass_6.5\n0\n0\n3 0.804159 0.99857 0.866106\n\nvoid glass DIAPLUS_glass_6\n0\n0\n3 0.868279 0.883488 0.834593\n\nvoid glass light_gray_tinted_glass_6\n0\n0\n3 0.453656 0.500507 0.456925\n\n" + \
                    "void glass light_brown_tinted_glass_6\n0\n0\n3 0.480896 0.467821 0.362101\n\nvoid glass bronze_tinted_glass_10\n0\n0\n3 0.400253 0.390443 0.290142\n")
    savefilepath=folder+"materials.rad"
    with open(savefilepath, "w") as f:
        f.write(material_def)
    mtlFile = savefilepath
    options = "PLASTIC\ndiffuse_0\nRoof\nCeiling\nWalls\nWorkstation\nMonitor\nCarpet\nwhite_roughcast\nbush_leaf\ntree_foliage\nred_brick\ngreenish-white_ALBA\ncellular_concrete_YTONG\nmaple_wood\npoplar_wood\nwhite_pine_wood\nlight_painted_concrete\nhornbeam_wood\nred_pine_wood\n" + \
                "chalky_silicate_brick\ndirty-white_ALBA\nScots_pine_wood\narolle_wood\nlinden_wood\nlight_concrete\nash_wood\nblue-gray_ETERNIT\nOregon_pine_wood\ncream-white_gravel\nchesnut_wood\nlimba_wood\nlight_Simplon_granite\nbirch_wood\nhemlock_wood\n" + \
                "larch_wood\npink_ETERNIT\nelm_wood\nlight_blue_ETERNIT\ncement_brick_2\nlight_terra_cotta_brick\nbeech_wood\nblue_ETERNIT\ncement_block\noak_wood\ntextured_dark_terra_cotta_brick\ndark_terra_cotta_brick\nmedium_concrete\ncherry_wood\ncement_brick_1\n" + \
                "auburn_ETERNIT\nparquet_wood\nteak_wood\ntextured_light_terra_cotta_brick\nviolet_ETERNIT\ndark_concrete\ndark_Ticino_granite\nagglomerate_wood_fiber\npear_wood\nwalnut_wood\nshiny_black_granite\n\nMETAL\noxidized_aluminium\nnew_galvanised_sheet_metal\n" + \
                "old_galvanised_sheet_metal\noxidized_copper\n\nGLASS\nGlazing\nclear_glass_4\nfloat_glass_3\nfloat_glass_6\nsafety_glass_8\nsmooth_wire-reinforced_glass_6.5\nDIAPLUS_glass_6\nlight_gray_tinted_glass_6\nlight_brown_tinted_glass_6\nbronze_tinted_glass_10\n\n" + \
                "FUNC\ngran_tex\nmar_tex\narm_pat\n\n"