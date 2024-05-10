import maya.cmds as cmds

class colour():
    def __init__(self):
        self.selection = cmds.ls(sl=True)
        self.collect_all_ctrls()

    def collect_all_ctrls(self):
        COLOR_CONFIG = {'_l': 6, '_r': 13, 'default': 22}
        ctrls = cmds.listRelatives(self.selection, ad=True, typ="transform")
        if ctrls is None:
            ctrls = self.selection
        else:
            ctrls.append(self.selection[0])
        for ctrl in ctrls:    
            if ctrl[:4] == "ctrl":
                side = ctrl[-2:]
                cmds.setAttr(f"{ctrl}.overrideEnabled", 1)
                try:
                    cmds.setAttr(f"{ctrl}.overrideColor",
                                 COLOR_CONFIG[side])
                except KeyError:
                    cmds.setAttr(f"{ctrl}.overrideColor",
                                 COLOR_CONFIG['default'])
                    pass
            else:
                cmds.error("Curve not coloured as does not match 'ctrl' prefix")
                    
# colour()
