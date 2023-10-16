import arcpy
import os

class FeatureClipper:
    def __init__(self, workspace, clip_area, output_dataset):
        self.workspace = workspace
        self.clip_area = clip_area
        self.output_dataset = output_dataset
        self.list_error = []

        arcpy.env.addOutputsToMap = False
        arcpy.env.overwriteOutput = True
        arcpy.env.workspace = workspace

    def clip_features(self):
        fc_list = arcpy.ListFeatureClasses()
        count = len(fc_list)
        for i, fc in enumerate(fc_list, start=1):
            print(f"Andamento: {i} de {count}")
            try:
                if self._perform_pairwise_clip(fc):
                    print(f"Clip realizado com sucesso para o feature class: {fc}")
                else:
                    raise Exception("Clip falhou")
            except Exception as e:
                print(f"Erro no clip do feature class: {fc}. Tentando métodos alternativos...")
                if self._perform_select_by_location(fc) or self._perform_intersect(fc):
                    print(f"Clip realizado com sucesso para o feature class: {fc}")
                else:
                    print("Não foi possível realizar o clip.")
                    self.list_error.append(fc)
                    continue

        if self.list_error:
            print('Essas features deram erro: ')
            for error in self.list_error:
                print(error)

    def _perform_pairwise_clip(self, feature_class):
        try:
            clip_layer = arcpy.SelectLayerByAttribute_management(self.clip_area, "NEW_SELECTION", "fuso = 'fuso 23'")
            arcpy.analysis.PairwiseClip(feature_class, clip_layer, os.path.join(self.output_dataset, f"{feature_class}_F23"))
            return True
        except Exception as e:
            return False

    def _perform_select_by_location(self, feature_class):
        try:
            arcpy.MakeFeatureLayer_management(feature_class, "layer")
            arcpy.SelectLayerByLocation_management("layer", "INTERSECT", self.clip_area)
            arcpy.CopyFeatures_management("layer", "in_memory/layer")
            arcpy.Clip_analysis("in_memory/layer", self.clip_area, os.path.join(self.output_dataset, f"{feature_class}_clip"))
            return True
        except Exception as e:
            return False

    def _perform_intersect(self, feature_class):
        try:
            arcpy.Intersect_analysis([feature_class, self.clip_area], os.path.join(self.output_dataset, f"{feature_class}_clip"))
            return True
        except Exception as e:
            return False


if __name__ == "__main__":
    workspace = fr'R:\09-Banco_De_Dados_Geografico\01-Clientes\CHESF\PreLeilao_Lote2_3\GDB_Dados_Referenciais\PL_LOTE_02_03_Geodesic.gdb\Dados_Referenciais'
    clip_area = fr'C:\Users\anderson.souza\Downloads\DIV_FUSOS.shp'
    dataset_final = fr'R:\09-Banco_De_Dados_Geografico\01-Clientes\CHESF\PreLeilao_Lote2_3\GDB_Dados_Referenciais\PL_LOTE_02_03_Clipped.gdb\Dados_Referenciais_F23'

    clipper = FeatureClipper(workspace, clip_area, dataset_final)
    clipper.clip_features()
