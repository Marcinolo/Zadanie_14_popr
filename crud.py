from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from .models import Contact, User
from .schemas import ContactCreate
from passlib.context import CryptContext
from jose import jwt, JWTError
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Funkcja do weryfikacji hasła
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Funkcja do generowania hasha hasła
def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return

    return User(email=email)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def register_user(email: str, password: str, db: Session):
    # Sprawdzenie, czy istnieje użytkownik o podanym adresie e-mail
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return None  # Jeśli użytkownik już istnieje, zwróć None

    # Utworzenie nowego użytkownika
    hashed_password = pwd_context.hash(password)
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user  # Zwróć nowego użytkownika


# Funkcja do weryfikacji adresu e-mail użytkownika
def verify_email(verification_token: str, db: Session):
    try:
        payload = jwt.decode(verification_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return {"message": "Invalid verification token"}

        # Znajdź użytkownika o podanym adresie e-mail w bazie danych
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return {"message": "User not found"}

        # Ustaw status weryfikacji użytkownika na True
        user.is_verified = True
        db.commit()

        return {"message": "Email verified successfully"}

    except jwt.JWTError:
        return {"message": "Invalid verification token"}

def get_contact(db_session: Session, contact_id: int):
    return db_session.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts(db_session: Session, search_query: str = None):
    if search_query:
        return db_session.query(Contact).filter(or_(
            Contact.first_name.ilike(f"%{search_query}%"),
            Contact.last_name.ilike(f"%{search_query}%"),
            Contact.email.ilike(f"%{search_query}%")
        )).all()
    else:
        return db_session

def create_contact(db_session: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db_session.add(db_contact)
    db_session.commit()
    db_session.refresh(db_contact)
    return db_contact

def update_contact(db_session: Session, contact_id: int, contact: ContactCreate):
    db_contact = get_contact(db_session, contact_id)
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db_session.commit()
    db_session.refresh(db_contact)
    return db_contact

def delete_contact(db_session: Session, contact_id: int):
    db_contact = get_contact(db_session, contact_id)
    db_session.delete(db_contact)
    db_session.commit()
    return {"message": "Contact deleted successfully"}

def get_contacts_upcoming_birthdays(db_session: Session):
    today = datetime.today()
    end_date = today + timedelta(days=7)
    return db_session.query(Contact).filter(
        (Contact.birth_date >= today) & (Contact.birth_date <= end_date)
    ).all()