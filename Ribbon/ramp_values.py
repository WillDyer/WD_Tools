import maya.cmds as cmds
import maya.OpenMaya as om

def param_from_length(curve, count, curve_type = "open", space = "uv", normalized=True, delete_curve=True):

    if curve_type == "periodic":
        divider = count
    else:
        divider = count - 1

    if divider==0:
        divider = 1
       
    dag = om.MDagPath()
    obj = om.MObject()
    crv = om.MSelectionList()
    crv.add(curve)
    crv.getDagPath(0, dag, obj)

    curve_fn = om.MFnNurbsCurve(dag)
    length = curve_fn.length()

    param = [curve_fn.findParamFromLength(i * ((1 / float(divider)) * length)) for i in range(count)]

    if space == "world":
        data=[]
        space = om.MSpace.kWorld
        point = om.MPoint()
        for p in param:
            curve_fn.getPointAtParam(p, point, space)
            data.append([point[0], point[1], point[2]]) #world space points
    elif normalized == True:

        def normalizer(value, old_range, new_range): 
            return (value - old_range[0]) * (new_range[1] - new_range[0]) / (old_range[1] - old_range[0]) + new_range[0]
        
        max_v = cmds.getAttr(curve + ".minMaxValue.maxValue")
        min_v = cmds.getAttr(curve + ".minMaxValue.minValue")

        data = [normalizer(p, [min_v, max_v], [0, 1]) for p in param] 
    else:
        data = param

    if delete_curve == True:
        cmds.delete(curve)
    else:
        pass
    return data