import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from data_processing import process_avg_perception
from data_processing import process_avg_cost_perception
from data_processing import process_churn_date
from data_processing import process_dataset

sc = StandardScaler()

drop = [
    'CODE', 'PERIOADA', 'INET_PACK',
    'PERIOADA_ACHITARII', 'IPTV_PACK', 'QNT_SUSP', 'LUNA_APEL', 'CODE_MA',
    'TECHNOLOGY', 'LUNA_INCIDENT', 'LUNA_SUSPENDARI'
]

drop += ['CREANTE_REST', 'NET_PARAMS']

dataset = pd.read_csv('./data/data1.csv', delimiter=';', skiprows=0, low_memory=False)


df = dataset.drop(columns=drop)

# df['CONTRACT_LENGTH'].fillna(36, inplace=True)
df['IPTV_STB_QUANTITY'].fillna(0, inplace=True)
df['QNT_APELARI'].fillna(0, inplace=True)
df['QNT_PORT_REZ'].fillna(0, inplace=True)


# AVG_PERCEPTION
df['AVG_PERCEPTION'] = df['AVG_PERCEPTION'].str.replace(',', '.').astype(float)
df['AVG_PERCEPTION'] = df['AVG_PERCEPTION'].apply(process_avg_perception)
df['AVG_PERCEPTION'].fillna(1, inplace=True)
# AVG_PERCEPTION

# COST_PERCEPTION
df['COST_PERCEPTION'] = df['COST_PERCEPTION'].apply(process_avg_cost_perception)
# COST_PERCEPTION

# QNT_INCEDENT
df['QNT_INCEDENT'].fillna(0, inplace=True)
# QNT_INCEDENT

df['CNT_SERVICII'].fillna(1, inplace=True)

df['PRET_ABON'] = df['PRET_ABON'].str.replace(',', '.').astype(float)

# SUMA_ACHITARII
df['SUMA_ACHITARII'].fillna(0, inplace=True)
df['SUMA_ACHITARII'] = df['SUMA_ACHITARII'].apply(process_churn_date)
# SUMA_ACHITARII


# MULTIPLAY
df['MULTIPLAY'].fillna(0, inplace=True)
# MULTIPLAY


df = process_dataset(df)

y = df['IS_CHURN']
x = df.drop(columns=['IS_CHURN', 'CHURN_DATE', 'MULTIPLAY', 'ACCOUNTID', 'CHURN_DATE'])



x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.4, random_state=0
)

x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

classifier = RandomForestClassifier()

classifier.fit(x_train, y_train)


def test_model_predictions(x, y, model):
    correct = 0
    incorrect = 0
    total = 1000
    count_true = 0
    for i in range(0, total):
        if model.predict(sc.fit_transform([x.iloc[i].values]))[0] == y.iloc[i]:
            correct += 1
        else:
            incorrect += 1
            if y.iloc[i] == 1:
                count_true += 1
    return f'{round(correct / total * 100, 2)}%'


prediction_rate = test_model_predictions(x, y, classifier)
