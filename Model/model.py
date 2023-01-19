import pandas as pd
import os
import numpy as np


def load_Model(my_model,typeHabitation):
    """ load le modèle sérialisé correspondant au type d'habitat

    Args:
        my_model (Xgboost): Model

    Returns:
        _type_: renvoie le model
    """    
    my_model.load_model(f"app/Modèles/{typeHabitation}.json")
    return my_model


def prediction(Date):
    """Prédit la qualité d'un vin

    Args:
        wine (dictionnary): les données sur un vin

    Returns:
        int: renvoie la qualité du vin
    """    
    my_model=XGBRegressor(n_estimators=100,learning_rate=0.05)
    my_model=load_Model(my_model)
    resultat=my_model.predict(wine)
    return resultat


