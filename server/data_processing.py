from datetime import datetime

import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta


def process_avg_perception(row):
    return 1 if float(row) >= 3 else 0


def process_avg_cost_perception(row):
    return 1 if float(row) < 3 else 0


def process_churn_date(row):
    return 1 if row else 0


def process_contract_lenght(start, end, value):
    date_format = '%d.%m.%Y'
    i = value
    if bool(i) and not np.isnan(i):
        j = i
    else:
        try:
            start_date = datetime.strptime(start, date_format).date()
            end_date = datetime.strptime(end, date_format).date()

            delta = relativedelta(end_date, start_date)

            j = delta.months + 12 * delta.years
        except:
            j = 24
    return j


def process_dataset(dataset):
    rows = []
    ids = dataset['ACCOUNTID'].unique()
    for i in ids:
        multiplay = []
        res = dataset[dataset['ACCOUNTID'] == i]
        for z in res['MULTIPLAY'].values:
            try:
                multiplay.extend(z.split(','))
            except:
                continue
        multiplay = list(set(multiplay))
        new_row = pd.DataFrame(
            {
                'ACCOUNTID': i,
                'MULTIPLAY': [multiplay],
                'CONTRACT_LENGTH': [process_contract_lenght(
                    res['CONTRACT_START_DATE'].values[0],
                    res['CONTRACT_EXPIRATION_DATE'].values[0],
                    res['CONTRACT_LENGTH'].values[0],
                )],
                '3G-V': [1 if '3G-V' in multiplay else 0],
                '3G-D ': [1 if '3G-D' in multiplay else 0],
                'INTERNET': [1 if 'INTERNET' in multiplay else 0],
                'IPTV-U': [1 if 'IPTV-U' in multiplay else 0],
                'IPTV-P': [1 if 'IPTV-P' in multiplay else 0],
                'WL-V': [1 if 'WL-V' in multiplay else 0],
                'CONCURENTI': [max(res['CONCURENTI'].values)],
                'INCIDENTE': [max(res['INCIDENTE'].values)],
                'STATUT_CONTRACT': [max(res['STATUT_CONTRACT'].values)], #
                'SOLICITARI_REZILIERE': [sum(res['SOLICITARI_REZILIERE'].values)],
                'PRET_ABON': [max(res['PRET_ABON'].values)], #
                'QUALITY_PERCEPTION': [sum(res['INCIDENTE'].values) / len(res)],
                'COST_PERCEPTION': [max(res['COST_PERCEPTION'].values)],
                'IPTV_STB_QUANTITY': [sum(res['IPTV_STB_QUANTITY'].values) / len(res)],
                'QNT_APELARI': [max(res['IPTV_STB_QUANTITY'].values)],
                'QNT_PORT_REZ': [sum(res['QNT_PORT_REZ'].values)],
                'AVG_PERCEPTION': [sum(res['AVG_PERCEPTION'].values) / len(res)],
                'QNT_INCEDENT': [max(res['QNT_INCEDENT'].values)],
                'LUNI_DATOR': [sum(res['LUNI_DATOR'].values) / len(res)],
                'SUMA_ACHITARII': [sum(res['SUMA_ACHITARII'].values) / len(res)],
                'CNT_SERVICII': [sum(res['CNT_SERVICII'].values) / len(res)],
                'IS_CHURN': [max(res['IS_CHURN'].values)],
                'CHURN_DATE': [max(res['CHURN_DATE'].values)],
            }
        )
        rows.append(new_row)
    df = pd.concat(rows)
    return df
