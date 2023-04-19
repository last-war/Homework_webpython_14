from src.schemas import UserModel
from src.database.models import User
from sqlalchemy.orm import Session


async def get_user_by_email(email: str, db: Session) -> User:
    """
    Get user by email

    :param email: user's email in db
    :type email: str
    :param db: current session to db
    :type db: Session
    :return: User
    :rtype: User
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Create a new user

    :param body: all field for new user
    :type body: UserModel
    :param db: current session to db
    :type db: Session
    :return: User
    :rtype: User
    """
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def confirmed_email(email: str, db: Session) -> None:
    """
    Set confirmed field for user in db

    :param email: user's email in db
    :type email: str
    :param db: current session to db
    :type db: Session
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
