import sys  
import clr
import os
from datetime import datetime, timedelta
import pandas as pd
sys.path.append('C:\\Program Files (x86)\\PIPC\\AF\\PublicAssemblies\\4.0\\')
clr.AddReference('OSIsoft.AFSDK')
from OSIsoft.AF.PI import PIServer, PIPoint
from OSIsoft.AF.Time import AFTimeRange, AFTimeSpan
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


def buscar_dados(unidade, equipamento, server_name, inicio, final, time_span, df_parametros):

    pi_server = PIServer.FindPIServer(server_name)
    timerange = AFTimeRange(inicio, final)    
    span = AFTimeSpan.Parse(time_span) # Intervalo na busca dos resultados

    tag_date_out = []
    tag_name_out = []
    tag_point_in = []
    tag_pl_out = []
    tag_ph_out = []
    df_day = pd.DataFrame.from_dict({
                'Data': [],
                'Point In': [],
                'TAGs Out': [],
                'Total TAGs': []
            })

    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days) + 1):
            yield start_date + timedelta(n)

    inicio_time = datetime.now()
    start_date = datetime.strptime(inicio,'%d/%m/%Y %H:%M:%S')
    end_date = datetime.strptime(final,'%d/%m/%Y %H:%M:%S')
    for date_range in daterange(start_date, end_date):
        point_in_t = 0
        point_count_t = 0
        tag_out = 0
        if date_range == start_date:
            data_i = inicio
            data_f = str((date_range + timedelta(days=1)).strftime("%d/%m/%Y") + ' 00:00:00')
        elif date_range == end_date:
            data_i = str(date_range.strftime("%d/%m/%Y") + ' 00:00:00')
            data_f = end_date
        else:
            data_i = str(date_range.strftime("%d/%m/%Y") + ' 00:00:00')
            data_f = str((date_range + timedelta(days=1)).strftime("%d/%m/%Y") + ' 00:00:00')
        
        if date_range != datetime.strptime(final,'%d/%m/%Y 00:00:00'):

            for row in range(0, df_parametros.shape[0]):
                tagname = df_parametros.iat[row, 0]
                pl = float(df_parametros.iat[row, 2])
                ph = float(df_parametros.iat[row, 3])
                tag = PIPoint.FindPIPoint(pi_server, tagname)  
                timerange = AFTimeRange(data_i, data_f) 
                V = []
                V.append(tag.InterpolatedValues(timerange, span, "" , False,))    
                T= []
                t= []
                for dado in V:
                    for value in dado:
                        if isinstance(value.Value,float):
                            T.append(float(value.Value))
                            t.append(datetime.strptime(str(value.Timestamp),'%d/%m/%Y %H:%M:%S'))
                        else:
                            T.append(0)
                            t.append(datetime.strptime(str(value.Timestamp),'%d/%m/%Y %H:%M:%S'))

                df_tags = pd.DataFrame({tagname:T}, index = t)
                point_count= df_tags.count()
                point_in = df_tags[(df_tags[tagname] >= pl) & (df_tags[tagname] <= ph)].count()
                perc_in = point_in.item() / point_count.item()
                
                if perc_in < 1:
                    tag_out = tag_out + 1
                    tag_date_out.append(str(date_range.strftime("%d/%m/%Y")))
                    tag_name_out.append(tagname)
                    tag_point_in.append(perc_in)
                    tag_pl_out.append(pl)
                    tag_ph_out.append(ph)
                    df_tags_out = pd.DataFrame({'Data':tag_date_out, 'TAGs':tag_name_out, 'Point In':tag_point_in , 'PL':tag_pl_out, 'PH':tag_ph_out})
                point_in_t = point_in_t + point_in.item()
                point_count_t = point_count_t + point_count.item()
                
            perc_in_t = point_in_t / point_count_t
            
            df_day.loc[len(df_day)] = [str(date_range.strftime("%d/%m/%Y")), perc_in_t, tag_out, df_parametros.shape[0]]

    fim_time = datetime.now()

    path = './pyspmp/resultado_busca'

    # Exportando df da para seleção de períodos

    df_day.to_csv(os.path.join(path,r'df_sp_' + equipamento + '_' + unidade + '.csv'),',')

    # Exportando df com as TAGs fora dos parâmetros

    df_tags_out.to_csv(os.path.join(path,r'df_tagsout_' + equipamento + '_' + unidade + '.csv'),',')

    duration = fim_time - inicio_time

    return duration