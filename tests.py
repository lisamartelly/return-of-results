import unittest
from unittest.mock import patch
import crud
from model import connect_to_db, db, example_data
from server import app
from flask import session

####################     UNIT TESTS     ########################

# mocked 'unit test'
@patch('crud.db')
def test_create_participant(db_mock):
    crud.create_participant(email="123@123.com",
    fname="Lisa",
    lname="Murray",
    dob="01/02/1993",
    phone="1234567890")
    
    db_mock.session.add.assert_called_once()
    db_mock.session.commit.assert_called_once()


####################  INTEGRATION TESTS  ##################

# basic route tests
class FlaskTestsBasic(unittest.TestCase):
    """Flask tests."""

    def setUp(self):
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_login_display(self):
        """Test login page displays"""

        result = self.client.get("/")
        self.assertIn(b"register or login", result.data)
        self.assertNotIn(b"Homepage", result.data)
       

    def test_redirect_if_not_logged_in(self):
        """Test that you're redirected to login if not logged in"""

        result = self.client.get("/participants", follow_redirects=True)
        self.assertIn(b"register or login", result.data)
        self.assertNotIn(b"Homepage", result.data)


# test db
class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login_function(self):
        """Test login page."""

        result = self.client.post("/login",
                                  data={"email": "investigator@test.com", "password": "password", "user_type": "investigator"},
                                  follow_redirects=True)
        self.assertIn(b"Homepage", result.data)

class FlaskTestsLoggedInAsInvestigator(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = "investigator@test.com"
                sess['user_type'] = "investigator"
                sess['user_id'] = 1

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_participants_list(self):
        """Test participants page when logged in as investigator."""

        result = self.client.get("/participants")
        self.assertIn(b'<li class="detail-link"><a name="participant" id=1 href="#">First Participant</a></li>', result.data)



# class FlaskTestsLoggedOut(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_important_page(self):
#         """Test that user can't see important page when logged out."""

#         result = self.client.get("/important", follow_redirects=True)
#         self.assertNotIn(b"You are a valued user", result.data)
#         self.assertIn(b"You must be logged in", result.data)




if __name__ == "__main__":
    import unittest

    unittest.main()
