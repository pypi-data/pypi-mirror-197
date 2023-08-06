import warnings
from datetime import datetime, timedelta

import pandas as pd

warnings.simplefilter(action="ignore", category=FutureWarning)
pd.options.mode.chained_assignment = None  # default='warn'


def filtrar_dados_dataset(df_parametro, df_dataset):

    # formato de data
    df_dataset["Datas"] = pd.to_datetime(df_dataset["Datas"]).dt.strftime("%Y-%m-%d %H:%M:%S")

    # função para criação de range entre a data mínima e máxima do dataset
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)

    # definição de variáveis
    inicio = df_dataset["Datas"].min()
    final = df_dataset["Datas"].max()
    tag_date_out = []
    tag_name_out = []
    tag_point_in = []
    tag_pl_out = []
    tag_ph_out = []
    df_datas = pd.DataFrame.from_dict({"Data": [], "Point In": [], "TAGs Out": [], "Total TAGs": []})
    start_date = datetime.strptime(pd.to_datetime(inicio).strftime("%Y-%m-%d 00:00:00"), "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(pd.to_datetime(final).strftime("%Y-%m-%d 00:00:00"), "%Y-%m-%d %H:%M:%S")

    # estrutura de repetição para cada data_range
    for date_range in daterange(start_date, end_date):
        point_in_t = 0
        point_count_t = 0
        tag_out = 0

        # definição de data início e data fim para filtro aplicado no dataset
        if date_range == start_date:
            data_i = inicio
            data_f = str((date_range + timedelta(days=1)).strftime("%Y-%m-%d") + " 00:00:00")
        elif date_range == end_date:
            data_i = str(date_range.strftime("%Y-%m-%d") + " 00:00:00")
            data_f = final
        else:
            data_i = str(date_range.strftime("%Y-%m-%d") + " 00:00:00")
            data_f = str((date_range + timedelta(days=1)).strftime("%Y-%m-%d") + " 00:00:00")

        if data_i != data_f:
            # filtro no dataset por data início e data fim
            df_tags = df_dataset[(df_dataset["Datas"] >= data_i) & (df_dataset["Datas"] < data_f)]
            if df_tags.shape[0] > 0:
                # estrutura de repetição para cada variável continda nos parâmetros/dataset
                for row in range(0, df_parametro.shape[0]):
                    tagname = df_parametro.iat[row, 0]
                    pl = float(df_parametro.iat[row, 2])
                    ph = float(df_parametro.iat[row, 3])
                    # total de linhas(pontos) no dataset
                    point_count = df_tags[tagname].count()
                    # filtro no dataset por parâmetros mínimo e máximo definidos
                    point_in = df_tags[(df_tags[tagname] >= pl) & (df_tags[tagname] <= ph)][tagname].count()
                    # percentual de pontos dentro dos parâmetros definidos
                    perc_in = point_in.item() / point_count.item()

                    # construção do dataset data a data
                    if perc_in < 1:
                        tag_out = tag_out + 1
                        tag_date_out.append(date_range)
                        tag_name_out.append(tagname)
                        tag_point_in.append(perc_in)
                        tag_pl_out.append(pl)
                        tag_ph_out.append(ph)
                        df_tags_out = pd.DataFrame(
                            {
                                "Data": tag_date_out,
                                "TAGs": tag_name_out,
                                "Point In": tag_point_in,
                                "PL": tag_pl_out,
                                "PH": tag_ph_out,
                            }
                        )
                    point_in_t = point_in_t + point_in.item()
                    point_count_t = point_count_t + point_count.item()

                perc_in_t = point_in_t / point_count_t

                df_datas.loc[len(df_datas)] = [date_range, perc_in_t, tag_out, df_parametro.shape[0]]
    return df_datas, df_tags_out
