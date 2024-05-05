from datetime import date ,datetime

from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class stage(BaseModel):
    user_id : str
    entreprise : Optional[str]
    departement : Optional[str] 
    date_debut :  Optional[datetime] = None
    date_fin : Optional[datetime] =None
    responsable : str
    type : str
    adresse : Optional[str]
    fax : Optional[str]  
    tel : Optional[str]
    email_entreprise : Optional[str]
    status :Optional[str] = True
    classe : str



class stage_pfe(BaseModel):
    user_id : str
    entreprise : Optional[str]
    departement : Optional[str] 
    date_debut :  Optional[datetime] = None
    date_fin : Optional[datetime] =None
    responsable : str
    type : str
    adresse : Optional[str]
    fax : Optional[str]  
    tel : Optional[str]
    email_entreprise : Optional[str]
    project : Optional[str]
    encadrent_externe : Optional[str]
    email_encadrent_externe  : Optional[str]
    tel_encadrent_externe  : Optional[str]
    encadrant_interne : Optional[str]
    fonctionalie :  Optional[str]
    classe : Optional[str]
    

class staus_satge(BaseModel):
    status : bool
    commantaire : Optional[str] = ""

class stage_note(BaseModel):
    note : str