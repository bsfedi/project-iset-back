from datetime import date ,datetime

from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class demande_presence(BaseModel):
    user_id : str
    first_name : str 
    last_name : str
    cin:str 
    nb_page : int
    nb_arab : int
    nb_fr : int
    enseignants : list 
    code : Optional[str] 
    departement : Optional[str]
    datedepot : Optional[datetime] =datetime.now()
    classe : Optional[str]
    status : Optional[str] = "pending"


class demande_verification(BaseModel):
    user_id : str
    first_name : str 
    last_name : str
    cin:str 
    type : str
    matiere : str
    datedepot : Optional[datetime]  =datetime.now()
    note : int 
    code : Optional[str] 
    departement : Optional[str] 
    classe : Optional[str]
    commantaire : Optional[str]
    status : Optional[str]   = "pending"


class update_demande(BaseModel):
    role : str
    status : str