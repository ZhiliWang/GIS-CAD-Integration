import arcpy
import os

cad_folder = os.path.join('data', 'cad_files')
gis_gdb = os.path.join('data', 'gis_files', 'gis_data.gdb')

def import_cad_to_gis(cad_file, gis_gdb):
    arcpy.env.workspace = gis_gdb
    try:
        arcpy.ImportCADConversion_conversion(cad_file, "DWG_R2010", gis_gdb, "", "GENERIC_DATA")
        feature_classes = arcpy.ListFeatureClasses()
        for fc in feature_classes:
            arcpy.AddField_management(fc, "CADFileName", "TEXT")
            arcpy.CalculateField_management(fc, "CADFileName", f"'{os.path.basename(cad_file)}'")
        print(f"Imported and processed: {cad_file}")
    except Exception as e:
        print(f"Failed to import {cad_file}: {e}")

for cad_file in os.listdir(cad_folder):
    if cad_file.endswith(".dwg"):
        import_cad_to_gis(os.path.join(cad_folder, cad_file), gis_gdb)