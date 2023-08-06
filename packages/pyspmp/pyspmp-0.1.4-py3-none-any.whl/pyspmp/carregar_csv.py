import os
import pandas as pd


def carregar_df(arquivo, dir):

    # carrega arquivo csv
    diretorio = os.path.dirname(__file__)
    diretorio = os.path.join(diretorio, dir)
    file = arquivo + ".csv"
    df = pd.read_csv(os.path.join(diretorio, file), ",")
    pd.set_option('display.max_rows', None)

    return df

def carregar_df_pi(arquivo, dir):

    # carrega arquivo csv
    diretorio = os.path.dirname(__file__)
    diretorio = os.path.join(diretorio, dir)
    file = arquivo + ".csv"
    df = pd.read_csv(os.path.join(diretorio, file), ",")
    df = df.drop(df.columns[0], axis=1)
    df["Data"] = pd.to_datetime(df["Data"], format='%d/%m/%Y')
    pd.set_option('display.max_rows', None)

    return df
