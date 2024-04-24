from datetime import date, datetime
from fastapi import UploadFile
from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    email: str =""
    password: str =""
    role : str =""
    preinscirption : str  =""

class User_login(BaseModel):
    email: EmailStr =""
    password: str =""
 

class New_user(BaseModel):
    first_name:str
    last_name :str
    code : Optional[str]
    email :str
    phone : str
    identifiant :str
    departement : str
    grade : str
    role : str
    password : str
    service : Optional[str] =""
    privilege : Optional[str] = ""

class student(BaseModel):
    first_name : str =""
    last_name : str =""
    cin:str =""
    image_cin : UploadFile
    level : int =""
    baccalaureate : Optional[bool] =""
    code : Optional[str] =""
    adresse : Optional[str] =""
    phone: Optional[str] =""
    brith_date:Optional[date] =""
    sexe : Optional[str] =""

class student_family(BaseModel):
    father_name : Optional[str] =""
    mother_name: Optional[str] =""
    mother_phone: Optional[str] =""
    father_phone: Optional[str] =""
    father_job: Optional[str] =""

class sanction(BaseModel):
    type : str 
    date : datetime
    motif : str
    user_id :Optional[str] =""


    