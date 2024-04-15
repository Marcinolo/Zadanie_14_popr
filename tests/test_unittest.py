import unittest
from unittest.mock import MagicMock
from crud import (
    authenticate_user,
    create_access_token,
    register_user,
    verify_email,
    get_password_hash,
    verify_password,
)
from models import User

class TestCRUDFunctions(unittest.TestCase):
    def setUp(self):
        self.db_session = MagicMock()
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "hashed_password": get_password_hash("testpassword"),
            "is_verified": False
        }
        self.user = User(**self.user_data)

    def test_authenticate_user(self):
        token = create_access_token({"sub": self.user_data["email"]})
        authenticated_user = authenticate_user(token)
        self.assertEqual(authenticated_user.email, self.user_data["email"])

    def test_create_access_token(self):
        token = create_access_token({"sub": self.user_data["email"]})
        self.assertTrue(token)

    def test_register_user(self):
        register_user(self.user_data["email"], self.user_data["password"], self.db_session)
        self.db_session.add.assert_called_once_with(self.user)

    def test_verify_email(self):
        token = create_access_token({"sub": self.user_data["email"]})
        verify_email(token, self.db_session)
        self.db_session.query(User).filter.assert_called_once_with(User.email == self.user_data["email"])
        self.assertTrue(self.user.is_verified)

    def test_get_password_hash(self):
        hashed_password = get_password_hash(self.user_data["password"])
        self.assertTrue(hashed_password)

    def test_verify_password(self):
        self.assertTrue(verify_password(self.user_data["password"], self.user_data["hashed_password"]))
        self.assertFalse(verify_password("incorrectpassword", self.user_data["hashed_password"]))

if __name__ == "__main__":
    unittest.main()