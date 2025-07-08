from sqlalchemy.orm import Session
from models.user import User
from schemas.user import SignUp, Login
from utils import helpers
from fastapi import HTTPException

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def sign_up(db: Session, user: SignUp):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = helpers.hash_password(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "Sign up successful", "Status" : True}

def login(db: Session, user: Login):
    user_db = get_user_by_email(db, user.email)
    if not user_db:
        raise HTTPException(status_code=400, detail="Invalid email")
    
    if not helpers.verify_password(user.password, user_db.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token = helpers.create_access_token(data={
        "id": user_db.id,
        "name": user_db.name,
        "email": user_db.email,
        "is_active": user_db.is_active,
    })

    return {"access_token": access_token, "message" : "Login successful", "Status" : True}

# def update_user(db: Session, user_id: int, user_update: UserUpdate):
#     db_user = get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     update_data = user_update.dict(exclude_unset=True)
#     if "password" in update_data:
#         update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
#     for key, value in update_data.items():
#         setattr(db_user, key, value)
    
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# def delete_user(db: Session, user_id: int):
#     db_user = get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     db.delete(db_user)
#     db.commit()
#     return db_user
