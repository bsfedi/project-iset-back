
from bson import ObjectId
from fastapi import HTTPException
from database import db
import argon2


ph = argon2.PasswordHasher()


def signup(user):
    # Create a new dictionary to store the user data
    new_user = dict(user)

    # The collection is not empty, so we need to check if the user already exists and if the email domain matches an admin's domain
    if db["users"].find_one({"email": new_user["email"]}):
        raise HTTPException(status_code=409, detail="Email address already in use")
    
    # Insert the new user into the database
    response = db["users"].insert_one(new_user)
    preregister_id = db["preregistres"].insert_one({"user_id":response.inserted_id,"status":"NOTEXIST"})
    db["preregistres"].update_one({"_id":ObjectId(preregister_id.inserted_id)},{
                "$set": {
                    "personalInfo":{
                    "email":new_user["email"] }}})
    if response:
        return {
            "message": "User added successfully !",
            "user_id": response.inserted_id,
            "register_id": preregister_id.inserted_id
        }


def get_user_by_email(email):
    # Query the database to find a user by email
    user = db["users"].find_one(dict(email=email))
    # Return the user object if found, or None if not found
    return user


def get_all_users():
    user_list = []
    try:
        # Query to find users where role is not "student"

        
        # Iterate over users that match the query 
        for user in db["users"].find({"role": {"$nin": ["student","ADMIN"]}}):
            # Convert ObjectId to string
            user["_id"] = str(user["_id"]) 
            # Convert the bytes to a base64-encoded string using base64.b64encode
            user_list.append(user)  # Append user object to user_list

        return user_list  # Return the list of users
    except Exception as ex:
        return {
            "message": f"{str(ex)}"
        }  
    
def get_user_by_id(uid):
    # Retrieve a user from the database based on the given user ID (uid)
    user = db["users"].find_one(dict(_id=ObjectId(uid)))

    # If no user is found with the given user ID, raise an HTTPException with a 404 status code
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Return the user dictionary
    return user

def update_new_password(user_id, old_password, new_password):
    user = get_user_by_id(user_id)
    try:
        # Verify old password
        verify_password(user["password"], old_password)
        # Hash the new password
        hashed_password = ph.hash(new_password)
        # Update the password in the database
        update_password(user_id, hashed_password)
        return True
    except:
        # Raise an HTTPException with appropriate error message if old password is incorrect
        raise HTTPException(status_code=426, detail="Your old password is incorrect")
    
def update_password(user_id, password):
    response = db["users"].update_one(
        {"_id": ObjectId(user_id)}, {"$set": {"password": password}}
    )
    return response

def verify_password(hashed_password, password):
    try:
        # Verify if the provided password matches the hashed password
        if argon2.PasswordHasher().verify(hashed_password, password):
            # Return a message indicating that the password is correct
            return {"message": "Password is correct!"}
        else:
            # Raise an HTTPException with appropriate error message if password is invalid
            raise HTTPException(status_code=411, detail="Invalid password")
    except argon2.exceptions.VerifyMismatchError:
        # Raise an HTTPException with appropriate error message if password is incorrect
        raise HTTPException(status_code=412, detail="Incorrect password!")
    

