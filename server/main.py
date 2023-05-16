import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import pandas as pd
from sklearn.preprocessing import StandardScaler

from model import prediction_rate, classifier
sc = StandardScaler()

app = FastAPI(title="Async FastAPI")

dataset = pd.read_csv('./data/data.csv', delimiter=';', skiprows=0, low_memory=False)
df =dataset
dict_list = dataset.to_dict(orient='records')
dataset = dataset.drop(columns=['MULTIPLAY', 'IS_CHURN', 'CHURN_DATE'])

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:4000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/general/dashboard")
async def index():
    predictions = []
    for i in dict_list:
        row = dataset[dataset['ACCOUNTID'] == i['ACCOUNTID']]
        row = row.drop(columns='ACCOUNTID')
        predictions.append(
            {
                'user_id': str(i['ACCOUNTID']),
                'cost': int(i['PRET_ABON']),
                'churn': int(classifier.predict(sc.fit_transform(row))[0]),
            }
        )
    stats = {
            'Apeluri': dataset['QNT_APELARI'].sum(),
            'Probleme': dataset['QNT_INCEDENT'].sum(),
        }
    return {
        'totalCustomers': len(dataset),
        'left': df['IS_CHURN'].value_counts().to_dict()[1],
        'remain': df['IS_CHURN'].value_counts().to_dict()[0],
        'predictionRate': prediction_rate,
        'stats': stats,
        'predictions': predictions
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
