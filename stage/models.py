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

