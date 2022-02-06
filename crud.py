"""CRUD operations."""

from model import db, Participant, Study, Investigator, Result_Plan, ParticipantsStudies, Result, connect_to_db

# CREATIONS

def create_participant(email, fname, lname, dob, phone):
    """Create and return a new user."""

    participant = Participant(email=email.lower(), fname=fname, lname=lname, dob=dob, phone=phone)

    db.session.add(participant)
    db.session.commit()

    return participant

def create_investigator(fname, lname, phone, email):
    """Create and return a new investigator."""

    investigator = Investigator(fname=fname, lname=lname, email=email.lower(), phone=phone)

    db.session.add(investigator)
    db.session.commit()

    return investigator

def create_study(investigator_id, study_name, investigational_product, status):
    """Create and return a new study."""

    study = Study(
        investigator_id=investigator_id,
        study_name=study_name,
        investigational_product=investigational_product,
        status=status
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

def create_result(participant_id, result_plan_id, receive_decision):
    """Create and return a shell for forthcoming result and preconceived decision to receive it from participant"""

    result = Result(
        participant_id=participant_id,
        result_plan_id=result_plan_id,
        receive_decision=receive_decision
    )

    db.session.add(result)
    db.session.commit()

    return result

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

def return_all_study_participant_ids(study_id):
    """ return all participant IDs of a given study"""
    return ParticipantsStudies.query.filter(ParticipantsStudies.study_id == study_id).all()

def return_participant_urgent_results(participant_id):
    """ return all of a participant's urgent results"""
    return Result.query.filter(Result.participant_id == participant_id, Result.urgent is True).all()

# GET ITEMS

def get_study_by_id(study_id):
    """Return study based on study id"""

    return Study.query.get(study_id)

def get_participant_by_id(participant_id):
    """Return participant from participant id"""

    return Participant.query.get(participant_id)

def get_result_by_id(result_id):

    return Result.query.get(result_id)

def get_result_by_result_plan_by_participant(participant_id, result_plan_id):
    """ return a participant's return decisions for a study"""

    return Result.query.filter_by(result_plan_id = result_plan_id, participant_id = participant_id).first()

def get_investigator_by_id(investigator_id):
    
    return Investigator.query.get(investigator_id)

def get_investigator_by_email(email):

    return Investigator.query.filter(Investigator.email == email).first()

def get_participant_by_email(email):

    return Participant.query.filter(Participant.email == email).first()

def check_study_participant(study_id, participant_id):
    """ return participant-study link if they're enrolled in a study"""

    return ParticipantsStudies.query.filter_by(study_id = study_id, participant_id = participant_id).first()

def get_hcp_info(participant_id):
    """ return a participant's HCP info in db"""
    participant = get_participant_by_id(participant_id)

    hcp_info = {}
    hcp_info['hcp_fullname'] = {participant.hcp_fullname}
    hcp_info['hcp_phone'] = {participant.hcp_phone}
    hcp_info['hcp_email'] = {participant.hcp_email}
    hcp_info['hcp_practice'] = {participant.hcp_practice}

    return hcp_info

# UPDATES

def update_receive_decision(participant_id, result_plan_id, receive_decision):
    """Update decision"""
    
    Result.query.filter_by(result_plan_id = result_plan_id, participant_id = participant_id).update({"receive_decision": receive_decision})
    db.session.commit()

def add_password(user_type, email, password):
    """ add password to existing record of certain email"""

    if user_type== "investigator":
        Investigator.query.filter_by(email = email).update({"password": password})
    elif user_type== "participant":
        Participant.query.filter_by(email = email).update({"password": password})
    db.session.commit()

def update_attr_by_category_and_id(input_dict, category, item_id):
    """ update any attribute of participant or study when specifying category and id"""

    print("************item ID: ", item_id)
    if category == "participant":
        item = get_participant_by_id(item_id)
    elif category == "study":
        item = get_study_by_id(item_id)

    for key in input_dict:
        setattr(item, key, input_dict[key])

    db.session.commit()

    return 'success'

def update_result(results, participant_id):
    """add in result values for a participant's result"""

    for result in results:
        result_plan_id = result["result_plan_id"]
        result_record = get_result_by_result_plan_by_participant(participant_id=participant_id, result_plan_id=result_plan_id)

        setattr(result_record, 'result_value', result["result_value"])
        if result["urgent"] is True:
            setattr(result_record, 'urgent', True)
        else:
            setattr(result_record, 'urgent', False)

    db.session.commit()

    return "success"

  
# CHECK IF A PARTICIPANT HAS BEEN NOTIFIED ABOUT ANY AVAILABLE NON URGENT RESULTS THAT 
# THEY CONSENTED TO RECEIVE
def check_if_should_notify(participant_id):
    participant = get_participant_by_id(participant_id)
    notification = {'code': 0, 'msg': ''}
    for result in participant.results:
    # notify about urgent result no matter what
        if result.result_value != None:
            if result.urgent is True and result.notified is None:
                notification['code'] = 1
                notification['msg'] = "There is an urgent result in your research portal. Please log in immediately to view and call the study investigator listed."
            # if participant consented to receive and the plan is to return:
            elif result.receive_decision is True and result.result_plan.return_plan is True:
                # if the study timing lines up with the plan timing to return:
                if result.result_plan.study.status in ['Planning', 'Active'] and result.result_plan.return_timing == "during":
                    if result.notified is None:
                        notification['code'] = 2
                        notification['msg'] = "Results from your study have been posted to your participant portal. Please login to view."
                elif result.result_plan.study.status in ['Closed/Analysis', 'Published'] and result.result_plan.return_timing in ['during', 'after']:
                    if result.notified is None:
                        notification['code'] = 3
                        notification['msg'] = "Your research study has ended and your results have been made available. Login to view."
    return notification

def mark_notified(participant_id):
    """ mark any result as notified after notification was sent that new results were available"""
    participant = get_participant_by_id(participant_id)
    print("********************i'm in notified")

    for result in participant.results:
        if result.result_value != None:
            if result.urgent is True:
                setattr(result, 'notified', True)
            elif result.receive_decision is True and result.result_plan.return_plan is True:
                if result.result_plan.study.status in ['Planning', 'Active'] and result.result_plan.return_timing == "during":
                    setattr(result, 'notified', True)
                    print("*******************supposed to be here")
                elif result.result_plan.study.status in ['Closed/Analysis', 'Published'] and result.result_plan.return_timing in ['during', 'after']:
                    setattr(result, 'notified', True)

    db.session.commit()
                   

if __name__ == '__main__':
    from server import app
    connect_to_db(app)