"""Models for IRR app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ParticipantsStudies(db.Model):
    """Through table for participants and studies many to many setup"""

    __tablename__ = "participants_studies"

    participants_studies_id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id"), nullable=False)
    study_id = db.Column(db.Integer, db.ForeignKey("studies.study_id"), nullable=False)


class Participant(db.Model):
    """A study participant"""

    __tablename__ = "participants"

    participant_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    #personal info:
    #### REMINDER AFTER DEVELOPMENT TO CHANGE BACK TO UNIQUE EMAILS - UNIQUE = TRUE!!!!!
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    #hcp info:
    hcp_fullname = db.Column(db.String(100), nullable=True)
    hcp_phone = db.Column(db.String(30), nullable=True)
    hcp_email = db.Column(db.String, nullable=True)
    hcp_practice = db.Column(db.String, nullable=True)
    #relationships
    studies = db.relationship("Study", secondary="participants_studies", back_populates="participants")
    results = db.relationship("Result", back_populates="participant")
    

    def __repr__(self):
        return f'<Participant participant_id={self.participant_id} email={self.email} name={self.fname}>'

    def say_hello(self):
        return 'hello!!!'

class Study(db.Model):
    """ Research study"""

    __tablename__ = "studies"

    study_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    study_name = db.Column(db.String, nullable=True)
    investigational_product = db.Column(db.String, nullable=False)
    investigator_id = db.Column(db.Integer, db.ForeignKey("investigators.investigator_id"), nullable=False)
    # statuses: 1=planning 2=active 3=data locked 4=published
    status = db.Column(db.String, nullable=False)
    #relationships:
    participants = db.relationship("Participant", secondary="participants_studies", back_populates="studies")
    investigator = db.relationship("Investigator", back_populates="studies")
    result_plans = db.relationship("Result_Plan", back_populates="study")

    def __repr__(self):
        return f'<Study study_id={self.study_id} name={self.study_name}>'

class Investigator(db.Model):
    """ create a healthcare provider """
    
    __tablename__ = "investigators"

    #Investigator info:
    investigator_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    fname = db.Column(db.String(30), nullable=True)
    lname = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=True)

    studies = db.relationship("Study", back_populates="investigator")

    def __repr__(self):
        return f'<Investigator investigator_id={self.investigator_id} name={self.fname} {self.lname}>'

class Result_Plan(db.Model):
    """ Plan for whether to return a result"""
    __tablename__ = "result_plans"
    result_plan_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    study_id = db.Column(db.Integer, db.ForeignKey("studies.study_id"), nullable=False)
    result_category = db.Column(db.String, nullable=False)
    visit = db.Column(db.String, nullable=False)
    urgency_potential = db.Column(db.Boolean, nullable=False)
    return_plan = db.Column(db.Boolean, nullable=False)
    test_name = db.Column(db.String, nullable=False)
    return_timing = db.Column(db.String, nullable=True)

    study = db.relationship("Study", back_populates="result_plans")
    result = db.relationship("Result", back_populates="result_plan")


    def __repr__(self):
        return f'<Result Plan result_plan_id={self.result_plan_id} return_plan={self.return_plan} test_name={self.test_name}>'

class Result(db.Model):
    """ Record per result per participant with decision from participant to receive result or not"""
    __tablename__ = "results"

    result_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id"), nullable=False)
    result_plan_id = db.Column(db.Integer, db.ForeignKey("result_plans.result_plan_id"), nullable=False)
    receive_decision = db.Column(db.Boolean, nullable=True)
    urgent = db.Column(db.Boolean, nullable=True)
    result_value = db.Column(db.String, nullable=True)
    notified = db.Column(db.Boolean, nullable=True)

    result_plan = db.relationship("Result_Plan", back_populates="result")  
    participant = db.relationship("Participant", back_populates="results")

    def __repr__(self):
        return f'participant: {self.participant.participant_id}, result value: {self.result_value} result id: {self.result_id}'

def example_data():
    """example data created for testing"""

    # In case this is run more than once, empty out existing data
    Participant.query.delete()
    # Study.query.delete()
    # ParticipantsStudies.query.delete()

    # Add participants
    participant1 = Participant(email="first_participant@test.com", fname="First", lname="Participant", dob="01/01/1991", phone="111-1111", password="password")
    participant2 = Participant(email="second_participant@test.com", fname="Second", lname="Participant", dob="02/02/1992", phone="222-2222", password="password")
    db.session.add_all([participant1, participant2])

    # # Add one investigator
    # investigator = Investigator(fname="Only", lname="Investigator", email="investigator@test.com", phone="333-3333")
    # db.session.add(investigator)

    # # Add two studies
    # study1 = Study(investigator_id=1, study_name="first test study", investigational_product="XYZ 123", status="planning")
    # study2 = Study(investigator_id=1, study_name="second test study", investigational_product="ABC 456", status="planning")
    # db.session.add_all([study1, study2])

    # # Add result plans for 2 results in each study
    # result_plan1_1 = Result_Plan(study_id=1, result_category="actionable", visit="recruitment", urgency_potential=True, return_plan=True, test_name="fake first test", return_timing="after")
    # result_plan1_2 = Result_Plan(study_id=1, result_category="unknown", visit="consent", urgency_potential=False, return_plan=False, test_name="fake second test", return_timing="not applicable")
    # result_plan2_1 = Result_Plan(study_id=2, result_category="personally valuable", visit="study-visit-1", urgency_potential=False, return_plan=True, test_name="fake third test", return_timing="during")
    # result_plan2_2 = Result_Plan(study_id=2, result_category="unknwon", visit="study-visit-2", urgency_potential=False, return_plan=False, test_name="fake fourth test", return_timing="not applicable")
    # db.session.add_all([result_plan1_1, result_plan1_2, result_plan2_1, result_plan2_2])

    # # Add result shells and participant decisions
    # result1 = Result(participant_id=1, result_plan_id=1, receive_decision=True)
    # result2 = Result(participant_id=1, result_plan_id=2, receive_decision=None)
    # result3 = Result(participant_id=2, result_plan_id=3, receive_decision=False)
    # result4 = Result(participant_id=2, result_plan_id=4, receive_decision=None)
    # db.session.add_all([result1, result2, result3, result4])

    # # Enroll first participant in first study and second participant in second study
    # ps1 = ParticipantsStudies(participant_id=1, study_id=1)
    # ps2 = ParticipantsStudies(participant_id=2, study_id=2)
    # db.session.add_all([ps1, ps2])
    
    # db.session.add_all([participant1, participant2, investigator, study1, study2, ps1, ps2, 
    #     result_plan1_1, result_plan1_2, result_plan2_1, result_plan2_2, result1, result2, result3, result4])

    db.session.commit()


def connect_to_db(flask_app, db_uri="postgresql:///irr", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, echo=False)