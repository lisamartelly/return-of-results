import unittest
from unittest.mock import patch, Mock
import crud
from model import connect_to_db, db, example_data
from server import app
from flask import session, json, render_template

####################     UNIT TESTS     ########################

# mocked db
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
        self.assertIn(b'<li class="detail-link list-page-item"><a name="participant" id=1 href="#"><div>First Participant</div></a></li>', result.data)

    def test_enroll_participant(self):
        """Test enrolling an existing participant"""

        result = self.client.post("/enroll",
                                  data={"existing": "yes", "participant_id": "1", "study_id": "2"},
                                  follow_redirects=True)
        self.assertIn(b"<h1> Result decisions -- second test study study </h1>", result.data)

    def test_add_result(self):
        """Test route adding a participant's result"""

        result = self.client.post("/create-result",
                                  data=json.dumps({"participantId":"1","results":[{"result_plan_id":"1","result_value":"TEST-43435-TEST-RESULT-VAL","urgent":"true"}]}),
                                  content_type='application/json',
                                  follow_redirects=True)

        self.assertIn(b"<td>TEST-43435-TEST-RESULT-VAL</td>", result.data)

class FlaskTestsLoggedInAsParticipant(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = "second_participant@test.com"
                sess['user_type'] = "participant"
                sess['user_id'] = 2

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

    def test_results_render(self):

        result = self.client.get("/participant/my-results")
        self.assertIn(b'URGENT NO RETURN - THIS SHOULD DISPLAY', result.data)
        self.assertIn(b'NON URGENT, RETURN DURING, CONSENTED - THIS SHOULD DISPLAY', result.data)
        self.assertNotIn(b'NO CONSENT NOT URGENT - THIS SHOULD NOT DISPLAY', result.data)
        self.assertNotIn(b'NON URGENT, RETURN AFTER - THIS SHOULD NOT DISPLAY', result.data)

if __name__ == "__main__":

    unittest.main()
