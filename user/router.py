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
subject = f"Compte Enseignant créé sur la plateforme SGI-ISETN"
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
        message.attach(MIMEText(f" Bonjour, <br> Un compte de gestion avec le profil “Enseignant” a été créé en votre nom sur la plateforme de gestion intégrée de l’ISET de Nabeul. Pour y accéder, veuillez utiliser les paramètres suivants:  <br>   Nom d’utilisateur : <b> {user.first_name} {user.last_name} </b> <br> <b> Mot de passe:  {password} </b> <br> En cas de difficultés, vous pouvez contacter l’administrateur de la plateforme via mail ou par téléphone.  ", "html"))

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
    

@user_router.post(
    "/send_email/{user_id}",
)
async def sign_up(user_id,send_email: send_email
):
    """
    Validates a password format based on specified requirements:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """
    
    try:
        user =db["users"].find_one({"_id": ObjectId(user_id)})      
        sender_address = gmail_user
        sender_pass = pass_code
        receiver_address = user['email']
        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = user['email']
        message["Subject"] = send_email.subject

                            # Attach the additional information and HTML table to the email
        message.attach(MIMEText(send_email.message, "html"))

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

@user_router.put(
    "/users/set_password/{user_id}",
)
async def set_password(user_password: User_password, user_id):
    """
    Update the password of a user in the database based on their user_id.

    Args:
        user_id (str): The user_id of the user whose password needs to be updated.
        password (str): The new password to be set.

    Returns:
        pymongo.results.UpdateResult: The result of the update operation.
    """


    hashed_password = ph.hash(user_password.password)

    # Update the password in the database

    update_password(user_id, hashed_password)
    return {"message": "password updated successfully !"}





EMAIL_URL = "https://front-project-iset-4q2w.vercel.app/"
@user_router.post(
    "/auth/forgot-password",
)
async def reset_password(user: User_email):
    """
    Reset password for a user by email address.

    Args:
        user (User_email): User_email object containing the email address of the user.

    Returns:
        dict: Dictionary containing a success message indicating that an email has been sent for password reset.

    Raises:
        HTTPException: If the user does not exist or if there is an error sending the email.

    """
    # Get user by email
    user = get_user_by_email(user.email)
    if not user:
        raise HTTPException(status_code=404, detail="user does not exist!")
    if user['role'] != "student":
        receiver = user["email"]
        first_name = user["first_name"]
        id_user = str(user["_id"])
    else:
        user1 = db["preregistres"].find_one(dict(user_id=ObjectId(str(user["_id"]))))
        receiver = user1['personalInfo']['email']
        first_name = user1['personalInfo']['first_name']
        id_user = str(user["_id"])

    
    # Send password reset email
    subject = "Password reset request"
    first_name=first_name[0].upper()  + first_name[1:]
    HTMLPart = f"""
    Dear <b>{first_name}</b> , <br> \
    We have received a request to reset the password associated with this email address. <br> \
    If you did not make this request, please ignore this email and your account will remain secure.<br> \
    If you did request a password reset, please verify your email address by clicking on the link below: <br> \
   <a href="{EMAIL_URL}change-mot-de-passe/{id_user}"> Set password </a>.<br>\
    Please note that this link will expire in 24 hours for security reasons. <br>\
    Best regards,
"""



    try : 
        sender_address = gmail_user
        sender_pass = pass_code
        mail_content = HTMLPart
        receiver_address = receiver
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver
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
    
@user_router.put("/user/{user_id}")
async def update_user(user_id,updateuser :updateuser):
    user = db["users"].find_one(dict(_id=ObjectId(user_id)))
    if user['role'] == 'student':
        db["preregistres"].update_one({"user_id":ObjectId(user_id)},{
                    "$set": {
                      
                        

                        "personalInfo.first_name": updateuser.first_name,
                        "personalInfo.last_name": updateuser.last_name,
                        "personalInfo.adresse": updateuser.adresse,
                        "personalInfo.phone": updateuser.phone,
                     

                        

                    }
                },)


    else:
        db["users"].update_one({"_id":ObjectId(user_id)},{
                    "$set": {
                        
                        

                        "first_name": updateuser.first_name,
                        "last_name": updateuser.last_name,
                        "adresse": updateuser.adresse,
                        "phone": updateuser.phone,
                     

                        

                    }
                },)
        



@user_router.put("/update_user/{user_id}")
async def update_user(user_id,newupdateuser :newupdateuser):

    db["users"].update_one({"_id":ObjectId(user_id)},{
                    "$set": {
                        
                        "departement": newupdateuser.departement,
                        "phone": newupdateuser.phone,
                     

                        

                    }
                },)
        


@user_router.put(
    "/users/update_password/{user_id}",)
async def updatee_password(
    user_id, password: new_password_user
):
    """
    API endpoint for updating the password of a user.

    Args:
        user_id (str): ID of the user to update.
        password (new_password_user): new_password_user object containing old and new password.
        token (dict): Token required for authentication.

    Returns:
        dict: Dictionary containing a success message.

    """
    response = update_new_password(
        user_id, password.old_password, password.new_password
    )
    if response == True:
        return {"message": "Your password changed successfully"}



@user_router.get('/forget_password/{email}')
async def forget_mot_depasse(email):
    try:       
        sender_address = gmail_user
        sender_pass = pass_code
        receiver_address = email
        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = email
        message["Subject"] = subject

                            # Attach the additional information and HTML table to the email
        message.attach(MIMEText(f"<b>  votre {user.code} et le mot de passe est {password} <b> ", "html"))

                            # Create SMTP session for sending the mail
        session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        return {"response":"user added sucessfully"}
    except Exception as e:
        return False

