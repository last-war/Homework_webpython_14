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
    """
    get all notes

    :param cur_user: current user - note owner
    :type cur_user: User
    :param db: current session to db
    :type db: Session
    :return: all notes in database for current user
    :rtype: List
    """
    notes = await repository_notes.get_all(cur_user, db)
    return notes


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create(body: NoteModel, cur_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """
    create new note by db id

    :param body: all need field to create
    :type body: NoteModel
    :param cur_user: current user - note owner
    :type cur_user: User
    :param db: current session to db
    :type db: Session
    :return: Note | None
    :rtype: Note | None
    """
    note = await repository_notes.create(body, cur_user, db)
    return note


@router.get("/{note_id}", response_model=NoteResponse)
async def get_one(note_id: int = Path(ge=1), cur_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """
    get note by db id

    :param note_id: id to find
    :type note_id: int
    :param cur_user: current user - note owner
    :type cur_user: User
    :param db: current session to db
    :type db: Session
    :return: Note | None
    :rtype: Note | None
    """
    note = await repository_notes.get_one(note_id, cur_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return note


@router.put("/{note_id}", response_model=NoteResponse)
async def update(body: NoteModel, note_id: int = Path(ge=1), cur_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """
    update note by db id

    :param body: all need field to update
    :type body: NoteModel
    :param note_id: id to find
    :type note_id: int
    :param cur_user: current user - note owner
    :type cur_user: User
    :param db: current session to db
    :type db: Session
    :return: Note | None
    :rtype: Note | None
    """
    note = await repository_notes.update(note_id, body, cur_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(note_id: int = Path(ge=1), cur_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """
    detele note finded by db id

    :param note_id: id to find
    :type note_id: int
    :param cur_user: current user - note owner
    :type cur_user: User
    :param db: current session to db
    :type db: Session
    :return: Note | None
    :rtype: Note | None
    """
    note = await repository_notes.delete(note_id, cur_user, db)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return note

