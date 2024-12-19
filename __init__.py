import bpy
from bpy.app.handlers import persistent

# Blender Addon: Export on Save

bl_info = {
	"name": "Export on Save",
	"author": "needleful",
	"version": (1, 0, 0),
	"blender": (2, 93, 0),
	"category": "Import-Export",
}

def export_path_callback(settings):
	print("Export on Save: Exported to " + settings["gltf_filepath"])
	save_path = settings["gltf_filepath"]
	rel_path = bpy.path.relpath(save_path)
	bpy.context.scene["gltf_relpath"] = rel_path

glTF2_pre_export_callback = export_path_callback

class AutoExportPanel(bpy.types.Panel):
	bl_label = "Export on Save"
	bl_idname = "OBJECT_PT_ExportOnSave"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "scene"

	def draw(self, context):
		layout = self.layout
		op = layout.operator("export_scene.gltf", text="GLB Export")
		op.export_apply = True
		op.use_active_collection = True
		op.will_save_settings = True
		if "gltf_relpath" in bpy.context.scene:
			op.filepath = bpy.context.scene["gltf_relpath"]

@persistent
def export_on_save_handler(scene):
	print("Saving...")
	if "gltf_relpath" in bpy.context.scene:
		print("Exporting GLB now..")

		# work out the export settings and save path
		settings = {}
		if "glTF2ExportSettings" in bpy.context.scene:
			settings = bpy.context.scene["glTF2ExportSettings"]
		abs_path = bpy.path.abspath(bpy.context.scene["gltf_relpath"])
		print("Exporting to " + abs_path)

		# get current mode
		current_mode = bpy.context.object.mode

		# perform export
		bpy.ops.export_scene.gltf(filepath=abs_path, **settings)

		# restore current mode (as the export puts us in object mode which is annoying)
		bpy.ops.object.mode_set(mode=current_mode)

def register():
	bpy.app.handlers.save_post.append(export_on_save_handler)
	bpy.utils.register_class(AutoExportPanel)
	print("Export on Save")

def unregister():
	bpy.utils.unregister_class(AutoExportPanel)
	print("Unregistered: Export on Save")

if __name__ == "__main__":
	register()
