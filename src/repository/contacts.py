from src.database.models import Contact, User
from src.schemas import ContactModel
from sqlalchemy.orm import Session
from datetime import date, datetime
from sqlalchemy import and_


async def create(body: ContactModel, user: User, db: Session):
    """
    Create a new contact

    :param body: all parameters for new contact
    :type body: ContactModel
    :param user: current user - contact owner 
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: Contact
    :rtype: Contact
    """
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def get_all(skip: int, limit: int, user: User, db: Session):
    """
    info

    :param user: current user - contact owner 
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: 
    :rtype: List
    """
    contacts = db.query(Contact).offset(skip).limit(limit).filter(Contact.user_id == user.id).all()
    return contacts


async def get_one(contact_id, user: User, db: Session):
    """
    info

    :param user: current user - contact owner 
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: 
    :rtype: Contact
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, id=contact_id)).first()
    return contact


async def update(contact_id, body: ContactModel, user: User, db: Session):
    """
    info

    :param user: current user - contact owner 
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: 
    :rtype: Contact
    """
    contact = await get_one(contact_id, user, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.birthday = body.birthday
        db.commit()
    return contact


async def delete(contact_id, user: User, db: Session):
    """
    info

    :param user: current user - contact owner 
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: 
    :rtype: Contact
    """
    contact = await get_one(contact_id, user, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def find_by_name(contact_name, user: User, db: Session):
    """
    info

    :param user: current user - contact owner 
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: 
    :rtype: Contact
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, first_name=contact_name)).first()
    return contact


async def find_by_lastname(lastname, user: User, db: Session):
    """
    info

    :param user: current user - contact owner 
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: 
    :rtype: Contact
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, last_name=lastname)).first()
    return contact


async def find_by_email(email, user: User, db: Session):
    """
    info

    :param user: current user - contact owner 
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: 
    :rtype: Contact
    """
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, email=email)).first()
    return contact


async def find_birthday7day(user: User, db: Session):
    """
    contact with birthday next 7 days

    :param user: current user - contact owner 
    :type user: User
    :param db: current session to db
    :type db: Session
    :return: contact with birthday next 7 days 
    :rtype: List
    """
    contacts = []
    db_contacts = await get_all(user, db)
    today = date.today()
    for db_contact in db_contacts:
        birthday = db_contact.birthday
        shift = (datetime(today.year, birthday.month, birthday.day).date() - today).days
        if shift < 0:
            shift = (datetime(today.year + 1, birthday.month, birthday.day).date() - today).days
        if shift <= 7:
            contacts.append(db_contact)
    return contacts