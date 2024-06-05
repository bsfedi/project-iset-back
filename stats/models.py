from datetime import date ,datetime

from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class modules(BaseModel):
    classe : list
    module : list
    enseignant : list
    


class absence(BaseModel):
    student_id : str
    module_id :str
    status : str

class annonce(BaseModel):
    departement :str
    titre : str
    contenu :str



class update_demande(BaseModel):
    role : str
    validated:bool