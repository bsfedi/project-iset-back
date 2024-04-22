from bson import ObjectId
from fastapi import APIRouter, File, HTTPException
from secuirty import *
from user.models import *
from user.services import *
from argon2 import PasswordHasher
import re
import smtplib

user_router = APIRouter(tags=["User"])

ph = PasswordHasher()

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
gmail_user = "fedislimen98@gmail.com"
pass_code=  "wiuijqbeodgezebw"


import random
import string
subject = f"Invitation to join the platforme"
def generate_password(length=12):
    # Define the characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate the password
    password = ''.join(random.choice(characters) for i in range(length))
    
    return password



@user_router.post(
    "/auth/signup",
)
async def sign_up(user: User):
    """
    Validates a password format based on specified requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    # Get date of today
  
    user.role = "student"
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[a-zA-Z\d@$!%*?&]{8,}$"
    # if re.match(pattern, user.password):
    #     # hash a passsword
    hashed_password = ph.hash(user.password)
    user.password = hashed_password
    user_id = signup(user)
    if user_id:
        return {"message": "user added succesfully !"}
    else:
        raise HTTPException(
            status_code=411,
            detail="Password format is invalid. It must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character.",
        )

import csv
expected_header = ["nom", "prenom", "code_enseignement", "email", "numtel", "identifiantunique","departement", "role" ,"grade"]


@user_router.post(
    "/auth/newuser",
)
async def sign_up(user: New_user):
    """
    Validates a password format based on specified requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    # Get date of today
    if db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=409, detail="Email address already in use")
    
    try:
        password = generate_password()
        hashed_password = ph.hash(password)
        user.password = hashed_password          
        sender_address = gmail_user
        sender_pass = pass_code
        receiver_address = user.email
        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = user.email
        message["Subject"] = subject

                            # Attach the additional information and HTML table to the email
        message.attach(MIMEText(f"<b>  votre {user.code} et le mot de passe est {password} <b> ", "html"))

                            # Create SMTP session for sending the mail
        session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        response = db["users"].insert_one(dict(user))
        return {"response":"user added sucessfully"}
    except Exception as e:
        return False
    




@user_router.post("/upload_users")
async def upload_file(file: UploadFile = File(...)):
    try:
        
        # Check if the uploaded file is a CSV file
        if file.filename.endswith('.csv'):
            contents = await file.read()
            decoded_contents = contents.decode('utf-8').splitlines()
            
            # Read the CSV rows
            csv_reader = csv.DictReader(decoded_contents)
            
            for row in csv_reader:
                
                # Check if the header matches the expected header
                if list(row.keys()) == expected_header:
                    existing_user = db["users"].find_one({"email": row["email"]}) 
                    if existing_user:
                        pass
                    else:
                        password = generate_password()
                        hashed_password = ph.hash(password)
                        new_user_data = {
                        "first_name": row["nom"],
                        "last_name": row["prenom"],
                        "code": row["code_enseignement"],
                        "email": row["email"],
                        "phone": row["numtel"],
                        "identifiant": row["identifiantunique"],
                        "departement": row["departement"],
                        "grade": row["grade"],
                        "password":hashed_password ,
                        "role": row["role"]  # You may need to adjust this depending on your requirements
                        }
                        new_user = New_user(**new_user_data)
                        # Insert the new user into MongoDB
                        
                        try:
                            code =row["code_enseignement"]
                            sender_address = gmail_user
                            sender_pass = pass_code
                            receiver_address = row["email"]
                            message = MIMEMultipart()
                            message["From"] = sender_address
                            message["To"] = row["email"]
                            message["Subject"] = subject

                            # Attach the additional information and HTML table to the email
                            message.attach(MIMEText(f"<b>  votre {code} et le mot de passe est {password} <b> ", "html"))

                            # Create SMTP session for sending the mail
                            session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
                            session.starttls()  # enable security
                            session.login(sender_address, sender_pass)  # login with mail_id and password
                            text = message.as_string()
                            session.sendmail(sender_address, receiver_address, text)
                            db['users'].insert_one(new_user.dict())
                            
                        except Exception as e:
                            return False
                else:
                    return {"error": "Header does not match the expected format"}
            
            return {"message": "Data inserted successfully"}
            
        else:
            return {"error": "Uploaded file is not a CSV"}
    except Exception as e:
        return {"error": str(e)}


@user_router.post(
    "/auth/login",
)
async def login_api(userr: User_login):
    """
    API endpoint for user login.

    Args:
        userr (User_login): User login information (email, password) .

    Returns:
        dict: Dictionary containing user email and access token.

    """
    # retrieves the user from the database by email
    user = get_user_by_email(userr.email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # verify the password hash
    verify_password(user.get("password"), userr.password)
    preregister_id = db["preregistres"].find_one({"user_id":user["_id"]})
    token = create_access_token({"id": str(user["_id"])})
    if preregister_id :
        return {"user": user["email"], "role" : user["role"], "register_id" :str(preregister_id["_id"]),"user_id":str(user["_id"]),"token": token}
    # Create an access token with user ID
    else:
        return {"user": user["email"], "role" : user["role"], "user_id":str(user["_id"]),"token": token}

    


@user_router.get(
    "/users",
)
async def get_list_users():
    """
    API endpoint for getting a list of all users.

    Args:
        token (dict): Token required for authentication.

    Returns:
        dict: Dictionary containing a list of all users.

    """

    all_users = get_all_users()
    return {"users": all_users}


@user_router.get("/user/{user_id}")
async def get_user_by_id(user_id):
    user = db["users"].find_one({"_id":ObjectId(user_id)})
    user['_id']=str(user['_id'])
    return user

@user_router.get('/enseignants/{departement}')
async def get_all_enseignants(departement):
    all_enseignants = []
    enseignants =db["users"].find({"role": "enseignant","departement":departement})
    for ee in enseignants :
        
        ee['_id']=str(ee['_id'])
        all_enseignants.append(ee)
    return all_enseignants
    
    
