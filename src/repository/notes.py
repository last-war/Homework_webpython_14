from src.database.models import Note, User
from src.schemas import NoteModel
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List


async def create(body: NoteModel, user: User, db: Session):
    """
    Create a new note

    :param body: all parameters for new note
    :type body: NoteModel
    :param user: current user - contact owner
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: Note | None
    :rtype: Note | None
    """
    note = Note(**body.dict(), user_id=user.id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


async def get_all(user: User, db: Session) -> List[Note]:
    """
    get notes from current user

    :param user: current user - contact owner
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: Note
    :rtype: List
    """
    return db.query(Note).filter(Note.user_id == user.id).all()


async def get_one(note_id, user: User, db: Session):
    """
    get note by db id

    :param note_id: id to find
    :type note_id: int
    :param user: current user - contact owner
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: Note | None
    :rtype: Note | None
    """
    note = db.query(Note).filter(and_(Note.user_id == user.id, id == note_id)).first()
    return note


async def update(note_id, body: NoteModel, user: User, db: Session):
    """
    Update note, find by db id

    :param note_id: id to find
    :type note_id: int
    :param body: all new parameters for note update
    :type body: NoteModel
    :param user: current user - contact owner
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: Note | None
    :rtype: Note | None
    """
    note = await get_one(note_id, user, db)
    if note:
        note.text = body.text
        db.commit()
    return note


async def delete(note_id, user: User, db: Session):
    """
    delete note find note by db id

    :param note_id: id to find
    :type note_id: int
    :param user: current user - contact owner
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: Note | None
    :rtype: Note | None
    """
    note = await get_one(note_id, user, db)
    if note:
        db.delete(note)
        db.commit()
    return note

