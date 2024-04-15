from fastapi import HTTPException, Depends, status
from .schemas import ContactCreate, ContactOut, Token
from .crud import (
    create_contact,
    get_contacts,
    get_contact,
    update_contact,
    delete_contact,
    get_contacts_upcoming_birthdays,
    authenticate_user,
    create_access_token,
    register_user,
    verify_email,
)
from .models import SessionLocal, User
from sqlalchemy.orm import Session

@app.post("/contacts/", response_model=ContactOut)
def create_new_contact(
    contact: ContactCreate,
    db_session: Session = Depends(SessionLocal),
    current_user: User = Depends(get_current_user),
):
    """
    Tworzy nowy kontakt.

    Args:
        contact (ContactCreate): Dane kontaktowe nowego kontaktu.
        db_session (Session, optional): Sesja bazy danych. Domyślnie: SessionLocal.
        current_user (User, optional): Zalogowany użytkownik. Domyślnie: Depends(get_current_user).

    Returns:
        ContactOut: Utworzony kontakt.
    """
    return create_contact(db_session, contact)

@app.get("/contacts/", response_model=list[ContactOut])
def read_all_contacts(
    search_query: str = None,
    db_session: Session = Depends(SessionLocal),
    current_user: User = Depends(get_current_user),
):
    """
    Pobiera wszystkie kontakty.

    Args:
        search_query (str, optional): Zapytanie wyszukiwania. Domyślnie: None.
        db_session (Session, optional): Sesja bazy danych. Domyślnie: SessionLocal.
        current_user (User, optional): Zalogowany użytkownik. Domyślnie: Depends(get_current_user).

    Returns:
        list[ContactOut]: Lista kontaktów.
    """
    return get_contacts(db_session, search_query)

@app.get("/contacts/{contact_id}", response_model=ContactOut)
def read_contact(
    contact_id: int,
    db_session: Session = Depends(SessionLocal),
    current_user: User = Depends(get_current_user),
):
    """
    Pobiera pojedynczy kontakt.

    Args:
        contact_id (int): ID kontaktu.
        db_session (Session, optional): Sesja bazy danych. Domyślnie: SessionLocal.
        current_user (User, optional): Zalogowany użytkownik. Domyślnie: Depends(get_current_user).

    Returns:
        ContactOut: Kontakt o podanym ID.
    """
    return get_contact(db_session, contact_id)

@app.put("/contacts/{contact_id}", response_model=ContactOut)
def update_existing_contact(
    contact_id: int,
    contact: ContactCreate,
    db_session: Session = Depends(SessionLocal),
    current_user: User = Depends(get_current_user),
):
    """
    Aktualizuje istniejący kontakt.

    Args:
        contact_id (int): ID kontaktu do aktualizacji.
        contact (ContactCreate): Nowe dane kontaktowe.
        db_session (Session, optional): Sesja bazy danych. Domyślnie: SessionLocal.
        current_user (User, optional): Zalogowany użytkownik. Domyślnie: Depends(get_current_user).

    Returns:
        ContactOut: Zaktualizowany kontakt.
    """
    return update_contact(db_session, contact_id, contact)

@app.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_contact(
    contact_id: int,
    db_session: Session = Depends(SessionLocal),
    current_user: User = Depends(get_current_user),
):
    """
    Usuwa istniejący kontakt.

    Args:
        contact_id (int): ID kontaktu do usunięcia.
        db_session (Session, optional): Sesja bazy danych. Domyślnie: SessionLocal.
        current_user (User, optional): Zalogowany użytkownik. Domyślnie: Depends(get_current_user).

    Returns:
        HTTPResponse: Kod statusu 204 No Content.
    """
    return delete_contact(db_session, contact_id)

@app.get("/contacts/upcoming_birthdays", response_model=list[ContactOut])
def get_upcoming_birthdays(
    db_session: Session = Depends(SessionLocal),
    current_user: User = Depends(get_current_user),
):
    """
    Pobiera nadchodzące urodziny kontaktów.

    Args:
        db_session (Session, optional): Sesja bazy danych. Domyślnie: SessionLocal.
        current_user (User, optional): Zalogowany użytkownik. Domyślnie: Depends(get_current_user).

    Returns:
        list[ContactOut]: Lista kontaktów z nadchodzącymi urodzinami.
    """
    return get_contacts_upcoming_birthdays(db_session)

@app.post("/login", response_model=Token)
def login_for_access_token(email: str, password: str, db_session=SessionLocal()):
    """
    Loguje użytkownika i zwraca token dostępu.

    Args:
        email (str): Adres e-mail użytkownika.
        password (str): Hasło użytkownika.
        db_session (Session, optional): Sesja bazy danych. Domyślnie: SessionLocal.

    Returns:
        dict: Zwraca słownik zawierający token dostępu i typ tokenu.

    Raises:
        HTTPException: Zwraca HTTPException z kodem 401 UNAUTHORIZED, jeśli podano niepoprawny adres e-mail lub hasło.
    """
    user = authenticate_user(email, password, db_session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register", response_model=Token)
def register_new_user(email: str, password: str, db_session=SessionLocal()):
    """
    Rejestruje nowego użytkownika i zwraca token dostępu.

    Args:
        email (str): Adres e-mail nowego użytkownika.
        password (str): Hasło nowego użytkownika.
        db_session (Session, optional): Sesja bazy danych. Domyślnie: SessionLocal.

    Returns:
        dict: Zwraca słownik zawierający token dostępu i typ tokenu.

    Raises:
        HTTPException: Zwraca HTTPException z kodem 400 BAD REQUEST, jeśli użytkownik o podanym adresie e-mail już istnieje.
    """
    user = register_user(email, password, db_session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    access_token = create_access_token(data={"sub": email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/verify-email/{verification_token}")
def verify_user_email(
    verification_token: str, db_session=SessionLocal(), current_user: User = Depends(get_current_user)
):
    """
    Weryfikuje adres e-mail użytkownika na podstawie tokena weryfikacyjnego.

    Args:
        verification_token (str): Token weryfikacyjny adresu e-mail.
        db_session (Session, optional): Sesja bazy danych. Domyślnie: SessionLocal.
        current_user (User, optional): Zalogowany użytkownik. Domyślnie: Depends(get_current_user).

    Returns:
        dict: Zwraca komunikat potwierdzający weryfikację adresu e-mail.

    Raises:
        HTTPException: Zwraca HTTPException z kodem 401 UNAUTHORIZED, jeśli podano niepoprawny token weryfikacyjny.
    """
    return verify_email(verification_token, db_session)