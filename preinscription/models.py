from datetime import date ,datetime

from fastapi import UploadFile
from pydantic import BaseModel
from typing import Optional


class student(BaseModel):
    first_name : str
    last_name : str
    cin:str
    level : int
    baccalaureate : Optional[bool]
    code : Optional[str]
    adresse : Optional[str]
    phone: Optional[str]
    brith_date: Optional[datetime]
    sexe : Optional[str]
    annee : Optional[str]
    departement : Optional[str]
    classe : Optional[str]

class student_family(BaseModel):
    father_name : Optional[str]
    mother_name: Optional[str]
    mother_phone: Optional[str]
    father_phone: Optional[str]
    father_job: Optional[str]
    mother_job :Optional[str]

class ValidationBody(BaseModel):
    validated: bool

class typepayment(BaseModel):
    type: str 
class Files(BaseModel):
    baccalaureate : Optional[UploadFile] 
    cin : Optional[UploadFile] 
    transcripts : Optional[UploadFile] 


class PreRegistration(BaseModel):
    personalInfo: student
    student_family: student_family
    
class validation(BaseModel):
    first_nameValidation :Optional[bool] 
    first_nameCause :Optional[str]
    last_nameValidation :Optional[bool] 
    last_nameCause :Optional[str]
    cinValidation :Optional[bool] 
    cinCause :Optional[str]
    levelValidation :Optional[bool] 
    levelCause :Optional[str]
    codeValidation :Optional[bool] 
    codeCause :Optional[str]
    adresseValidation :Optional[bool] 
    adresseCause :Optional[str]
    phoneValidation :Optional[bool] 
    phoneCause :Optional[str]
    brith_dateValidation :Optional[bool] 
    brith_dateCause :Optional[str]
    sexeValidation :Optional[bool] 
    sexeCause :Optional[str]
    father_nameValidation :Optional[bool] 
    father_nameCause :Optional[str]
    mother_nameValidation :Optional[bool] 
    mother_nameCause :Optional[str]
    mother_phoneValidation :Optional[bool] 
    mother_phoneCause :Optional[str]
    father_phoneValidation :Optional[bool] 
    father_phoneCause :Optional[str]
    father_jobValidation :Optional[bool] 
    father_jobCause :Optional[str]
    mother_jobValidation :Optional[bool] 
    mother_jobCause :Optional[str]
    baccalaureateValidation :Optional[bool] 
    baccalaureateCause :Optional[str]
    cinimgValidation :Optional[bool] 
    cinimgCause :Optional[str]
    transcriptsValidation :Optional[bool] 
    transcriptsCause :Optional[str]
    departementValidation : Optional[bool] 
    departementCause :Optional[str]
    classeValidation : Optional[bool] 
    classeCause :Optional[str]
