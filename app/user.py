from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix='/users',
    tags=['users']
)

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class User(UserBase):
    id: int

users: Dict[int, User] = {}
next_id = 1

@router.get('/', response_model=List[User])
def get_users():
    return list(users.values())

@router.get('/{user_id}', response_model=User)
def get_user(user_id: int):
    user = users.get(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user

@router.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate):
    global next_id
    user = User(id=next_id, **user_create.dict())
    users[next_id] = user
    next_id += 1
    return user

@router.put('/{user_id}', response_model=User)
def update_user(user_id: int, user_update: UserUpdate):
    existing_user = users.get(user_id)
    if existing_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    updated_data = user_update.dict(exclude_unset=True)
    updated_user = existing_user.copy(update=updated_data)
    users[user_id] = updated_user
    return updated_user

@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    del users[user_id]
    return None