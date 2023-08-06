from datetime import timedelta

import pandas as pd


def selecao_periodos(df_datas, total_tags_out, point_perc_min, duracao_min_periodo):

    ### carregando dataset df_day gerado na função filtrar_dados_dataset

    df_sp_filter = df_datas[(df_datas["TAGs Out"] <= total_tags_out) & (df_datas["Point In"] > point_perc_min)]

    ### formatando períodos conforme parâmetros definidos

    df_sp_filter["Período"] = None

    if df_sp_filter.shape[0] > 0:
        for row in range(0, df_sp_filter.shape[0]):
            if row == 0:
                periodo = 1
                df_sp_filter.iat[row, 4] = periodo
                ant_data = df_sp_filter.iat[row, 0]
            else:
                ant_data = df_sp_filter.iat[row - 1, 0]
                if (df_sp_filter.iat[row, 0] - timedelta(days=1)) == ant_data:
                    df_sp_filter.iat[row, 4] = periodo
                else:
                    periodo = periodo + 1
                    df_sp_filter.iat[row, 4] = periodo

        df_sp_filter["Data_Inicio"] = df_sp_filter["Data"].groupby(df_sp_filter["Período"]).transform("min")
        df_sp_filter["Data_Fim"] = df_sp_filter["Data"].groupby(df_sp_filter["Período"]).transform("max")
        df_sp_filter["Duração"] = (
            df_sp_filter["Data_Fim"] - df_sp_filter["Data_Inicio"] + timedelta(days=1)
        ) / pd.Timedelta(hours=1)
        df_sp_filter["TAGs_Out"] = df_sp_filter["TAGs Out"].groupby(df_sp_filter["Período"]).transform("max")
        df_sp_filter["Total_TAG"] = df_sp_filter["Total TAGs"].groupby(df_sp_filter["Período"]).transform("max")
        df_sp_filter["Point_In"] = df_sp_filter["Point In"].groupby(df_sp_filter["Período"]).transform("mean")
        df_sp_filter = df_sp_filter.drop(["Data", "Point In", "TAGs Out", "Total TAGs"], axis=1)
        df_sp_filter = df_sp_filter.drop_duplicates()
        df_sp_filter = df_sp_filter[df_sp_filter["Duração"] >= duracao_min_periodo]
        df_sp_filter = df_sp_filter.reset_index(drop=True)
        df_sp_filter["Point_In"] = df_sp_filter["Point_In"] * 100
        df_sp_filter["Point_In"] = df_sp_filter["Point_In"].map("{0:.2f}%".format)
        df_sp_filter["Data_Inicio"] = df_sp_filter["Data_Inicio"].dt.strftime("%d/%m/%Y %H:%M:%S")
        df_sp_filter["Data_Fim"] = df_sp_filter["Data_Fim"] + timedelta(days=1)
        df_sp_filter["Data_Fim"] = df_sp_filter["Data_Fim"].dt.strftime("%d/%m/%Y %H:%M:%S")
        return df_sp_filter
    else:
        return "Não há períodos para os parâmetros definidos!"
