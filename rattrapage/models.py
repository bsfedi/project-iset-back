from datetime import date ,datetime

from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class absence(BaseModel):
    dureé : Optional[str]
    date : Optional[datetime] = None
    date_debut :  Optional[datetime] = None
    date_fin : Optional[datetime] =None
    enseignant : str
    Id_demande : Optional[str]=""
    date_demmande : Optional[datetime]  =datetime.now()

class rattrapage(BaseModel):
    type : str
    date_demmande : Optional[datetime]  =datetime.now()
    Id_demande : Optional[str]=""
    data : list


class status(BaseModel):
    status :str
    motif : Optional[str]= ""
    salle : Optional[str]= ""
    horaire: Optional[str]= ""
