bl_info = {
    "name": "CleanMeshes",
    "author": "Jeanclaude Stephane",
    "version": (1, 1),
    "blender": (2, 90, 0),
    "location": "View3D > Properties Panel",
    "description": "Help to clean imported meshes from others software or from scan",
    "doc_url": "https://gumroad.com/products/KUMjG",
    'warning': '',
    "category": "Mesh"}

import bpy
from bpy.types import Operator, Panel
dv = bpy.ops.mesh

def edselect():
    bpy.ops.object.mode_set(mode='EDIT') #passe en mode edit
    dv.select_all(action='DESELECT') #deselectionne tous les vertices
def reOb():
    dv.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT') # passe en mode objet

def deleteAllModifiers(obj):
    obj.modifiers.clear()

def deleteAllConstraints(obj):
    obj.constraints.clear()
    
def deleteIsolateVertices(obj):
    edselect()
    dv.select_loose(extend=False)#selectionne les vertices isolés
    dv.delete_loose(use_verts=True, use_edges=True, use_faces=False) #supprime les vertices isolés
    reOb()

def deleteIsolateEdges(obj):
    edselect()
    dv.select_face_by_sides()
    dv.select_all(action='INVERT')
    dv.delete(type='VERT')
    reOb()
    
def removeDoublesVertices(obj):
    edselect()
    dv.remove_doubles() #Supprime les vertices en double
    reOb()

def removeSplitNormals(obj):
    edselect()
    dv.customdata_custom_splitnormals_clear()
    reOb()

def recalculateNormalsOutside(obj):
    edselect()
    dv.normals_make_consistent(inside=False)
    reOb()

def convertTrisToQuads(obj):
    edselect()
    dv.tris_convert_to_quads()
    reOb()
    
def centerPivots(obj):
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    
def centerObjectsOnWorld(obj):
    bpy.ops.view3d.snap_cursor_to_center()
    bpy.ops.view3d.snap_selected_to_cursor(use_offset=False) #deplacer l'objet au centre
    bpy.ops.object.transform_apply(location=Trus,rotation=False, scale=False) #apply transformation
    
def clearAndKeepTransformation(obj):
    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')


# --------------------------------------------------------------------------------    
class AutoClean(Operator):
    bl_idname = "auto.clean"
    bl_label = "Clean Mesh"
    bl_description = "Clean auto meshes"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        #Recupere les objets selectionnés
        C = bpy.context.selected_objects
        for ob in C:
            deleteAllModifiers(ob) #supprime tous les modifiers
            deleteIsolateVertices(ob) #Supprime les vertices isolés
            deleteIsolateEdges(ob)
            removeDoublesVertices(ob) #Supprime les vertices en double
            removeSplitNormals(ob) #Supprime les splitNormals
            recalculateNormalsOutside(ob) #recalcule les normals outside
            convertTrisToQuads(ob) #Convert Tris to Quads
        
        #selectionne tous les vertices
        #supprime les vertices en doubles
        #Differentes operation de nettoyage, normals, tris to quad...
        #passe en mode objet
        #met et applique un decimate
        #met un shade smooth
        #met un edgesplit a 30degree
        
        #Deselectionne tous les objets
        return {'FINISHED'}

# --------------------------------------------------------------------------------        
class DeleteModifiers(Operator):
    bl_idname = "del.modifiers"
    bl_label = "delete modifiers"
    bl_description = "delete all modifiers on all selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        C = bpy.context.selected_objects
        for ob in C:
            deleteAllModifiers(ob)
        return {'FINISHED'}
    
# --------------------------------------------------------------------------------        
class DeleteConstraints(Operator):
    bl_idname = "del.constraints"
    bl_label = "delete constraints"
    bl_description = "delete all constraints on all selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        C = bpy.context.selected_objects
        for ob in C:
            deleteAllConstraints(ob)
        return {'FINISHED'}
    
# --------------------------------------------------------------------------------        
class RemoveDouble(Operator):
    bl_idname = "rem.double"
    bl_label = "Remove Double"
    bl_description = "Remove doubles vertices on all selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        C = bpy.context.selected_objects
        for ob in C:
            removeDoublesVertices(ob)
        return {'FINISHED'}

# --------------------------------------------------------------------------------        
class RemoveSplitNormals(Operator):
    bl_idname = "rem.splitnormals"
    bl_label = "Remove split normals"
    bl_description = "Remove split normals on all selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        C = bpy.context.selected_objects
        for ob in C:
            removeSplitNormals(ob)
        return {'FINISHED'} 
