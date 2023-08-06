import pandas as pd


def variaveis_out_all(df_tags_out, df_datas, periodo):
    # dataset com o período analisado de acordo com a seleção períodos
    df_tags_out_filter = df_datas[df_datas["Período"] == periodo]
    dataInicio = pd.to_datetime(df_tags_out_filter.iat[0, 1], format="%d/%m/%Y %H:%M:%S")
    dataFim = pd.to_datetime(df_tags_out_filter.iat[0, 2], format="%d/%m/%Y %H:%M:%S")
    df_tags_out["Data"] = pd.to_datetime(df_tags_out["Data"], format="%d/%m/%Y")
    df_tags_out = df_tags_out[(df_tags_out["Data"] >= dataInicio) & (df_tags_out["Data"] < dataFim)]
    df_tags_out_groupby = df_tags_out
    df_tags_out_groupby = df_tags_out_groupby.drop("Data", axis=1)
    df_tags_out_groupby.set_index("TAGs", inplace=True)
    df_tags_out_groupby = df_tags_out_groupby.groupby("TAGs").mean()
    df_tags_out_groupby = df_tags_out_groupby.sort_values(["Point In"], ascending=True)
    df_tags_out_groupby["Point In"] = df_tags_out_groupby["Point In"] * 100
    df_tags_out_groupby["Point In"] = df_tags_out_groupby["Point In"].map("{0:.2f}%".format)

    return df_tags_out_groupby


def variaveis_out_day(df_tags_out, df_datas, periodo):
    # dataset com o período analisado detalhado dia a dia
    df_tags_out_filter = df_datas[df_datas["Período"] == periodo]
    dataInicio = pd.to_datetime(df_tags_out_filter.iat[0, 1], format="%d/%m/%Y %H:%M:%S")
    dataFim = pd.to_datetime(df_tags_out_filter.iat[0, 2], format="%d/%m/%Y %H:%M:%S")
    df_tags_out["Data"] = pd.to_datetime(df_tags_out["Data"], format="%d/%m/%Y")
    df_tags_out = df_tags_out[(df_tags_out["Data"] >= dataInicio) & (df_tags_out["Data"] < dataFim)]
    df_tags_out["Point In"] = df_tags_out["Point In"] * 100
    df_tags_out["Point In"] = df_tags_out["Point In"].map("{0:.2f}%".format)
    df_tags_out["Data"] = df_tags_out["Data"].dt.strftime("%d/%m/%Y")

    return df_tags_out
