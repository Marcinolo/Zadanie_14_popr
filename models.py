from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    """
        Model użytkownika.

        Attributes:
            id (int): ID użytkownika.
            email (str): Adres e-mail użytkownika.
            hashed_password (str): Zahaszowane hasło użytkownika.
            is_email_verified (bool): Flaga wskazująca, czy adres e-mail został zweryfikowany.
        """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_email_verified = Column(Boolean, default=False)

class Contact(Base):
    """
        Model kontaktu.

        Attributes:
            id (int): ID kontaktu.
            first_name (str): Imię kontaktu.
            last_name (str): Nazwisko kontaktu.
            email (str): Adres e-mail kontaktu.
            phone_number (str): Numer telefonu kontaktu.
            birth_date (datetime.date): Data urodzenia kontaktu.
            extra_data (str, optional): Dodatkowe dane kontaktu.
        """

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, index=True)
    birth_date = Column(Date)
    extra_data = Column(String, nullable=True)