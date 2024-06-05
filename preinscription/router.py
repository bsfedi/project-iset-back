from email.mime.multipart import MIMEMultipart
from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException
from secuirty import *
from preinscription.models import *
from preinscription.services import *
from datetime import date
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from database import db
import os
from typing import Optional
from fastapi import UploadFile, File
import smtplib
from collections import defaultdict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
gmail_user = "fedislimen98@gmail.com"
pass_code=  "wiuijqbeodgezebw"
from user.services import get_user_by_id

preregiter_router = APIRouter(tags=["Register"])

# Mount a directory containing uploaded files to be served statically
@preregiter_router.put("/personalInfo/{register_id}")
async def register(register_id,student : student):
    student.code = student.cin + '-' + student.annee.split('-')[0]
    if student.level == 1 :
        student.baccalaureate = True
    old_preregister = db["preregistres"].find_one({"_id":ObjectId (register_id)})
    preregistre = db["preregistres"].update_one({"_id":ObjectId(register_id)},{
            "$set": {
                "personalInfo":{
                "email":old_preregister["personalInfo"]["email"],
                "annee":student.annee ,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "cin": student.cin,
                "level": student.level,
                "baccalaureate": student.baccalaureate,
                "code": student.code,
                "adresse": student.adresse,
                "phone": student.phone,
                "brith_date": student.brith_date,
                "sexe" : student.sexe,
                "departement" : student.departement,
                "classe" : student.classe,
                "situation": student.situation,
                "status":student.status
                }

            }
        },)
    # Here you can process the received pre-registration data
    return {"message": "Pre-registration received successfully"}


