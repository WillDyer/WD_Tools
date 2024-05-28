import maya.cmds as cmds
import maya.OpenMaya as om
import importlib
import sys, os, math
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import ramp_values
import OPM
importlib.reload(ramp_values)
importlib.reload(OPM)

class ribbon():
    def __init__(self):
        #self.group_setup()
        self.ctrl_amount = 3
        self.fk_enabled = 1
        self.selection = cmds.ls(sl=1)

        self.top_grp = cmds.group(n="grp_ribbon_#", em=1)
        self.base_ribbon()
        self.create_controllers()
        self.group_setup()
        self.skin_ribbon()
        cmds.select(clear=1)

    def base_ribbon(self):
        
        # Collect span count
        print(f"selection: {self.selection[0]}")
        surface = cmds.listRelatives(self.selection[0],s=1)[0]

        self.spansU = cmds.getAttr(f"{self.selection[0]}.spansU")
        self.spansV = cmds.getAttr(f"{self.selection[0]}.spansV")

        # selected surface is periodic or open? (cylinder or a plane)
        if cmds.getAttr(surface + ".formU") == 2 or cmds.getAttr(surface + ".formV") == 2: # Check for closed
            curve_type = "periodic"
            spans = self.spansU
        elif cmds.getAttr(surface + ".formU") == 0 or cmds.getAttr(surface + ".formV") == 0: # check not closed
            curve_type = "open"
            spans = self.spansU + 1

        u_curve_corr = cmds.duplicateCurve(self.selection[0] + ".v[.5]", local=True, ch=0)[0]
        param_ctrls = ramp_values.param_from_length(u_curve_corr, spans, curve_type, "uv", delete_curve=False)
        self.skn_ctrls = ramp_values.param_from_length(u_curve_corr, self.ctrl_amount, curve_type, "uv", delete_curve=True)

        self.fol_shape_list = []
        self.fol_parent_list = []
        for x in range(spans):
            fol_shape = cmds.createNode("follicle")
            fol_parent = cmds.listRelatives(fol_shape, p=True)[0]
            cmds.setAttr(fol_shape + ".visibility", 1)

            cmds.setAttr(f"{fol_shape}.simulationMethod",0)
            
            cmds.connectAttr(f"{surface}.worldMatrix[0]",f"{fol_shape}.inputWorldMatrix")
            cmds.connectAttr(f"{surface}.local", f"{fol_shape}.inputSurface")

            cmds.connectAttr(f"{fol_shape}.outRotate",f"{fol_parent}.rotate")
            cmds.connectAttr(f"{fol_shape}.outTranslate",f"{fol_parent}.translate")

            cmds.setAttr(f"{fol_shape}.parameterV",0.5)
            cmds.setAttr(f"{fol_shape}.parameterU",param_ctrls[x])

            cmds.select(fol_parent)
            cmds.joint(n=f"jnt_fol_{fol_parent}")

            self.fol_shape_list.append(fol_shape)
            self.fol_parent_list.append(fol_parent)

    def create_controllers(self):
        cmds.select(cl=1)

        self.ctrl_list = []
        self.skn_jnt_list = []

        fol_list_int = len(self.fol_parent_list)
        for x in self.skn_ctrls:
            item = fol_list_int * x
            item = math.ceil(item)
            if item == 0:
                item = 1

            selected_follicle = self.fol_parent_list[item-1]
            cmds.select(selected_follicle)
            cmds.joint(n=f"jnt_ctrl_{selected_follicle}",r=3)
            cmds.parent(f"jnt_ctrl_{selected_follicle}",world=True)
            cmds.select(cl=1)
            self.skn_jnt_list.append(f"jnt_ctrl_{selected_follicle}")

            ctrl = f"ctrl_{selected_follicle}"
            cmds.circle(n=ctrl,r=1) # temporary, will make interchangable
            cmds.matchTransform(ctrl,f"jnt_ctrl_{selected_follicle}")
            cmds.parentConstraint(ctrl,f"jnt_ctrl_{selected_follicle}",mo=1, n=f"pConst_jnt_ctrl_{selected_follicle}")
            cmds.connectAttr(f"{ctrl}.scale", f"jnt_ctrl_{selected_follicle}.scale")
            cmds.select(ctrl)
            OPM.offsetParentMatrix()
            self.ctrl_list.append(ctrl)

    def group_setup(self):
        cmds.group(self.ctrl_list, n="grp_ribbon_ctrl", p=self.top_grp)
        cmds.group(self.skn_jnt_list, n="grp_ribbon_skn_jnt", p=self.top_grp)
        cmds.group(self.fol_parent_list, n="grp_ribbon_fol", p=self.top_grp)

    def skin_ribbon(self):
        print(self.skn_jnt_list)
        print(self.selection[0])
        cmds.skinCluster(self.skn_jnt_list, self.selection[0])
