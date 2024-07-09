import maya.cmds as cmds

class ribbon_twist():
    def __init__(self):
        selected_surface = cmds.ls(selection=True)
        if selected_surface:
            print("i changed")
            self.nurbs_surface = selected_surface[0]
            iso_list = self.select_isoparms(UV="U")
            self.insert_offset_isoparms(iso_list)
        else:
            print("Please select a NURBS surface.")
    
    def select_isoparms(self, UV):
        surface_info = cmds.createNode('surfaceInfo')

        cmds.connectAttr(f"{self.nurbs_surface}.worldSpace[0]", f"{surface_info}.inputSurface", f=True)

        iso_list = cmds.getAttr(f"{surface_info}.knots{UV}")[0]
        iso_list = list(dict.fromkeys(iso_list))
        print(iso_list)
        cmds.delete(surface_info)
        return iso_list

    def insert_offset_isoparms(self, iso_list):
        offset = 0.01
        for iso in iso_list:
            print(iso)
            # Calculate the new parameter values
            param_value_plus = iso + offset
            param_value_minus = iso - offset
            
            # Insert the isoparms
            cmds.insertKnotSurface(self.nurbs_surface, d=1, p=param_value_plus, rpo=1)
            cmds.insertKnotSurface(self.nurbs_surface, d=1, p=param_value_minus, rpo=1)
            cmds.delete(self.nurbs_surface, constructionHistory = True)

def main():
    run = ribbon_twist()
