import unittest

from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, Note, User
from src.schemas import ContactModel
from src.repository.contacts import (
    create,
    get_all,
    get_one,
    update,
    delete,
    find_by_name,
    find_by_lastname,
    find_by_email,
    find_by_lastname,
    find_birthday7day,
)
import datetime


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_create(self):
        body = ContactModel(first_name="test", last_name="last", email="test@email.com", phone="234-345-2343",
                            birthday=datetime.datetime.now())
        result = await create(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertTrue(hasattr(result, "id"))
"""
    get_all,
    get_one,
    update,
    delete,
    find_by_name,
    find_by_lastname,
    find_by_email,
    find_by_lastname,
    find_birthday7day,
"""


if __name__ == '__main__':
    unittest.main()
