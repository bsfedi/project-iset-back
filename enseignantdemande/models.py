from datetime import date ,datetime

from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class demande(BaseModel):
    user_id : str
    type:str 
    month : Optional[str] =""
    status : Optional[str] = "pending"