# --------------------------------------------------------------------------------        
class RecalculateNormals(Operator):
    bl_idname = "rec.normals"
    bl_label = "Recalculate normals"
    bl_description = "Recalculate normals outside on all selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        C = bpy.context.selected_objects
        for ob in C:
            recalculateNormalsOutside(ob)
        return {'FINISHED'}
    
# --------------------------------------------------------------------------------        
class ConvertTrisToQuads(Operator):
    bl_idname = "con.ttq"
    bl_label = "Convert Tris to quads"
    bl_description = "Convert Tris to quads on all selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        C = bpy.context.selected_objects
        for ob in C:
            convertTrisToQuads(ob)
        return {'FINISHED'}
    
# --------------------------------------------------------------------------------        
class DelIsolateVertices(Operator):
    bl_idname = "del.vert"
    bl_label = "Delete isolate vertices"
    bl_description = "Delete isolate vertices on all selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        C = bpy.context.selected_objects
        for ob in C:
            deleteIsolateVertices(ob)
        return {'FINISHED'}
    
# --------------------------------------------------------------------------------        
class DelIsolateEdges(Operator):
    bl_idname = "del.edges"
    bl_label = "Delete isolate edges"
    bl_description = "Delete isolate edges on all selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        C = bpy.context.selected_objects
        for ob in C:
            deleteIsolateEdges(ob)
        return {'FINISHED'}

# --------------------------------------------------------------------------------        
class CenterPivots(Operator):
    bl_idname = "cen.piv"
    bl_label = "Center pivots"
    bl_description = "Center Pivot on all selected Objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        C = bpy.context.selected_objects
        for ob in C:
            centerPivots(ob)
        return {'FINISHED'}
# --------------------------------------------------------------------------------        
class CenterObjectsOnWorld(Operator):
    bl_idname = "cen.ob"
    bl_label = "Center object"
    bl_description = "Center all selected Object on 3d World"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        C = bpy.context.selected_objects
        for ob in C:
            centerObjectsOnWorld(ob)
        return {'FINISHED'}    

# --------------------------------------------------------------------------------        
class ClearAndKeepTransformation(Operator):
    bl_idname = "clr.trans"
    bl_label = "Clear and keep transformation"
    bl_description = "Clear and keep transformation on all selected Object"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        C = bpy.context.selected_objects
        for ob in C:
            clearAndKeepTransformation(ob)
        return {'FINISHED'} 
        
# --------------------------------------------------------------------------------
# GUI
class CleanMeshes(Panel):
    bl_label = 'Clean Meshes'
    bl_idname = '_PT_testPanel'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Cleaning'
    
    def draw(self, context):
        layout = self.layout
        #rd = scene.render
        
        row = layout.row()
        row.operator("auto.clean", text="AUTO CLEAN", icon="RNDCURVE")
        row = layout.row()
        row.label(text= "Individual Clean Option")
        row = layout.row()
        row.operator("del.vert", text="Delete isolate vertices")
        row = layout.row()
        row.operator("del.edges", text="Delete isolate edges")
        row = layout.row()
        row.operator("rem.double", text="Remove Double")
        row = layout.row()
        row.operator("con.ttq", text="Tris to Quads")
        row = layout.row()
        row.operator("rem.splitnormals", text="Remove Split Normals")
        row = layout.row()
        row.operator("rec.normals", text="Recalculate Normals")
        row = layout.row()
        row.operator("del.modifiers", text="Delete Modifiers")
        row = layout.row()
        row.operator("del.constraints", text="Delete Constraints")
        row = layout.row()
        row.operator("cen.piv", text="Center Pivots")
        row = layout.row()
        row.operator("cen.ob", text="Recenter Objects")
        row = layout.row()
        row.operator("clr.trans", text="Clear and keep transformation")
        
               
#############################################################################################
classes = (
    CleanMeshes,
    AutoClean,
    DelIsolateVertices,
    DelIsolateEdges,
    DeleteModifiers,
    DeleteConstraints,
    RemoveDouble,
    RemoveSplitNormals,
    RecalculateNormals,
    ConvertTrisToQuads,
    CenterPivots,
    CenterObjectsOnWorld,
    ClearAndKeepTransformation
    ) 

register, unregister = bpy.utils.register_classes_factory(classes)    
       
# Register     
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
# unregister    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
if __name__ == "__main__":
    register()
