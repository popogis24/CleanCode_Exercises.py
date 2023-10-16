import arcpy

class RasterMaskExtractor:
    def __init__(self, raster_path, shapefile_path, output_folder):
        self.raster_path = raster_path
        self.shapefile_path = shapefile_path
        self.output_folder = output_folder

    def extract_by_mask(self):
        with arcpy.da.SearchCursor(self.shapefile_path, ["nm_utp"]) as cursor:
            for row in cursor:
                shapefile1 = arcpy.MakeFeatureLayer_management(self.shapefile_path, "layer", "nm_utp = '" + row[0] + "'")
                output_raster_path = fr"{self.output_folder}\{row[0]}.tif"
                arcpy.gp.ExtractByMask_sa(self.raster_path, shapefile1, output_raster_path)


if __name__ == "__main__":
    try:
        raster = fr"R:\09-Banco_De_Dados_Geografico\01-Clientes\PMF\RIOS_URBANOS\Raster\MDE_SIGSC\mde_floripa2.tif"
        shapefile = fr"R:\09-Banco_De_Dados_Geografico\01-Clientes\PMF\RIOS_URBANOS\Banco_Dados.gdb\Dados_Caruso\MICROBACIAS_ESTUDO_quantitativos"
        output_folder = fr"R:\09-Banco_De_Dados_Geografico\01-Clientes\PMF\RIOS_URBANOS\Raster\Div_Bacias"

        extractor = RasterMaskExtractor(raster, shapefile, output_folder)
        extractor.extract_by_mask()

    except arcpy.ExecuteError:
        arcpy.AddError(arcpy.GetMessages())
    except Exception as e:
        arcpy.AddError(str(e))
