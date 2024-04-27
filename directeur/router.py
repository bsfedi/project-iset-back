
import os
from bson import ObjectId
from fastapi import APIRouter, File, HTTPException ,Form,UploadFile
from directeur.models import *
from secuirty import *
from demande.models import *

from database import db
import random




directeur_router = APIRouter(tags=["directeur"])




# Create
@directeur_router.post("/add_parcours")
async def add_parcours(parcours: parcours):
    db['parcours'].insert_one(parcours.dict())
    return {"message": "Parcours added successfully!"}

# Read
@directeur_router.get("/get_parcour/{parcours_id}")
async def get_parcours(parcours_id: str):
    parcours = db['parcours'].find_one({"_id": ObjectId(parcours_id)})
    if parcours:
        parcours['_id']=str(parcours['_id'])
        return parcours

# Read
@directeur_router.get("/get_parcours")
async def get_parcours():
    all_parcours =[]
    parcours = db['parcours'].find()
    for parcour in parcours:
        parcour['_id']=str(parcour['_id'])
        all_parcours.append(parcour)
    return all_parcours
    
# Update
@directeur_router.put("/update_parcours/{parcours_id}")
async def update_parcours(parcours_id: str, parcours: parcours):
    updated = db['parcours'].update_one({"_id": ObjectId(parcours_id)}, {"$set": parcours.dict()})
    if updated.modified_count:
        return {"message": "Parcours updated successfully!"}
    raise HTTPException(status_id=404, detail="Parcours not found")

# Delete
@directeur_router.delete("/delete_parcours/{parcours_id}")
async def delete_parcours(parcours_id: str):
    deleted = db['parcours'].delete_one({"_id": ObjectId(parcours_id)})
    if deleted.deleted_count:
        return {"message": "Parcours deleted successfully!"}
    raise HTTPException(status_id=404, detail="Parcours not found")


# Create
@directeur_router.post("/add_classe")
async def add_classes(classe: classes):
    db['classes'].insert_one(classe.dict())
    return {"message": "classes added successfully!"}

# Read
@directeur_router.get("/get_classe/{classe_id}")
async def get_classes(classe_id: str):
    classes = db['classes'].find_one({"_id": ObjectId(classe_id)})
    if classes:
        classes['_id']=str(classes['_id'])
        return classes

# Read
@directeur_router.get("/get_classes")
async def get_classes():
    all_classes =[]
    classes = db['classes'].find()
    for classe in classes:
        if db['parcours'].find_one({"_id": ObjectId(classe['parcour'])}):
            classe['parcour'] = db['parcours'].find_one({"_id": ObjectId(classe['parcour'])})["libelle"] 
        else:
            classe['parcour'] = "" 

        classe['_id']=str(classe['_id'])
        all_classes.append(classe)
    return all_classes

    
# Update
@directeur_router.put("/update_classes/{classes_id}")
async def update_classes(classes_id: str, classes: classes):
    updated = db['classes'].update_one({"_id": ObjectId(classes_id)}, {"$set": classes.dict()})
    if updated.modified_count:
        return {"message": "classes updated successfully!"}
    raise HTTPException(status_id=404, detail="classes not found")

# Delete
@directeur_router.delete("/delete_classes/{classes_id}")
async def deleteclasses(classes_id: str):
    deleted = db['classes'].delete_one({"_id": ObjectId(classes_id)})
    if deleted.deleted_count:
        return {"message": "classes deleted successfully!"}
    raise HTTPException(status_id=404, detail="classes not found")



# Create
@directeur_router.post("/add_module")
async def add_modules(modules: modules):
    db['modules'].insert_one(modules.dict())
    return {"message": "modules added successfully!"}

# Read
@directeur_router.get("/get_module/{module_id}")
async def get_modules(module_id: str):
    modules = db['modules'].find_one({"_id": ObjectId(module_id)})
    if modules:
        modules['_id']=str(modules['_id'])
        return modules

# Read
@directeur_router.get("/get_modules")
async def get_modules():
    all_modules =[]
    modules = db['modules'].find()
    for module in modules:
        if db['parcours'].find_one({"_id": ObjectId(module['parcours'])}):
            module['parcours'] =  db['parcours'].find_one({"_id": ObjectId(module['parcours'])})["libelle"] 
        else:
            module['parcour'] = "" 
        module['_id']=str(module['_id'])
        all_modules.append(module)
    return all_modules

    
# Update
@directeur_router.put("/update_modules/{modules_id}")
async def update_modules(modules_id: str, modules: modules):
    updated = db['modules'].update_one({"_id": ObjectId(modules_id)}, {"$set": modules.dict()})
    if updated.modified_count:
        return {"message": "modules updated successfully!"}
    raise HTTPException(status_id=404, detail="modules not found")

# Delete
@directeur_router.delete("/delete_modules/{modules_id}")
async def deletemodules(modules_id: str):
    deleted = db['modules'].delete_one({"_id": ObjectId(modules_id)})
    if deleted.deleted_count:
        return {"message": "modules deleted successfully!"}
    raise HTTPException(status_id=404, detail="modules not found")



# Create
@directeur_router.post("/add_salle")
async def add_salles(salles: salles):
    db['salles'].insert_one(salles.dict())
    return {"message": "salles added successfully!"}

# Read
@directeur_router.get("/get_salle/{salle_id}")
async def get_salles(salle_id: str):
    salles = db['salles'].find_one({"_id": ObjectId(salle_id)})
    if salles:
        salles['_id']=str(salles['_id'])
        return salles

# Read
@directeur_router.get("/get_salles")
async def get_salles():
    all_salles =[]
    salles = db['salles'].find()
    for salle in salles:
        salle['_id']=str(salle['_id'])
        all_salles.append(salle)
    return all_salles

    
# Update
@directeur_router.put("/update_salles/{salles_id}")
async def update_salles(salles_id: str, salles: salles):
    updated = db['salles'].update_one({"_id": ObjectId(salles_id)}, {"$set": salles.dict()})
    if updated.modified_count:
        return {"message": "salles updated successfully!"}
    raise HTTPException(status_id=404, detail="salles not found")

# Delete
@directeur_router.delete("/delete_salles/{salles_id}")
async def deletesalles(salles_id: str):
    deleted = db['salles'].delete_one({"_id": ObjectId(salles_id)})
    if deleted.deleted_count:
        return {"message": "salles deleted successfully!"}
    raise HTTPException(status_id=404, detail="salles not found")