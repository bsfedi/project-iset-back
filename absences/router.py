
import os
from bson import ObjectId
from fastapi import APIRouter, File, HTTPException
from secuirty import *
from absences.models import *
from database import db




absence_router = APIRouter(tags=["Absences"])


@absence_router.post("/absence")
def signup(modules: modules):

    # Inserting the data into the database
    response = db["absences"].insert_one(dict(modules))
    for module in modules.module:
            
        for classe in modules.classe:
            classe_code = db["classes"].find_one({'_id': ObjectId(classe)})['code']
            etudiant = db["preregistres"].find_one({"personalInfo.classe": classe_code})
            db['student_absence'].insert_one({
                "user_id":str(etudiant['user_id']),
                "module_id": module,
                "classe_id": classe,
                "S1": "",
                "S2": "",
                "S3": "",
                "S4": "",
                "S5": "",
                "S6": "",
                "S7": "",
                "S8": "",
                "S9": "",
                "S10": "",
                "S11": "",
                "S12": "",
                "reclamation" : []

            })


    if response:
        return {
            "message": "Demande added successfully!"
        }
    
@absence_router.put("/renseigner_absence/{absence_id}")
async def renseigner_absence(absence_id,data:dict):
    print(data)
    db['student_absence'].update_one({'_id':ObjectId(absence_id)},{
        "$set" :
            data
        
    })
    return True
    
@absence_router.get("/get_absences_by_classe/{classe_id}")
async def  get_absences_by_classe(classe_id):
    all_absences = []
    all_students = db['student_absence'].find({'classe_id':classe_id})
    for student in all_students:
        print(student)
        etudiant = db["preregistres"].find_one({"user_id":ObjectId(student['user_id']) })
        etudiant['user_id'] =str(etudiant['user_id'] )
        etudiant['_id'] =str(etudiant['_id'] )
        student['etudiant']=etudiant
        student['_id']=str(student['_id'])
        all_absences.append(student)
    return(all_absences)

@absence_router.get('/get_classe_by_module/{module_id}')
async def get_modules_by_enseignant(module_id: str):
    all_classe = []
    modules = db["absences"].find({'module': {'$in': [module_id]}})
    for module in modules:
        module['_id'] = str(module['_id'])
        for classe_id in module['classe']:
            classe = db["classes"].find_one({'_id': ObjectId(classe_id)})
            if classe:
                classe['_id'] = str(classe['_id'])
                all_classe.append(classe)
    return all_classe


@absence_router.get('/get_modules_by_enseignant/{enseignant_id}')
async def get_modules_by_enseignant(enseignant_id: str):
    all_classe = []
    modules = db["absences"].find({'enseignant': {'$in': [enseignant_id]}})
    for module in modules:
        for m in module['module']:
        
            m = db["modules"].find_one({'_id': ObjectId(m)})
            m['_id'] = str(m['_id'])

            all_classe.append(m)
    return all_classe

@absence_router.get('/students_module/{module_id}')
async def get_students_module(module_id):
    all_students = []
    module = db["absences"].find_one({'module': {'$in': [module_id]}})
  
    for classe in module['classe']:
        print(classe)
        classe_code = db["classes"].find_one({'_id': ObjectId(classe)})['code']
        print(classe_code)
        etudiant = db["preregistres"].find_one({"personalInfo.classe": classe_code})
        
        etudiant['user_id'] = str(etudiant['user_id'])
        etudiant['_id'] = str(etudiant['_id'])
        print()
        absences = db["student_absence"].find_one({"user_id": etudiant['user_id'], "module_id": ObjectId(module_id)})
        print(absences)
        nb_absence = 0  # Initialize absence counter for the student
        if absences:  # Check if absences are found
            for i in range(1, 13):
                # Assuming 'S1', 'S2', ..., 'S12' are keys in absences dictionary
                if "S" + str(i) in absences and absences["S" + str(i)] == "1":
                    nb_absence += 1  # Increment absence count if absence recorded for the session

        etudiant['nb_absence'] = nb_absence  # Add absence count to the student object
        all_students.append(etudiant)      
    return all_students


