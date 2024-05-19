
import os
from bson import ObjectId
from fastapi import APIRouter, File, HTTPException ,Form,UploadFile
from rattrapage.models import *
from secuirty import *
from demande.models import *

from database import db
import random




rattrapge_router = APIRouter(tags=["rattrapge"])



@rattrapge_router.post("/add_absence/{enseignant_id}")
async def upload_file(
    enseignant_id,
    dureé: str = Form(...),
    date: Optional[datetime] = Form(None),
    date_debut: Optional[datetime] = Form(None),
    date_fin: Optional[datetime] = Form(None),
    justificatif:  Optional[UploadFile] = File(None)
):
    if justificatif:
        with open(os.path.join("uploads", justificatif.filename), "wb") as buffer:
            buffer.write(await justificatif.read())

    # Generate random number between 0 and 99
    random_number = random.randint(0, 99)
    
    # Get the current date
    date_depot = datetime.now()
    
    # Generate id_demande
    id_demande = f"da_{date_depot.strftime('%d%m')}/{date_depot.strftime('%m')}{random_number:02d}"
    
    # Prepare update_data
    update_data = {}
    if justificatif:
        update_data["note1"] = justificatif.filename

    # Insert data into the database
    response = db["absence"].insert_one({
        "enseignant_id": enseignant_id,
        "date_depot": date_depot,
        "dureé": dureé,
        "date": date,
        "status":"pending",
        "date_debut": date_debut,
        "date_fin": date_fin,
        "justificatif": update_data.get("note1"),
        "id_demande": id_demande
    })

    return {"message": "demande absence added"}


from datetime import datetime, timedelta

@rattrapge_router.get("/get_absence_by_enseignant_id/{enseignant_id}")
async def get_absence_by_enseignant_id(enseignant_id):
    all_demandes = []
    absences = db["absence"].find({"enseignant_id": enseignant_id})
    for ab in absences:
        ab['_id'] = str(ab['_id'])
        if ab["dureé"] == "plusieurs" and ab["date_debut"] and ab["date_fin"]:
            date_debut = ab["date_debut"]
            date_fin = ab["date_fin"]
            dates_between = [date_debut + timedelta(days=x) for x in range((date_fin - date_debut).days + 1)]
            for date in dates_between:
                all_demandes.append({
                    "_id": ab["_id"],
                     "status":"pending",
                    "enseignant_id": ab["enseignant_id"],
                    "date": date.strftime("%Y-%m-%d"),
                    "justificatif": ab["justificatif"]
                })
        else:
            ab["date"] = ab["date"].strftime("%Y-%m-%d")
            all_demandes.append(ab)
    return all_demandes


@rattrapge_router.get("/get_absence_enseignant_id/{enseignant_id}")
async def get_absence_by_enseignant_id(enseignant_id):
    all_demandes = []
    absences = db["absence"].find({"enseignant_id": enseignant_id})
    for ab in absences:
        ab['_id'] = str(ab['_id'])
        if ab["dureé"] == "plusieurs" and ab["date_debut"] and ab["date_fin"]:
            date_debut = ab["date_debut"]
            date_fin = ab["date_fin"]
            dates_between = [date_debut + timedelta(days=x) for x in range((date_fin - date_debut).days + 1)]
            ab["date_depot"] = ab["date_depot"].strftime("%Y-%m-%d")
            ab["duree"] = len(dates_between)
            all_demandes.append(ab)
        else:
            ab["date_depot"] = ab["date_depot"].strftime("%Y-%m-%d")
            ab["date"] = ab["date"].strftime("%Y-%m-%d")
            all_demandes.append(ab)
    return all_demandes
    

@rattrapge_router.post("/add_rattrapage/{enseignant_id}")
async def upload_file(
    enseignant_id,
    rattrapage : rattrapage ):
    date_depot = datetime.now()
    random_number = random.randint(0, 99)
    # Generate id_demande
    id_demande = f"da_{date_depot.strftime('%d%m')}/{date_depot.strftime('%m')}{random_number:02d}"
    response = db["rattrapage"].insert_one({
        "data" :rattrapage.data,
        "type":rattrapage.type,
        "enseignant_id":enseignant_id,
         "status":"pending",
         "id_demande": id_demande,
         "date_depot":date_depot


    })
    return {"message":"demande absence added"}

