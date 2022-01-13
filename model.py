"""Models for IRR app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Participant(db.Model):
    """A study participant"""

    __tablename__ = "participants"

    participant_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    #personal info:
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=True)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    study_id = db.Column(db.Integer, db.ForeignKey("studies.study_id"), nullable=False)

    #hcp info:
    hcp_fname = db.Column(db.String(30), nullable=True)
    hcp_lname = db.Column(db.String(30), nullable=True)
    hcp_phone = db.Column(db.String(30), nullable=True)
    hcp_email = db.Column(db.String, nullable=True)
    hcp_practice = db.Column(db.String, nullable=True)

    #relationships
    studies = db.relationship("Study", secondary="participants_studies", back_populates="participants")
    return_decisions = db.relationship("Return_Decision", back_populates="participants")

    def __repr__(self):
        return f'<Participant participant_id={self.user_id} email={self.email} name={self.fname}>'

class Investigator(db.Model):
    """ create a healthcare provider """
    __tablename__ = "investigators"

    #Investigator info:
    investigator_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    fname = db.Column(db.String(30), nullable=True)
    lname = db.Column(db.String(30), nullable=True)
    phone = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String, nullable=True)

    studies = db.relationship("Study", back_populates="investigators")


    def __repr__(self):
        return f'<Investigator investigator_id={self.investigator_id} name={self.fname} {self.lname}>'

class Study(db.Model):
    """ Research study"""

    __tablename__ = "studies"

    study_id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    study_name = db.Column(db.String, nullable=True)
    investigational_product = db.Column(db.String, nullable=False)
    investigator_id = db.Column(db.Integer, db.ForeignKey("investigators.investigator_id"), nullable=False)

    # status codes: 1=planning 2=active 3=data locked 4=published
    status_code = db.Column(db.Integer, nullable=False)

    #relationships:
    participants = db.relationship("Participant", secondary="participants_studies", back_populates="studies")
    investigators = db.relationship("Investigator", back_populates="studies")
    result_plans = db.relationship("Result_Plan", back_populates="studies")

    def __repr__(self):
        return f'<Study study_id={self.study_id} name={self.name} investigator={self.investigator.fname} {self.investigator.lname}>'

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

    studies = db.relationship("Study", back_populates="result_plans")

    def __repr__(self):
        return f'<Result Plan result_plan_id={self.result_plan_id} return_plan={self.return_plan} test_name={self.test_name}'

class Return_Decision(db.Model):
    """ Decision from participant to receive result or not"""
    __tablename__ = "return_decisions"
    return_decision_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id"), nullable=False)
    result_plan_id = db.Column(db.Integer, db.ForeignKey("result_plans.result_plan_id"), nullable=False)
    return_decision = db.Column(db.Boolean, nullable=False)
    
    participants = db.relationship("Participant", back_populates="return_decisions")

    def __repr__(self):
        return f'<Return Decision return_decision_id={self.return_decision_id} result_plan_id={self.result_plan_id} return_decision={self.return_decision}'

class ParticipantsStudies(db.Model):
    """Studies that a participant is enrolled in"""

    __tablename__ = "participants_studies"

    participants_studies_id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("participants.participant_id"), nullable=False)
    study_id = db.Column(db.Integer, db.ForeignKey("studies.study_id"), nullable=False)


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