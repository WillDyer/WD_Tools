import importlib
import maya.cmds as cmds
import OPM

importlib.reload(OPM)


class CreateFkSystems():
    def __init__(self):
        self.system_joints = cmds.ls(sl=True)

        self.fk_system()

    def fk_system(self):
        primary_axis = (1, 0, 0) #xyz


        for x in self.system_joints:
            ctrls_fk = []
            jnt_ctrls_fk = []

            selection = cmds.listRelatives(x, ad=True, typ="joint")
            selection.append(x)

            for i in range(len(selection)):
                print(selection[i])
                cmds.circle(n=f"ctrl_fk_{selection[i]}",
                            r=1, nr=primary_axis)
                cmds.matchTransform(f"ctrl_fk_{selection[i]}",
                                    selection[i])
                if cmds.listRelatives(selection[i], c=True) is None:
                    cmds.delete(f"ctrl_fk_{selection[i]}")
                else:
                    ctrls_fk.append(f"ctrl_fk_{selection[i]}")
                    jnt_ctrls_fk.append(selection[i])

            for ctrl in range(len(ctrls_fk)):
                try:
                    cmds.parent(ctrls_fk[ctrl], ctrls_fk[ctrl+1])
                except IndexError:
                    pass

            for ctrl in ctrls_fk:
                cmds.select(ctrl)
                OPM.offsetParentMatrix()

            self.fk_system_to_joint(ctrls_fk, jnt_ctrls_fk)

    def fk_system_to_joint(self, ctrls_fk, jnt_ctrls_fk):
        for item in range(len(ctrls_fk)):
            cmds.parentConstraint(ctrls_fk[item],
                                  jnt_ctrls_fk[item],
                                  n=f"pConst_{ctrls_fk[item]}",mo=1)

#CreateFkSystems()
