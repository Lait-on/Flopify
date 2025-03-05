from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import db


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://flopify.org", "https://www.flopify.org"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ytburl")
def getURL(country = "", style= "") -> dict:
    if country == "" or style == "":
        url = "_tr5wNHYpNk" 
    else:
        url = db.get_ytb_url(country, style) #on met la requete sql avec db
    return {"url" : url}

@app.get("/trash")
def trashURL(url = ""):
    db.insert_table_trash(url) #on met la requete sql avec db
