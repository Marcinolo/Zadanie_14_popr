from pydantic import BaseModel

class ContactCreate(BaseModel):
    """
       Model danych do tworzenia nowego kontaktu.

       Attributes:
           first_name (str): Imię kontaktu.
           last_name (str): Nazwisko kontaktu.
           email (str): Adres e-mail kontaktu.
           phone_number (str): Numer telefonu kontaktu.
           birth_date (str): Data urodzenia kontaktu w formacie 'YYYY-MM-DD'.
           extra_data (str, optional): Dodatkowe dane kontaktu.
       """

    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: str
    extra_data: str = None

class ContactOut(ContactCreate):
    """
        Model danych kontaktu z ID.

        Attributes:
            id (int): ID kontaktu.
        """

    id: int

class Token(BaseModel):
    """
       Model tokena dostępu.

       Attributes:
           access_token (str): Token dostępu.
           token_type (str): Typ tokenu.
       """

    access_token: str
    token_type: str