from datetime import date ,datetime

from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class demande(BaseModel):
    user_id : str
    type:str 
    month : Optional[str] =""
    status : Optional[str] = "pending"


class conge(BaseModel):
    user_id : str
    type:str
    status : Optional[str] = "pending"
    type_conge : str
    date_debut : Optional[str] =""
    date_fin : Optional[str] =""
    heure_debut : Optional[str] =  ""
    heure_fin :Optional[str] =  ""