@rattrapge_router.get("/rattrapage_by_department/{user_id}")
async def get_demande_attestation(user_id):
    list_attes = []
    user = db["users"].find_one({"_id": ObjectId(user_id)})
    response = db["rattrapage"].find()
    
    for attes in response:
        attes['_id'] = str(attes['_id'])
        
        if db["users"].find_one({"_id": ObjectId(attes["enseignant_id"])})["departement"] == user["departement"]:
            enseignant_name = db["users"].find_one({"_id": ObjectId(attes["enseignant_id"])})["first_name"] + " " + db["users"].find_one({"_id": ObjectId(attes["enseignant_id"])})["last_name"]
            
        for data_item in attes["data"]:
                # Check if any of the fields are empty
            if all(data_item[field] for field in ["date", "inputClass", "inputModule", "inputHoraire"]):
                new_entry = attes.copy()
                new_entry["data"] = [data_item]
                new_entry["enseignant_id"] = enseignant_name
                list_attes.append(new_entry)
    
    return list_attes

@rattrapge_router.get('/get_historique/{date}/{classe}')
async def get_historique(date, classe):
    all_rattrapge_data = []
    rattrapge_data = db['rattrapage'].find({
        "status":"validated",
        "data": {
            "$elemMatch": {
                "inputClass": classe,
                "date": date
            }
        }
    })
    for rattrapge in rattrapge_data:
        print(rattrapge)
        rattrapge['_id']=str(rattrapge['_id'])
        for data in rattrapge["data"]:
            if data['date'] == date:
                all_rattrapge_data.append(data)
    return all_rattrapge_data

 






@rattrapge_router.get("/rattrapage/{enseignant_id}")
async def get_demande_attestation(enseignant_id):
    list_attes = []
    response = db["rattrapage"].find({"enseignant_id": enseignant_id})
    for attes in response:
        attes['_id']=str(attes['_id'])
        for data_item in attes["data"]:
                # Check if any of the fields are empty
            if all(data_item[field] for field in ["date", "inputClass", "inputModule", "inputHoraire"]):
                new_entry = attes.copy()
                new_entry["data"] = [data_item]
               
                list_attes.append(new_entry)
        
    return list_attes

@rattrapge_router.put("/rattrapage/{rattrapage_id}")
async def update_rattrapage(rattrapage_id, status: status):
    if status.motif:
        response = db["rattrapage"].update_one(
            {
                "_id": ObjectId(rattrapage_id),
                "data": {
                    "$elemMatch": {
                        "inputClass": status.classe,
                        "inputModule": status.module,
                        "inputHoraire": status.horaire,
                        "date": status.date
                    }
                }
            },
            {
                "$set": {
                    "data.$.status": status.status,
                    "data.$.motif": status.motif,
                }
            }
        )
    else:
        ee= db["rattrapage"].find_one(
            {
                "_id": ObjectId(rattrapage_id),
                "data": {
                    "$elemMatch": {
                        "inputClass": status.classe,
                        "inputModule": status.module,
                        "inputHoraire": status.horaire,
                        "date": status.date
                    }
                }
            })
        print(ee)
        response = db["rattrapage"].update_one(
            {
                "_id": ObjectId(rattrapage_id),
                "data": {
                    "$elemMatch": {
                        "inputClass": status.classe,
                        "inputModule": status.module,
                        "inputHoraire": status.horaire,
                        "date": status.date
                    }
                }
            },
            {
                "$set": {
                    "data.$.status": status.status,
                    "data.$.salle": status.salle,
                    "data.$.horaire": status.new_horaire
                }
            }
        )
    return True




@rattrapge_router.get("/validated_rattrapage")
async def get_demande_attestation():
    list_attes = []

    response = db["rattrapage"].find({"status": "validated"})
    
    for attes in response:
        attes['_id'] = str(attes['_id'])
        
        
        enseignant_name = db["users"].find_one({"_id": ObjectId(attes["enseignant_id"])})["first_name"] + " " + db["users"].find_one({"_id": ObjectId(attes["enseignant_id"])})["last_name"]
            
        for data_item in attes["data"]:
                # Check if any of the fields are empty
            if all(data_item[field] for field in ["date", "inputClass", "inputModule", "inputHoraire"]):
                new_entry = attes.copy()
                new_entry["data"] = [data_item]
                new_entry["enseignant_id"] = enseignant_name
                list_attes.append(new_entry)
    
    return list_attes
@rattrapge_router.get("/validated_rattrapage/{rattrapage_id}/{status}")
async def get_demande_attestation(status,rattrapage_id):
    response = db["rattrapage"].update_one(
                {"_id": ObjectId(rattrapage_id)},{
                    "$set": {"excuted":status}
                }
                
                )
    return True


