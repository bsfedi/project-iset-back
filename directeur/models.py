from datetime import date ,datetime

from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class parcours(BaseModel):
    departement : Optional[str] = ""
    libelle : str
    code : str


class classes(BaseModel):
    departement : Optional[str] = ""
    niveau : str
    parcour : str
    code : str


class modules(BaseModel):
    departement : Optional[str] = ""
    niveau :str
    parcours : str
    code: str
    intitule : str
    type :str


class salles(BaseModel):
 
    code : str
    utilisation :str
    batiment : str
    affectation : str