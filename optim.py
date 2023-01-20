from fastapi import APIRouter
import pandas as pd
import os
import datetime
import research.research as research
router = APIRouter()



@router.post("/api/optim")
async def composition_habitation(type_habitation: str, surface: int, nb_habitants: int,index:int):
    return research.get_index_by_id(f"{type_habitation}{surface}-{nb_habitants}-{index}")
