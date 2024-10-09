import maya.cmds as cmds

class jiggle_it():
    def __init__(self):
        selected_vertices = self.get_vertex()

        for vertex in selected_vertices:
            self.make_rivet(vertex)

    def get_vertex(self):
        selected_vertices = cmds.ls(selection=True, flatten=True)
    
        if not selected_vertices:
            print("No vertices selected.")
            return

        for x in selected_vertices:
            if ".vtx[" not in x:
                cmds.warning(f"Selection is not a vertex. {x}")
        

        return selected_vertices
    
    def make_rivet(self, vertex):
        side = "L"

        cmds.select(vertex)
        cmds.Rivet()
        rivet = "pinOutput"

        rivet = cmds.rename(rivet, f"rivet_{side}#")

        ctrl = cmds.sphere(r=5)[0]
        ctrl = cmds.rename(ctrl, f"ctrl_jiggle_{side}#")
        cmds.matchTransform(ctrl, rivet)

        cmds.parent(ctrl, rivet)
        cmds.select(clear=True)
        joint = cmds.joint(name=f"jnt_jiggle_{side}#", r=5)
        cmds.matchTransform(joint, rivet)
        cmds.makeIdentity(joint, apply=True, t=False, r=True, s=False)
        
        cmds.parentConstraint(ctrl, joint)
