"""CRUD operations."""

from model import db, Participant, Study, Investigator, Result_Plan, ParticipantsStudies, Return_Decision, connect_to_db

# CREATIONS

def create_participant(email, fname, lname, dob, phone):
    """Create and return a new user."""

    participant = Participant(email=email, fname=fname, lname=lname, dob=dob, phone=phone)

    db.session.add(participant)
    db.session.commit()

    return participant

def create_investigator(fname, lname, phone, email):
    """Create and return a new user."""

    investigator = Investigator(fname=fname, lname=lname, email=email, phone=phone)

    db.session.add(investigator)
    db.session.commit()

    return investigator

def create_study(investigator_id, study_name, investigational_product, status_code):
    """Create and return a new study."""

    study = Study(
        investigator_id=investigator_id,
        study_name=study_name,
        investigational_product=investigational_product,
        status_code=status_code
        )

    db.session.add(study)
    db.session.commit()

    return study

def create_participantsstudies_link(participant_id, study_id):
    """Create and return a new study."""

    ps = ParticipantsStudies(
        participant_id=participant_id,
        study_id=study_id
    )

    db.session.add(ps)
    db.session.commit()

    return ps

def create_result_plan(study_id, result_category, visit, urgency_potential, return_plan, test_name, return_timing):
    """Create and return a new study."""

    result_plan = Result_Plan(
        study_id=study_id,
        result_category=result_category,
        visit=visit,
        urgency_potential=urgency_potential,
        return_plan=return_plan,
        test_name=test_name,
        return_timing=return_timing
        )

    db.session.add(result_plan)
    db.session.commit()

    return result_plan

def create_result_decision(participant_id, result_plan_id, return_decision):
    """Create and return a new study."""

    rd = Return_Decision(
        participant_id=participant_id,
        result_plan_id=result_plan_id,
        return_decision=return_decision
    )

    db.session.add(rd)
    db.session.commit()

    return rd

# RETURN ALLS

def return_all_studies():
    """Return all studies"""
    return Study.query.all()

def return_all_investigators():
    """Return all studies"""
    return Investigator.query.all()

def return_all_participants():
    """Return all participants"""
    return Participant.query.all()

# GET ITEMS

def get_study_by_id(study_id):
    """Return study based on study id"""

    return Study.query.get(study_id)

def get_participant_by_id(participant_id):
    """Return participant from participant id"""

    return Participant.query.get(participant_id)

def get_rd_by_rp_by_participant(participant_id, result):
    """ return a participantsstudies link if a participant is already connected to a study"""

    return Return_Decision.query.filter_by(result_plan_id = result.result_plan_id, participant_id = participant_id).all()

def get_participant_by_email(email):
    
    return Participant.query.filter(Participant.email == email).first()

def get_investigator_by_email(email):
    
    return Investigator.query.filter(Investigator.email == email).first()

# UPDATES

def update_return_decision(participant_id, result, return_decision):
    """Update rating"""
    # rd = get_rd_by_rp_by_participant(participant_id, result)
    # rd.update({"return_decision": return_decision})
    Return_Decision.query.filter_by(result_plan_id = result.result_plan_id, participant_id = participant_id).update({"return_decision": return_decision})
    db.session.commit()

def add_password(user_type, email, password):
    """ add password to existing record of certain email"""

    if user_type== "investigator":
        Investigator.query.filter_by(email = email).update({"password": password})
    elif user_type== "participant":
        Participant.query.filter_by(email = email).update({"password": password})
    db.session.commit()

def update_participant_hcp(participant_id, email, fname, lname, practice, phone):
    """add healthcare provider info to participant"""

    Participant.query.filter_by(participant_id = participant_id).update(
        {"hcp_fname": fname,
        "hcp_lname": lname,
        "hcp_email": email,
        "hcp_phone": phone,
        "hcp_practice": practice}
    )
    db.session.commit()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)