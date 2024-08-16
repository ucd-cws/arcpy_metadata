import arcpy_metadata

metadata = arcpy_metadata.MetadataEditor(r"C:\Users\nick.santos\AppData\Local\Temp\bunnyhop_workspacesjvdkzqv\bunnyhop_workspace.gdb\cities_counties_merged",
                                         metadata_export_option="REMOVE_ALL_SENSITIVE_INFO")