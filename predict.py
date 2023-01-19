from fastapi import APIRouter
import pandas as pd
import os
import datetime
from prophet import Prophet
from prophet.serialize import model_to_json, model_from_json
import datetime as dt
router = APIRouter()

@router.post("/api/predict")
async def prediction_consommation(année: int,mois:int,jour:int, heure: str, type_habitation: str, surface: int, nb_habitants: int):
    with open(f'Model.data {type_habitation}{surface}-{nb_habitants}.json', 'r') as f:
        model = model_from_json(f.read())  # Load model
    dateTest=dt.date(année,mois,jour)
    dateWithHour=dt.datetime.combine(dateTest, dt.time(15,30))+dt.timedelta(days=1)
    Datepredict=[]
    Datepredict.append(dateWithHour)
    testDates = pd.DataFrame(Datepredict, columns=['ds'])
    #formatted_date = datetime.datetime.strptime(date, '%m/%d/%Y')
    #jour_suivant = (formatted_date + datetime.timedelta(days=1)).date()
    forecast = model.predict(testDates)
    return f"La consommation prédite le {dateWithHour} pour un(e) {type_habitation} de {surface}m² habité(e) par {nb_habitants} habitants est de {forecast.yhat[0]}kWh."
