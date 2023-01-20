from fastapi import APIRouter
import pandas as pd
import os
import datetime
import research.research as research
router = APIRouter()



@router.post("/api/optim")
async def composition_habitation(type_habitation: str, surface: int, nb_habitants: int,index:int):
    dico = research.get_index_by_id(f"{type_habitation}{surface}-{nb_habitants}-{index}")
    equivalence = {
        "LV": "lave-vaisselle",
        "LL": "lave-linge",
        "SL": "sèche-linge",
        "TV": "télévision",
        "FG_1": "réfrigérateur",
        "FG_2": "réfrigérateur",
        "CG": "congélateur",
        "CE_1": "chauffe-eau",
        "CE_2": "chauffe-eau",
        "FO": "four",
        "PL": "plaques de cuisson"
    }
    liste_message=[]
    for key in dico:
        machine = equivalence[key]
        time = dico[key]
        list_heure=[]
        for x in time:
            a = f"{int(x/2)}h{30*(x%2)}"
            list_heure.append(a)
        if list_heure:
            phrase = f"Votre {machine} doit être lancé aux heures suivantes: {list_heure}"
            liste_message.append(phrase)
    return liste_message