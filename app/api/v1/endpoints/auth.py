from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers import user as crud_user
from schemas.user import UserInDB, SignUp
# from app.dependencies.auth import get_current_user
from databases.db import get_db

router = APIRouter()

@router.post("/", response_model=UserInDB)
async def sign_up(user: SignUp, db: Session = Depends(get_db)):
    return crud_user.sign_up(db, user)

# @router.get("/{user_id}", response_model=UserInDB)
# async def read_user(user_id: int, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
#     db_user = crud_user.get_user(db, user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user

# @router.get("/", response_model=List[UserInDB])
# async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
#     return crud_user.get_users(db, skip, limit)

# @router.put("/{user_id}", response_model=UserInDB)
# async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
#     return crud_user.update_user(db, user_id, user)

# @router.delete("/{user_id}")
# async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
#     return crud_user.delete_user(db, user_id)
