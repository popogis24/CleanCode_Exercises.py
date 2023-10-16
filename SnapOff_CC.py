import arcpy

class PolygonProcessor:
    def __init__(self, poligonos, output):
        self.poligonos = poligonos
        self.output = output

    def auto_increment_code(self):
        autoincremento = '''
rec=0
def autoIncrement():
    global rec
    pStart = 1 #muda para nao iniciar do num 1
    pInterval = 1 #mude este numero para mudar o intervalo de seq
    if (rec == 0):
        rec = pStart
    else:
        rec = rec + pInterval
    return rec
        '''
        return autoincremento

    def process_polygons(self):
        arcpy.PolygonToLine_management(self.poligonos, "ftl", "IDENTIFY_NEIGHBORS")
        arcpy.MakeFeatureLayer_management("ftl", "featuretoline_lyr")
        arcpy.SelectLayerByAttribute_management("featuretoline_lyr", "NEW_SELECTION", '"LEFT_FID" <> -1 AND "RIGHT_FID" <> -1')
        arcpy.MakeFeatureLayer_management("featuretoline_lyr", "featuretoline_lyr2")
        arcpy.Buffer_analysis("featuretoline_lyr2", "buffer", "10 Millimeters", "FULL", "ROUND", "ALL", "", "GEODESIC")
        arcpy.MakeFeatureLayer_management(self.poligonos, "poligonos_lyr")
        arcpy.Erase_analysis("poligonos_lyr", "buffer", "erase")
        arcpy.MultipartToSinglepart_management("erase", self.output)
        auto_increment_code = self.auto_increment_code()
        arcpy.CalculateField_management(self.output, "div", "autoIncrement()", "PYTHON3", auto_increment_code, "LONG", "")

    def cleanup(self):
        to_delete = ["ftl", "featuretoline_lyr", "featuretoline_lyr2", "buffer", "poligonos_lyr", "erase"]
        for item in to_delete:
            arcpy.Delete_management(item)


if __name__ == "__main__":
    try:
        poligonos = arcpy.GetParameterAsText(0)
        output = arcpy.GetParameterAsText(1)

        polygon_processor = PolygonProcessor(poligonos, output)
        polygon_processor.process_polygons()
        polygon_processor.cleanup()

    except arcpy.ExecuteError:
        arcpy.AddError(arcpy.GetMessages())
    except Exception as e:
        arcpy.AddError(str(e))
