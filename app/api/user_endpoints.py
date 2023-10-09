import sqlite3
from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.auth import generate_token
from app.api.security import get_password_hash
from app.api.security import verify_password
from app.database.db_manager import get_user_by_username
from app.database.db_manager import insert_user, get_all_users, update_user_in_db, \
    delete_user_from_db
from app.models.token import Token
from app.models.user import User

router = APIRouter()

USER_NOT_FOUND = "User not found"


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail="Incorrect username or password"
        )
    token = generate_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
def register_user(user: User):
    return _create_user(user)


@router.post("/user")
def _create_user(user: User):
    hashed_password = get_password_hash(user.password)
    user_to_insert = User(username=user.username, email=user.email, password=hashed_password)
    try:
        insert_user(user_to_insert)
    except sqlite3.IntegrityError as e:  # Username or email already exists
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        ) from e
    return {"username": user.username, "email": user.email}


# Read single user by username
@router.get("/user/{username}", response_model=User)
def read_user(username: str):
    user = get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)
    return user


@router.get("/users", response_model=List[User])
def read_users():
    return get_all_users()


@router.put("/user/{username}")
def update_user(username: str, updated_user: User):
    user_in_db = get_user_by_username(username)
    if user_in_db is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)

    # Update user details here (you might need to create a function to handle the database update)
    update_user_in_db(updated_user)  # Assuming a function to update user in the database

    return {"message": "User updated successfully"}


@router.delete("/user/{username}")
def delete_user(username: str):
    user_in_db = get_user_by_username(username)
    if user_in_db is None:
        raise HTTPException(status_code=404, detail=USER_NOT_FOUND)

    # Delete the user from the database
    delete_user_from_db(username)  # Assuming a function to delete user from the database

    return {"message": "User deleted successfully"}
