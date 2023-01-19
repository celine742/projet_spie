from fastapi import APIRouter
import pandas as pd
import os
import datetime

router = APIRouter()

@router.post("/api/predict")
async def prediction_consommation(date: str, heure: str, type_habitation: str, surface: int, nb_habitants: int):
    menage = {
        'Date': [date],
        'Heure': [heure],
        'Maison ou appartement': [type_habitation],
        'Surface de l\'habitation': [surface],
        'Nombre d\'habitants': [nb_habitants]
    }
    df = pd.DataFrame(menage, index =[0])
    formatted_date = datetime.datetime.strptime(date, '%m/%d/%Y')
    jour_suivant = (formatted_date + datetime.timedelta(days=1)).date()
    conso = 0
    return f"La consommation prédite le {jour_suivant} à {heure} pour un(e) {type_habitation} de {surface}m² habité(e) par {nb_habitants} habitants est de {conso}kWh."
