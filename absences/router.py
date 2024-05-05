
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
            if etudiant :
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
async def get_classe_by_module(module_id: str):
    unique_classes = set()  # Initialize an empty set to store unique class IDs
    all_classe = []
    modules = db["absences"].find({'module': {'$in': [module_id]}})
    for module in modules:
        module['_id'] = str(module['_id'])
        for classe_id in module['classe']:
            if classe_id not in unique_classes:  # Check if class ID is already in the set
                unique_classes.add(classe_id)  # If not, add it to the set
                classe = db["classes"].find_one({'_id': ObjectId(classe_id)})
                if classe:
                    classe['_id'] = str(classe['_id'])
                    all_classe.append(classe)
    return all_classe



@absence_router.get('/get_modules_by_enseignant/{enseignant_id}')
async def get_modules_by_enseignant(enseignant_id: str):
    unique_modules = set()  # Initialize an empty set to store unique module IDs
    all_classe = []
    modules = db["absences"].find({'enseignant': {'$in': [enseignant_id]}})
    for module in modules:
        for m in module['module']:
            m_id = str(m)
            if m_id not in unique_modules:  # Check if module ID is already in the set
                unique_modules.add(m_id)  # If not, add it to the set
                m_doc = db["modules"].find_one({'_id': ObjectId(m_id)})
                m_doc['_id'] = str(m_doc['_id'])
                all_classe.append(m_doc)
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
        print(etudiant['user_id'], module_id)
        absences = db["student_absence"].find_one({"user_id": etudiant['user_id'], "module_id": module_id})
        print(absences)
        nb_absence = 0  # Initialize absence counter for the student
        if absences:  # Check if absences are found
            for i in range(1, 13):
                # Assuming 'S1', 'S2', ..., 'S12' are keys in absences dictionary
                if "S" + str(i) in absences and absences["S" + str(i)] == "1":
                    nb_absence += 1  # Increment absence count if absence recorded for the session
                print(nb_absence)
        etudiant['nb_absence'] = nb_absence  # Add absence count to the student object
        all_students.append(etudiant)      
    return all_students

@absence_router.get("/get_absences/{student_id}")
async def get_absences(student_id):
    all_absences = []
    absences = db["student_absence"].find({"user_id":student_id })
    for ab in absences :
        ab['_id']=str(ab['_id'])
        ab["module_id"] =  db['modules'].find_one({"_id":ObjectId(ab["module_id"])})['code']
        nb_absence = 0  # Initialize absence counter for the student

        for i in range(1, 13):
                    # Assuming 'S1', 'S2', ..., 'S12' are keys in absences dictionary
            if "S" + str(i) in ab and ab["S" + str(i)] == "1":
                nb_absence += 1  # Increment absence count if absence recorded for the session
        ab['nb_absence'] = nb_absence  # Add absence count to the student object
        all_absences.append(ab)  
    return all_absences

@absence_router.get('/get_classe_module_by_dep/{departement}')
async  def  get_classe_module_by_dep(departement):
    all_calsse = []
    all_modules =[]
    modules = db['modules'].find({"departement":departement})
    for module in modules:
        module['_id'] =str(module['_id'])
        all_modules.append(module)
    classes = db['classes'].find({"departement":departement})
    for classe in classes:
        classe['_id'] =str(classe['_id'])
        all_calsse.append(classe)
    return {"all_calsse" :all_calsse , "all_modules":all_modules}

