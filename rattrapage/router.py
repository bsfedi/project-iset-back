
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
    user = db["users"].find_one({"_id":ObjectId(user_id)})
    response = db["rattrapage"].find()
    for attes in response:
        attes['_id']=str(attes['_id'])
        print(attes["enseignant_id"])
        if db["users"].find_one({"_id":ObjectId(attes["enseignant_id"] )})["departement"] == user["departement"]:
            attes['enseignant_id']=  db["users"].find_one({"_id":ObjectId(attes["enseignant_id"] )})["first_name"] + " "+ db["users"].find_one({"_id":ObjectId(attes["enseignant_id"] )})["last_name"]
            list_attes.append(attes)
    return list_attes

@rattrapge_router.get("/rattrapage/{enseignant_id}")
async def get_demande_attestation(enseignant_id):
    list_attes = []
    response = db["rattrapage"].find({"enseignant_id": enseignant_id})
    for attes in response:
        attes['_id']=str(attes['_id'])
        list_attes.append(attes)
    return list_attes

@rattrapge_router.put("/rattrapage/{rattrapage_id}")
async def update_rattrapage(rattrapage_id,status:status):
    if status.motif:
        response = db["rattrapage"].update_one(
                {"_id": ObjectId(rattrapage_id)},{
                    "$set": {"status":status.status,"motif":status.motif}
                }
                
                )
    else:

        response = db["rattrapage"].update_one(
                {"_id": ObjectId(rattrapage_id)},{
                    "$set": {"status":status.status,
                             "salle":status.salle,
                             "horaire":status.horaire}
                }
                
                )
    return True
