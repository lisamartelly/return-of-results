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
    return_decisions = db.relationship("Return_Decision", back_populates="participant")
    results = db.relationship("Result", backref="participant")

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
    return_decision = db.relationship("Return_Decision", back_populates="result_plan")   
    result = db.relationship("Result", back_populates="result_plan")


    def __repr__(self):
        return f'<Result Plan result_plan_id={self.result_plan_id} return_plan={self.return_plan} test_name={self.test_name}'

class Return_Decision(db.Model):
    """ Decision from participant to receive result or not"""
    __tablename__ = "return_decisions"
    return_decision_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id"), nullable=False)
    result_plan_id = db.Column(db.Integer, db.ForeignKey("result_plans.result_plan_id"), nullable=False)
    return_decision = db.Column(db.Boolean, nullable=True)

    result_plan = db.relationship("Result_Plan", back_populates="return_decision")  
    participant = db.relationship("Participant", back_populates="return_decisions")

    def __repr__(self):
        return f'<Return Decision return_decision_id={self.return_decision_id} result_plan_id={self.result_plan_id} return_decision={self.return_decision}'

class Result(db.Model):
    """an individual test result"""
    __tablename__ ="results"
    result_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
   
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id"), nullable=False)
    result_plan_id = db.Column(db.Integer, db.ForeignKey("result_plans.result_plan_id"), nullable=False)
    urgent = db.Column(db.Boolean, nullable=False)
    result_value = db.Column(db.String, nullable=True)
    notified = db.Column(db.Boolean, nullable=True)

    # "participant" backrefs here for all results of a participant
    result_plan = db.relationship("Result_Plan", back_populates="result")

    def __repr__(self):
        return f'participant: {self.participant.participant_id}, result value: {self.result_value} result id: {self.result_id}'

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

    connect_to_db(app)