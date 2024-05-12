import maya.cmds as cmds
import maya.OpenMaya as om

def param_from_length(curve, count, curve_type = "open", space = "uv", normalized=True):

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

    cmds.delete(curve)
    return data

class ribbon():
    def __init__(self):
        #self.group_setup()
        self.base_ribbon()
        
    def base_ribbon(self):
        self.ctrl_amount = 3
        self.fk_enabled = 1
        
        # Collect span count
        selection = cmds.ls(sl=1)
        print(f"selection: {selection[0]}")
        surface = cmds.listRelatives(selection[0],s=1)[0]

        self.spansU = cmds.getAttr(f"{selection[0]}.spansU")
        self.spansV = cmds.getAttr(f"{selection[0]}.spansV")

        u_curve_corr = cmds.duplicateCurve(selection[0] + ".v[.5]", local=True, ch=0)[0]
        # selected surface is periodic or open? (cylinder or a plane)
        if cmds.getAttr(surface + ".formU") == 2 or cmds.getAttr(surface + ".formV") == 2: # Check for closed
            curve_type = "periodic"
            spans = self.spansU
        elif cmds.getAttr(surface + ".formU") == 0 or cmds.getAttr(surface + ".formV") == 0: # check not closed
            curve_type = "open"
            spans = self.spansU + 1

        param_ctrls = param_from_length(u_curve_corr, spans, curve_type, "uv")

        self.fol_shape_list = []
        self.fol_parent_list = []
        for x in range(spans):
            fol_shape = cmds.createNode("follicle")
            fol_parent = cmds.listRelatives(fol_shape, p=True)[0]
            cmds.setAttr(fol_shape + ".visibility", 1)

            #print(fol_shape)
            #print(fol_parent)

            cmds.setAttr(f"{fol_shape}.simulationMethod",0)
            
            cmds.connectAttr(f"{surface}.worldMatrix[0]",f"{fol_shape}.inputWorldMatrix")
            cmds.connectAttr(f"{surface}.local", f"{fol_shape}.inputSurface")

            cmds.connectAttr(f"{fol_shape}.outRotate",f"{fol_parent}.rotate")
            cmds.connectAttr(f"{fol_shape}.outTranslate",f"{fol_parent}.translate")

            cmds.setAttr(f"{fol_shape}.parameterV",0.5)
            cmds.setAttr(f"{fol_shape}.parameterU",param_ctrls[x])

            cmds.select(fol_parent)
            cmds.joint(n=f"jnt_fol_{fol_parent}")
            #cmds.select(cl=1)

            self.fol_shape_list.append(fol_shape)
            self.fol_parent_list.append(fol_parent)