@preregiter_router.put("/student_family/{register_id}")
async def register(register_id,student_family : student_family):    
    preregistre = db["preregistres"].find_one_and_update({"_id":ObjectId(register_id)},{
            "$set": {
                "depot":student_family.datedepot,
                "family_info" :{
                "father_name": student_family.father_name,
                "mother_name": student_family.mother_name,
                "mother_phone": student_family.mother_phone,
                "father_phone": student_family.father_phone,
                "father_job": student_family.father_job,
                "mother_job": student_family.mother_job,
                }

            }
        },)
    db["preregistres"].find_one_and_update({"_id": ObjectId(register_id)}, {
    "$set": {
        "status":"PENDING",
        "personalInfo.first_nameValidation": True,
        "personalInfo.first_nameCause": "",
        "personalInfo.last_nameValidation": True,
        "personalInfo.last_nameCause": "",
        "personalInfo.cinValidation": True,
        "personalInfo.cinCause": "",
        "personalInfo.levelValidation": True,
        "personalInfo.levelCause": "",
        "personalInfo.baccalaureateValidation": True,
        "personalInfo.codeValidation": True,
        "personalInfo.codeCause": "",
        "personalInfo.adresseValidation": True,
        "personalInfo.adresseCause": "",
        "personalInfo.phoneValidation": True,
        "personalInfo.phoneCause": "",
        "personalInfo.brith_dateValidation": True,
        "personalInfo.brith_dateCause": "",
        "personalInfo.sexeValidation": True,
        "personalInfo.sexeCause": "",
        "personalInfo.departementValidation": True,
        "personalInfo.departementCause": "",
        "personalInfo.classeValidation": True,
        "personalInfo.classeCause": "",
        "personalInfo.situationValidation": True,
        "personalInfo.situationCause": "",
        "family_info.father_nameValidation": True,
        "family_info.father_nameCause": "",
        "family_info.mother_nameValidation": True,
        "family_info.mother_nameCause": "",
        "family_info.mother_phoneValidation": True,
        "family_info.mother_phoneCause": "",
        "family_info.father_phoneValidation": True,
        "family_info.father_phoneCause": "",
        "family_info.father_jobValidation": True,
        "family_info.father_jobCause": "",
        "family_info.mother_jobValidation": True,
        "family_info.mother_jobCause": "",
        "docs.baccalaureateValidation": True,
        "docs.baccalaureateCause": "",
        "docs.cinimgValidation": True,
        "docs.cinimgCause": "",
        "docs.transcriptsValidation": True,
        "docs.transcriptsCause": "",
        "docs.docsuppValidation" : True,
        "docs.docsuppCause": "",
    }
})
    print(preregistre)
    user = get_user_by_id(str(preregistre["user_id"]))

    receiver = user["email"]
    first_name = preregistre["personalInfo"]["first_name"]
    id_user = str(user["_id"])
    # Send password reset email
    subject = "Depot de inscription"
    first_name=first_name[0].upper()  + first_name[1:]
    HTMLPart = f"""
    Dear <b>{first_name} {preregistre["personalInfo"]["last_name"]}</b> , <br> \
   
    Nom : {preregistre["personalInfo"]["first_name"]}<br> \
    Prénom : {preregistre["personalInfo"]["last_name"]}<br> \
    Cin : {preregistre["personalInfo"]["cin"]}<br> \
    Level : {preregistre["personalInfo"]["level"]}<br> \
    Adresse : {preregistre["personalInfo"]["adresse"]}<br> \
    Téléphone : {preregistre["personalInfo"]["phone"]}<br> \
    Année : {preregistre["personalInfo"]["annee"]}<br> \
    Departement : {preregistre["personalInfo"]["departement"]}<br> \
    Classe : {preregistre["personalInfo"]["classe"]}<br> \
    Situation : {preregistre["personalInfo"]["situation"]}<br> \
    Sexe : {preregistre["personalInfo"]["sexe"]}<br> \
    

    Best regards,
"""



    try : 
        sender_address = gmail_user
        sender_pass = pass_code
        mail_content = HTMLPart
        receiver_address = user['email']
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] =   user['email']
        message['Subject'] = subject
        message.attach(MIMEText(mail_content, 'html'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        return True
    except Exception as e :
        return False
    # Here you can process the received pre-registration data
    return {"message": "Pre-registration received successfully"}


@preregiter_router.post("/docs/{register_id}")
async def upload_file(register_id, 
                      baccalaureate: Optional[UploadFile] = File(None), 
                      img_profil : Optional[UploadFile] = File(None),
                      cin: Optional[UploadFile] = File(None),
                      img_docsupp :  Optional[UploadFile] = File(None),
                      transcripts: Optional[UploadFile] = File(None)):
    if baccalaureate:
        with open(os.path.join("uploads", baccalaureate.filename), "wb") as buffer:
            buffer.write(await baccalaureate.read())
    if cin:
        with open(os.path.join("uploads", cin.filename), "wb") as buffer:
            buffer.write(await cin.read())
    if transcripts:
        with open(os.path.join("uploads", transcripts.filename), "wb") as buffer:
            buffer.write(await transcripts.read())
    if img_profil:
        with open(os.path.join("uploads", img_profil.filename), "wb") as buffer:
            buffer.write(await img_profil.read())
    if img_docsupp:
        with open(os.path.join("uploads", img_docsupp.filename), "wb") as buffer:
            buffer.write(await img_docsupp.read())
    

    update_data = {}
    if baccalaureate:
        update_data["baccalaureate"] = baccalaureate.filename
    if cin:
        update_data["cin"] = cin.filename
    if transcripts:
        update_data["transcripts"] = transcripts.filename
    if img_profil:
        update_data["img_profil"] = img_profil.filename
    if img_docsupp:
        update_data["img_docsupp"] = img_docsupp.filename

    preregistre = db["preregistres"].update_one({"_id": ObjectId(register_id)}, {"$set": {"docs": update_data}})
    return {"filename": transcripts.filename if transcripts else None}


@preregiter_router.post("/new_docs_1/{register_id}")
async def upload_file(register_id, 
                      note1: Optional[UploadFile] = File(None)
       
                ):
    if note1:
        with open(os.path.join("uploads", note1.filename), "wb") as buffer:
            buffer.write(await note1.read())

    

    update_data = {}
    if note1:
        update_data["note1"] = note1.filename


    preregistre = db["preregistres"].update_one({"_id": ObjectId(register_id)}, {"$set": {"docs.note1": update_data["note1"],       
        "docs.note1Validation": True,
        "docs.note1Cause": "",}})
    return True

@preregiter_router.post("/new_docs_2/{register_id}")
async def upload_file(register_id, 
                      note1: Optional[UploadFile] = File(None),
         note2: Optional[UploadFile] = File(None)
                ):
    if note1:
        with open(os.path.join("uploads", note1.filename), "wb") as buffer:
            buffer.write(await note1.read())
    if note2:
        with open(os.path.join("uploads", note2.filename), "wb") as buffer:
            buffer.write(await note2.read())
    

    update_data = {}
    if note1:
        update_data["note1"] = note1.filename
    if note2:
        update_data["note2"] = note2.filename

    preregistre = db["preregistres"].update_one({"_id": ObjectId(register_id)}, {"$set": {"docs.note1": update_data["note1"],"docs.note2": update_data["note2"],        
        "docs.note1Validation": True,
        "docs.note1Cause": "",
        "docs.note2Validation": True,
        "docs.note2Cause": ""}})
    return True


@preregiter_router.put("/preregister/{register_id}")
async def validated_register(register_id,validation :validation):
    # Iterate over each attribute in the validation object
    # Check if any validation result is False
    # rh_validation_values = list(validation.values())
    is_false_value_present =  is_false_value_present = any(getattr(validation, attr) is False for attr in validation.__dict__)
  
    # If any validation is False, update status to "NOTVALIDATED" and return False
    if is_false_value_present:
        db["preregistres"].update_one({"_id": ObjectId(register_id)}, {
            "$set": {"status": "NOTVALIDATED"}
        })
    else:
        db["preregistres"].update_one({"_id": ObjectId(register_id)}, {
            "$set": { "status":"WAITINGVALIDATION",              
                     "validation.payment": False,
                "validation.paymenttype": "",
                "validation.depot": False,}
        })
       
    # for key, value in validation.items():
    #     # If any value is False, return False immediately
    #     if value is False:
    #         db["preregistres"].update_one({"_id":ObjectId(register_id)},{
    #             "$set": {"status":"NOTVALIDATED"}
    #         })
    preregistre = db["preregistres"].find_one_and_update({"_id":ObjectId(register_id)},{
            "$set": {
                
                "personalInfo.first_nameValidation": validation.first_nameValidation,
                "personalInfo.first_nameCause": validation.first_nameCause,
                "personalInfo.last_nameValidation": validation.last_nameValidation,
                "personalInfo.last_nameCause": validation.last_nameCause,
                "personalInfo.cinValidation": validation.cinValidation,
                "personalInfo.cinCause": validation.cinCause,
                "personalInfo.levelValidation": validation.levelValidation,
                "personalInfo.levelCause": validation.levelCause,
                "personalInfo.baccalaureateValidation": validation.baccalaureateValidation,
                "personalInfo.codeValidation": validation.codeValidation,
                "personalInfo.codeCause": validation.codeCause,
                "personalInfo.adresseValidation": validation.adresseValidation,
                "personalInfo.adresseCause": validation.adresseCause,
                "personalInfo.phoneValidation": validation.phoneValidation,
                "personalInfo.phoneCause": validation.phoneCause,
                "personalInfo.brith_dateValidation": validation.brith_dateValidation,
                "personalInfo.brith_dateCause": validation.brith_dateCause,
                "personalInfo.sexeValidation": validation.sexeValidation,
                "personalInfo.sexeCause": validation.sexeCause,
                "personalInfo.departementValidation": validation.departementValidation,
                "personalInfo.departementCause": validation.departementCause,
                "personalInfo.classeValidation": validation.classeValidation,
                "personalInfo.classeCause": validation.classeCause,
                "personalInfo.situationValidation": validation.situationValidation,
                "personalInfo.situationCause": validation.situationCause,
                "family_info.father_nameValidation": validation.father_nameValidation,
                "family_info.father_nameCause": validation.father_nameCause,
                "family_info.mother_nameValidation": validation.mother_nameValidation,
                "family_info.mother_nameCause": validation.mother_nameCause,
                "family_info.mother_phoneValidation": validation.mother_phoneValidation,
                "family_info.mother_phoneCause": validation.mother_phoneCause,
                "family_info.father_phoneValidation": validation.father_phoneValidation,
                "family_info.father_phoneCause": validation.father_phoneCause,
                "family_info.father_jobValidation": validation.father_jobValidation,
                "family_info.father_jobCause": validation.father_jobCause,
                "family_info.mother_jobValidation": validation.mother_jobValidation,
                "family_info.mother_jobCause": validation.mother_jobCause,
                "docs.baccalaureateValidation": validation.baccalaureateValidation,
                "docs.baccalaureateCause": validation.baccalaureateCause,
                "docs.docsuppValidation" : validation.docsuppValidation,
                "docs.docsuppCause": validation.docsuppCause,
                "docs.cinimgValidation": validation.cinimgValidation,
                "docs.cinimgCause": validation.cinimgCause,
                "docs.transcriptsValidation": validation.transcriptsValidation,
                "docs.transcriptsCause": validation.transcriptsCause,
                "docs.note1Validation": validation.note1Validation,
                "docs.note1Cause": validation.note1Cause,
                "docs.note2Validation": validation.note2Validation,
                "docs.note2Cause": validation.note2Cause,
  

                

            }
        },)

    return True



@preregiter_router.get("/preregister/{register_id}")
async def get_register_by_id(register_id):
    preregister = db["preregistres"].find_one({"_id":ObjectId (register_id)})
    preregister["_id"]=str(preregister["_id"])
    user = db["users"].find_one({"_id":preregister["user_id"]})
    preregister["personalInfo"]["email"] = user['email']
    preregister["user_id"]=str(preregister["user_id"])
    
    return {"preregister":preregister}


@preregiter_router.get('/preregister')
async def get_all_preregister():
    preregistres = []
    try:
        # Fetch documents matching the filter
        for preregistre in  db["preregistres"].find({"status": {"$in": ["WAITINGVALIDATION", "PENDING"]}}):
            print(preregistre)
            # Convert ObjectId to string
            preregistre["_id"] = str(preregistre["_id"]) 
            preregistre["user_id"] = str(preregistre["user_id"]) 
            # Convert the bytes to a base64-encoded string using base64.b64encode
            preregistres.append(preregistre)  # Append user object to user_list

        return preregistres  # Return the list of users with status = "PENDING"
    except Exception as ex:
        return {
            "message": f"{str(ex)}"
        }  # Return an error message with exception details if an exception occurs


@preregiter_router.put('/update_register/{register_id}')
async def edit_preregister(register_id,PreRegistration :PreRegistration):
    preregistre = db["preregistres"].update_one({"_id":ObjectId(register_id)},{
            "$set": {
                "status" : "PENDING",
                "personalInfo":{
                "annee" :PreRegistration.personalInfo.annee,
                "first_name": PreRegistration.personalInfo.first_name,
                "last_name": PreRegistration.personalInfo.last_name,
                "cin": PreRegistration.personalInfo.cin,
                "level": PreRegistration.personalInfo.level,
                "baccalaureate": PreRegistration.personalInfo.baccalaureate,
                "code": PreRegistration.personalInfo.code,
                "adresse": PreRegistration.personalInfo.adresse,
                "phone": PreRegistration.personalInfo.phone,
                "status" :  PreRegistration.personalInfo.status,
                "brith_date": PreRegistration.personalInfo.brith_date,
                "sexe" : PreRegistration.personalInfo.sexe,
                "departement" : PreRegistration.personalInfo.departement,
                "classe" : PreRegistration.personalInfo.classe,
                },
                                "family_info" :{
                "father_name": PreRegistration.student_family.father_name,
                "mother_name": PreRegistration.student_family.mother_name,
                "mother_phone": PreRegistration.student_family.mother_phone,
                "father_phone": PreRegistration.student_family.father_phone,
                "father_job": PreRegistration.student_family.father_job,
                "mother_job": PreRegistration.student_family.mother_job,
                }
                

            }
        },)
    

@preregiter_router.put('/update_paiemnt_status/{register_id}')
async def update_paiemnt_status(validated:ValidationBody  ,register_id):

    db["preregistres"].update_one({"_id": ObjectId(register_id)}, {
            "$set": {"validation.payment": validated.validated}
        })


@preregiter_router.put('/update_depot_status/{register_id}')
async def update_depot_status(validated: ValidationBody , register_id):

    db["preregistres"].update_one({"_id": ObjectId(register_id)}, {
            "$set": {"validation.depot": validated.validated ,"status":"VALIDATED"}
        })
    

@preregiter_router.put('/update_classe/{register_id}')
async def update_depot_status(classe: str , register_id):

    db["preregistres"].update_one({"_id": ObjectId(register_id)}, {
            "$set": {"personalInfo.classe": classe }
        })
    

@preregiter_router.put('/update_paymenttype_status/{register_id}')
async def update_paymenttype_status(paymenttype: typepayment ,register_id):

    db["preregistres"].update_one({"_id": ObjectId(register_id)}, {
            "$set": {"validation.paymenttype": paymenttype.type}
        })
    

@preregiter_router.get('/validated_preregister')
async def get_all_validated_preregister():
    preregistres = []
    try:
        # Fetch documents matching the filter
        for preregistre in  db["preregistres"].find({"status": "VALIDATED"}):
            # Convert ObjectId to string
            preregistre["_id"] = str(preregistre["_id"]) 
            preregistre["user_id"] = str(preregistre["user_id"]) 
            # Convert the bytes to a base64-encoded string using base64.b64encode
            preregistres.append(preregistre)  # Append user object to user_list

        return preregistres  # Return the list of users with status = "PENDING"
    except Exception as ex:
        return {
            "message": f"{str(ex)}"
        }  # Return an error message with exception details if an exception occurs



@preregiter_router.get("/get_preregister/{user_id}")
async def get_preregister_by_user_id(user_id):
    preregister = db["preregistres"].find_one({"user_id":ObjectId(user_id) })
    print(preregister)
    preregister['_id']=str(preregister['_id'])
    preregister['user_id']=str(preregister['user_id'])
    return preregister


@preregiter_router.post("/orientation")
async def orientatio(orientation: orientation):
    db['orientation'].insert_one(dict(orientation))
    return True

@preregiter_router.put("/orientation/{orientation_id}")
async def orientatio(orientation: orientation,orientation_id):
    db['orientation'].update_one({"_id":ObjectId(orientation_id)}, {
            "$set": { "choix1": orientation.choix1,"choix2": orientation.choix2,"choix3": orientation.choix3,
"choix4": orientation.choix4       }})
    return True

@preregiter_router.get("/orientation/{user_id}")
async def get_orientationr_by_user_id(user_id):
    orientation = db["orientation"].find_one({"user_id":user_id})
    if orientation :
        orientation['_id']=str(orientation['_id'])
    return orientation


@preregiter_router.get('/orientation_by_dep/{departement}')
async def get_orientation(departement):
  
    all_orientation = []
    orientation = db["orientation"].find()
    
    # Dictionary to store result counts
    result_counts = defaultdict(int)
    
    for orie in orientation:
        print(orie)
        orie['_id'] = str(orie['_id'])
        preregister = db["preregistres"].find_one({"user_id":ObjectId(orie['user_id']) })
        print(preregister)
        if preregister['personalInfo']['departement'] == departement:
            orie['student'] = preregister['personalInfo']
            all_orientation.append(orie)
            # Counting results
            result = orie.get('resultat', '')
            if result:
                result_counts[result] += 1
                
    # Convert result_counts defaultdict to a regular dictionary
    result_counts = dict(result_counts)
    
    return {
        "orientations": all_orientation,
        "result_counts": result_counts
    }


@preregiter_router.get('/orientations')
async def get_orientation():
  
    all_orientation = []
    orientation = db["orientation"].find()
    
    # Dictionary to store result counts
    result_counts = defaultdict(int)
    
    for orie in orientation:

        orie['_id'] = str(orie['_id'])
        preregister = db["preregistres"].find_one({"user_id":ObjectId(orie['user_id']) })

        orie['departement']= preregister['personalInfo']['departement']
        orie['student'] = preregister['personalInfo']['first_name'] + ' '+ preregister['personalInfo']['last_name']
        all_orientation.append(orie)

                

    
    return all_orientation




@preregiter_router.get("/orientation/{user_id}/{parcours}")
async def get_orientationr_by_user_id(user_id,parcours):
    orientation = db["orientation"].update_one({"user_id":user_id},
            {"$set": {       
        "last_update":datetime.now(),        
        "resultat": parcours,
        "status": "validated",
        }})


    return True