@user_router.post("/upload_users/{type}")
async def upload_file(type,file: UploadFile = File(...)):
    try:
        if type == "enseignant":
            expected_header = ["nom", "prenom", "code_enseignement", "email", "numtel", "identifiantunique","departement", "role" ,"grade"]
        # Check if the uploaded file is a CSV file
            if file.filename.endswith('.csv'):
                contents = await file.read()
                decoded_contents = contents.decode('utf-8').splitlines()
                
                # Read the CSV rows
                csv_reader = csv.DictReader(decoded_contents)
                
                for row in csv_reader:
                    print(row.keys())
                    print(expected_header)     
                    # Check if the header matches the expected header
                    if list(row.keys()) == expected_header:
                        print(row)
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
                            "role": "enseignant"  # You may need to adjust this depending on your requirements
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
        elif type == "technicien":
            expected_header = ["nom", "prenom", "email", "numtel", "identifiantunique","departement"]
            if file.filename.endswith('.csv'):
                contents = await file.read()
                decoded_contents = contents.decode('utf-8').splitlines()
                
                # Read the CSV rows
                csv_reader = csv.DictReader(decoded_contents)
                
                for row in csv_reader:
                    print(row.keys())
                    print(expected_header)
                    # Check if the header matches the expected header
                    if list(row.keys()) == expected_header:
                        print(row)
                        existing_user = db["users"].find_one({"email": row["email"]}) 
                        if existing_user:
                            pass
                        else:
                            password = generate_password()
                            hashed_password = ph.hash(password)
                            new_user_data = {
                            "first_name": row["nom"],
                            "last_name": row["prenom"],
                            "code": "",
                            "grade": "",
                            "email": row["email"],
                            "phone": row["numtel"],
                            "identifiant": row["identifiantunique"],
                            "departement": row["departement"],
                            "role": "technicien",
                            "password":hashed_password ,
                            }
                            new_user = New_user(**new_user_data)
                            # Insert the new user into MongoDB
                            
                            try:
                               
                                sender_address = gmail_user
                                sender_pass = pass_code
                                receiver_address = row["email"]
                                message = MIMEMultipart()
                                message["From"] = sender_address
                                message["To"] = row["email"]
                                message["Subject"] = subject

                                # Attach the additional information and HTML table to the email
                                message.attach(MIMEText(f"<b>  votre  mot de passe est {password} <b> ", "html"))

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
        else:
            expected_header = ["nom", "prenom", "email", "numtel", "identifiantunique","service"]

            if file.filename.endswith('.csv'):
                contents = await file.read()
                decoded_contents = contents.decode('utf-8').splitlines()
                
                # Read the CSV rows
                csv_reader = csv.DictReader(decoded_contents)
                
                for row in csv_reader:
                    print(expected_header)
                    print(list(row.keys()) )
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
                            "grade" : "",
                            "code": "",
                            "department" : "" ,
                            "email": row["email"],
                            "phone": row["numtel"],
                            "identifiant": row["identifiantunique"],
                            "service": row["service"],
                            "role": "personneladministratif",
                            "password":hashed_password ,
                              # You may need to adjust this depending on your requirements
                            }
                            print(new_user_data)
                            new_user = New_user(**new_user_data)
                            print(new_user)
                            # Insert the new user into MongoDB
                            
                            try:
                                
                                sender_address = gmail_user
                                sender_pass = pass_code
                                receiver_address = row["email"]
                                message = MIMEMultipart()
                                message["From"] = sender_address
                                message["To"] = row["email"]
                                message["Subject"] = subject

                                # Attach the additional information and HTML table to the email
                                message.attach(MIMEText(f"<b>  votre mot de passe est {password} <b> ", "html"))

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


@user_router.get('/enseignants')
async def get_all_enseignants():
    all_enseignants = []
    enseignants =db["users"].find({"role": "enseignant"})
    for ee in enseignants :
        
        ee['_id']=str(ee['_id'])
        all_enseignants.append(ee)
    return all_enseignants
    
@user_router.delete("/user/{user_id}")
async def delete_user(user_id):
    result = db["users"].delete_one(dict(_id=ObjectId(user_id)))
    return {"message" :"user deleted"}

@user_router.get('/add_privilege/{user_id}/{privilege}')
async def get_all_enseignants(user_id,privilege):
    all_ens =[]
    user = db["users"].find_one({"_id":ObjectId(user_id)})

    if privilege == "directeurdepartement":
        enseignants = db["users"].find({"privilege": privilege, "departement": user['departement']})
        for ee in enseignants:
            all_ens.append(ee)
        if len(all_ens)==1:
            return {"message":"can add this privilege to tow users"}
        else:
            useprivileger = db["users"].update_one({"_id":ObjectId(user_id)},{
                "$set": {
                    "privilege":privilege}})
            return {"message":"privilege add sucessufly"}
    else:
        if privilege =="nonprivilege":
            useprivileger = db["users"].update_one({"_id":ObjectId(user_id)},{
                "$set": {
                    "privilege":""}})
        else:
            useprivileger = db["users"].update_one({"_id":ObjectId(user_id)},{
            "$set": {
                "privilege":privilege}})
        return {"message":"privilege add sucessufly"}


@user_router.post('/sancttion/{user_id}')
async def add_sanction(user_id,sanction : sanction):
    sanction.user_id =user_id
    db['sanction'].insert_one(dict(sanction))
    return {"message":"sanction interted sucessuflly !"}

@user_router.get('/sancttion/{user_id}')
async def get_sanction(user_id):
    all_sanctions =[]
    sanctions = db['sanction'].find({"user_id":user_id})
    for san in sanctions:
        san['_id']=str(san['_id'])
        all_sanctions.append(san)
    return all_sanctions