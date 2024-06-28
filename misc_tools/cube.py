import maya.cmds as cmds

def create_cube():
    ctrlCV = cmds.curve(n="ctrl_cube_#",d=1,p=[(0,0,0),(1,0,0),(1,0,1),(0,0,1),(0,0,0),
                                    (0,1,0),(1,1,0),(1,0,0),(1,1,0),
                                    (1,1,1),(1,0,1),(1,1,1),
                                    (0,1,1),(0,0,1),(0,1,1),(0,1,0)])
                
    cmds.CenterPivot()
    cmds.xform(ctrlCV,t=(-.5,-.5,-.5))
    cmds.select(ctrlCV)
    cmds.FreezeTransformations()
    cmds.delete(ctrlCV, ch=1)
    
    return ctrlCV
