# projet_spie

## Installation

`pip install -r requirements.txt` 

## Utilisation

Lancer le serveur FastAPI :  
`uvicorn main:app`  

Ouvrir ce lien dans votre navigateur :  
[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

### Prédiction
La prédiction fontionne pour :
- Les appartements de 15m² et 1 habitant
- Les maisons de 120m² et 5 habitants

Dans le champ type_habitation, entrer M pour maison et A pour appartement

### Optimisation
Pour l'optimisation, l'index correspond au numéro de maison 

Exemple : La maison M-120-5-2 a pour index 2
