import unittest
import crud
from unittest.mock import patch

@patch('crud.db')
def test_create_participant(db_mock):
    crud.create_participant(email="123@123.com",
    fname="Lisa",
    lname="Murray",
    dob="01/02/1993",
    phone="1234567890")
    
    db_mock.session.add.assert_called_once()
    db_mock.session.commit.assert_called_once()
    