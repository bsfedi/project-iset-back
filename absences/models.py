from datetime import date ,datetime

from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class modules(BaseModel):
    classe : str
    module : str
    enseignant : str
    


class absence(BaseModel):
    student_id : str
    module_id :str
    status : str




class update_demande(BaseModel):
    role : str
    validated:bool