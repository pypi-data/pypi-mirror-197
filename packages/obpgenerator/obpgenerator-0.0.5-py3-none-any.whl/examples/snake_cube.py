import obpgenerator

file_path = r"layer_nine_cubes.svg"

newLayer = obpgenerator.Layer()
newLayer.import_svg_layer(file_path)
newLayer.set_shapes(1)
newLayer.set_melt_strategies("line_right_to_left")
newLayer.set_nmb_of_scans(2)
newLayer.sorting_strategy = "ramp_manufacturing_settings"


#file_path2 = r"C:\Users\antwi87\Downloads\drawing-2.obp"

#newLayer.export_obp(file_path2)
