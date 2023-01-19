from fastapi import APIRouter
import pandas as pd
import os
import datetime

router = APIRouter()
"""
class ElectroMenager:
    lave_linge: int
    lave_vaisselle: int
    seche_linge: int
    chauffe_eau: int
    refrigerateur: int
    congelateur: int
    four: int
    plaques_cuisson: int
    

@router.post("/api/optim")
async def composition_habitation(liste_appareils: ElectroMenager):
    compo_habitation = {
        'Lave-linge' : [ElectroMenager.lave_linge],
        'Lave-vaisselle': [ElectroMenager.lave_vaisselle],
        'Sèche-linge': [ElectroMenager.seche_linge],
        'Chauffe-eau': [ElectroMenager.chauffe_eau],
        'Réfrigérateur': [ElectroMenager.refrigerateur],
        'Congélateur': [ElectroMenager.congelateur],
        'Plaques de cuisson': [ElectroMenager.plaques_cuisson],
    }

    df_appareils_menagers = pd.DataFrame(compo_habitation, index =[0])

    return df_appareils_menagers
"""
# @router.post("/api/optim")
# async def utilisation_appareils()

