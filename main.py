from fastapi import FastAPI

import predict
import optim

app = FastAPI(
    title = "Projet Use Case SPIE"
)

app.include_router(predict.router)
app.include_router(optim.router)

@app.get("/")
async def home():
    return "Bienvenue sur notre prédicteur de consommation"