import maya.cmds as cmds

def insert_offset_isoparms(nurbs_surface, param_value, offset=0.01):
    """
    Inserts isoparms at specified offsets from an existing isoparm.
    
    Args:
        nurbs_surface (str): The name of the NURBS surface.
        param_value (float): The parameter value of the existing isoparm.
        offset (float): The offset value for the new isoparms.
    """
    
    # Calculate the new parameter values
    param_value_plus = param_value + offset
    param_value_minus = param_value - offset
    
    # Insert the isoparms
    cmds.insertKnotSurface(nurbs_surface, d=1, p=param_value_plus)
    cmds.insertKnotSurface(nurbs_surface, d=1, p=param_value_minus)

def run():
    selected_surface = cmds.ls(selection=True)
    if selected_surface:
        nurbs_surface = selected_surface[0]
        # Specify the parameter value of the existing isoparm (e.g., 0.5)
        existing_param_value = 0.8
        # Insert isoparms at offsets of 0.01 on either side
        insert_offset_isoparms(nurbs_surface, existing_param_value, offset=0.01)
    else:
        print("Please select a NURBS surface.")