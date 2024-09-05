import maya.cmds as cmds

class mouth():
    def __init__(self):
        self.tmp_variables()
        self.create_guide_locators()
        self.create_joints()

    def tmp_variables(self):
        self.main_controls = {"L_corner": [-6,0,0],
                         "R_corner": [6,0,0],
                         "C_top": [0,2,0],
                         "C_bottom": [0,-2,0]}
        self.between_controls = {"L1_top": [-4,1,0],
                            "L2_top": [-2,1,0],
                            "L1_bottom": [-4,-1,0],
                            "L2_bottom": [-2,-1,0],
                            "R1_top": [4,1,0],
                            "R2_top": [2,1,0],
                            "R1_bottom": [4,-1,0],
                            "R2_bottom": [2,-1,0],}
        
    def create_guide_locators(self):
        for guide in self.main_controls:
            cmds.spaceLocator(n=guide)
            cmds.xform(guide, t=self.main_controls[guide])

        for guide in self.between_controls:
            cmds.spaceLocator(n=guide)
            cmds.xform(guide, t=self.between_controls[guide])

    def create_joints(self):
        self.jaw_joint = "jnt_jaw"
        cmds.select(clear=1)
        cmds.joint(n=self.jaw_joint, p=(0,0,-5),radius=0.2)
        cmds.setAttr(f"{self.jaw_joint}.drawStyle",2)

        all_controls = self.main_controls | self.between_controls
        for guide in all_controls:
            cmds.select(clear=1)
            loc = cmds.xform(guide, r=True, ws=True, q=True, t=True)
            #cmds.delete(guide)
            jnt_name = cmds.joint(n=f"jnt_{guide}", p=loc, radius=0.2)
            cmds.parent(jnt_name, self.jaw_joint)

    def create_controllers(self):
        cmds.group(n="grp")
