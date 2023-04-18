from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Path

from src.database.models import User
from src.repository import notes as repository_notes
from src.schemas import NoteResponse, NoteModel
from sqlalchemy.orm import Session
from src.database.connector import get_db
from src.services.auth import auth_service as auth

router = APIRouter(prefix='/note', tags=['note'])


@router.get("/", response_model=List[NoteResponse])
async def get_all(cur_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    notes = await repository_notes.get_all(cur_user, db)
    return notes


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create(body: NoteModel, cur_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    note = await repository_notes.create(body, cur_user, db)
    return note


@router.get("/{contact_id}", response_model=NoteResponse)
async def get_one(contact_id: int = Path(ge=1), cur_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    note = await repository_notes.get_one(contact_id, cur_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return note


@router.put("/{contact_id}", response_model=NoteResponse)
async def update(body: NoteModel, contact_id: int = Path(ge=1), cur_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    note = await repository_notes.update(contact_id, body, cur_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return note


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(contact_id: int = Path(ge=1), cur_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    note = await repository_notes.delete(contact_id, cur_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return note

