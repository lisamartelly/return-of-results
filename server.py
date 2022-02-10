
from flask import Flask, render_template, redirect, flash, session, request, jsonify
from flask_mail import Mail, Message
from model import connect_to_db
import jinja2
import crud
import os
from faker import Faker
from jinja2 import StrictUndefined
import json

fake = Faker()
app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Help with Jinja errors
app.jinja_env.undefined = jinja2.StrictUndefined

# make the Flask interactive debugger more useful
# remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

########## NEED TO RUN SOURCE SECRETS.SH AT START OF EACH TERMINAL FOR EMAIL TO SEND #############

# email configurations
mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

############# ROUTES FOR INVESTIGATOR-ONLY PAGES ######################

# HOMEPAGE
@app.route('/')
def show_homepage():
    if "user" in session:
        if session["user_type"] == "participant":
            user = crud.get_participant_by_id(session["user_id"])
        elif session["user_type"] == "investigator":
            user = crud.get_investigator_by_id(session["user_id"])
        print(user)
        return render_template('home.html', user=user)
    else:
        return render_template('home-logged-out.html')

# LISTS ALL STUDIES
@app.route('/studies')
def show_studies():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')
   
    studies = crud.return_all_studies()
    return render_template('studies.html', studies=studies)

# SHOW STUDY DETAILS
@app.route('/studies/<study_id>')
def show_study_details(study_id):
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    study = crud.get_study_by_id(study_id)
    return render_template('study_details.html', study=study)

# ENROLL A PARTICIPANT IN A STUDY
@app.route('/enroll-participant')
def enroll_participant_form():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    studies = crud.return_all_studies()
    return render_template('enroll_participant.html', studies=studies)

# LIST ALL PARTICIPANTS
@app.route('/participants')
def show_all_participant():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    participants = crud.return_all_participants()
    return render_template('/participants.html', participants=participants)

# SHOW PARTICIPANT DETAILS
@app.route('/participants/<participant_id>')
def show_participant_details(participant_id):
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    participant = crud.get_participant_by_id(participant_id)

    for result in participant.results:
        print("********participant.result:", result)
    return render_template('participant_all_details.html', participant=participant)

# SHOW PAGE FOR CREATING RESULTS
@app.route('/results')
def show_add_results_page():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    return render_template('add-results.html')

########### ROUTES FOR PARTICIPANT-ONLY VIEWS #####################

@app.route('/participant/my-details')
def show_participant_their_details():
    if "user" not in session: return redirect('/')

    participant = crud.get_participant_by_id(session['user_id'])
    return render_template('participant-my-details.html', participant=participant)

@app.route('/participant/my-studies')
def show_participant_their_studies():
    if "user" not in session: return redirect('/')

    participant = crud.get_participant_by_id(session['user_id'])
    return render_template('participant-my-studies.html', participant=participant)

@app.route('/participant/my-results')
def show_participant_their_results():
    if "user" not in session: return redirect('/')

    participant = crud.get_participant_by_id(session['user_id'])
    return render_template('participant-my-results.html', participant=participant)

##################### FORM PROCESSING AND OTHER REDIRECTS #############################

# PROCESS LOGIN INFO
@app.route('/login', methods=["POST"])
def login_user():

    email = request.form.get("email").lower()
    password = request.form.get("password")
    user_type = request.form.get("user_type")

    # check if login-er is a registered user by checking email
    if user_type == "investigator":
        user = crud.get_investigator_by_email(email)
        if user:
            user_id = user.investigator_id
    elif user_type == "participant":
        user = crud.get_participant_by_email(email)
        if user:
            user_id = user.participant_id
    
    # if user's email is registered, check if password is correct
    if user:
        if password == user.password:
            session['user'] = user.email
            session['user_type'] = user_type
            session['user_id'] = user_id
        else:
            flash("Incorrect password, try again.")
    else:
        flash("User not registered.")

    return redirect('/')

# PROCESS REGISTRATION INFO
@app.route('/register', methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user_type")

    #check if user in investigator or pt tables
    if user_type == "investigator":
        user = crud.get_investigator_by_email(email)
    elif user_type == "participant":
        user = crud.get_participant_by_email(email)

    if user:
        if user.password:
            flash("Account already registered.")
        else:
            crud.add_password(user_type=user_type, email=email, password=password)
            flash("Account registered, now please login")
    else:
        flash("Email not in system or registering under wrong category. Contact administrator to be able to register.")
    return redirect('/')
    
# PROCESS LOGOUT
@app.route('/logout')
def logout_user():
    if "user" in session:
        session.pop("user")
        session.pop("user_type")
        return render_template('home-logged-out.html')
    else:
        return render_template('home-logged-out.html')

# BEGIN STUDY RESULT PLANNING
@app.route('/planning-1')
def plan_one():
    """ gather study details"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    investigators = crud.return_all_investigators()
    return render_template('planning-1.html', investigators=investigators)

# SECOND STAGE OF RESULT PLANNING
@app.route('/planning-2', methods=["POST"])
def plan_two():
    """ get number of tests per each visit"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    dict_visits = {visit: 0 for visit in request.form.getlist("visits")}
    investigator_id = request.form.get("study-investigator")
    study_name = request.form.get("study-name")

    if request.form.get('num-visits'):
        num_visits = request.form.get('num-visits')
    else:
        num_visits = 0

    for i in range(int(num_visits)):
        dict_visits[f'study-visit-{i+1}'] = 0

    session['visits'] = dict_visits
    session['study_name'] = study_name
    session['investigator_id'] = investigator_id

    if session['study_name'] == '':
        return redirect('/planning-1')
    else:
        dict_visits = session['visits']
        return render_template('/planning-2.html', dict_visits=dict_visits)

# GATHER FINAL STUDY PLANS
@app.route('/planning-3', methods=["POST"])
def plan_three():
    """create result plan for each test in each visit"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    temp_dict=dict(session['visits'])

    #visit details from form:
    for visit in session['visits']:
        num_visits = int(request.form.get(f"{visit}-num-visits"))
        temp_dict[visit] = num_visits
    
    session['visits'] = temp_dict
    if session['study_name'] == '':
        return redirect('/planning-1')
    else:
        dict_visits = session['visits']
        return render_template('/planning-3.html', dict_visits=dict_visits)

# LAST STEP IN RESULT PLANNING AND PROCESSING
@app.route('/plan-study', methods=["POST"])
def plan_study():
    """ after getting all needed data, process into result_plans and redirect to study details"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    # study details from session:
    study_name = session['study_name']
    investigator_id = session['investigator_id']
    investigational_product = fake.unique.license_plate()

    study = crud.create_study(investigator_id, study_name, investigational_product, status="Planning")

    #plan details from form:
    for visit in session['visits']:
        for i in range(session['visits'][visit]):
            study_id = study.study_id
            test_name = request.form.get(f"{visit}-test{i}-test-name")
            result_category = request.form.get(f"{visit}-test{i}-result_category")

            urgency_potential_pre = request.form.get(f"{visit}-test{i}-urgency-potential")
            if urgency_potential_pre =="yes": 
                urgency_potential = True
            else: 
                urgency_potential = False

            return_plan_pre = request.form.get(f"{visit}-test{i}-return_plan")
            if return_plan_pre =="yes": 
                return_plan = True
            else: 
                return_plan = False

            if return_plan == False:
                return_timing = None
            else:
                return_timing = request.form.get(f"{visit}-test{i}-return_timing")
         
            crud.create_result_plan(study_id, result_category, visit, urgency_potential, return_plan, test_name, return_timing)

    session['visits'] = ''
    session['study_name'] = ''
    session['investigator_id'] = ''

    return redirect(f'/studies/{study.study_id}')

# PROCESS PARTICIPANT ENROLLMENT
@app.route('/enroll', methods=["POST"])
def create_participant_in_db():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    if request.form.get("existing") == "yes":
        participant = crud.get_participant_by_id(int(request.form.get("participant_id")))
        study_id = int(request.form.get("study_id"))

    elif request.form.get("existing") == "no":
        email = request.form.get("email")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        dob = request.form.get("dob")
        phone = request.form.get("phone")
        study_id = int(request.form.get("study_id"))

        participant = crud.create_participant(email, fname, lname, dob, phone)

    crud.create_participantsstudies_link(participant.participant_id, study_id)
    return redirect(f'/decisions/{study_id}/{participant.participant_id}')

# ASK PARTICIPANTS WHICH RESULTS THEY WANT TO RECEIVE - VIEWABLE TO PARTICIPANTS TOO
@app.route('/decisions/<study_id>/<participant_id>')
def get_receive_decisions(study_id, participant_id):
    """ ask participants which results they want to receive"""
    if "user" not in session : return redirect('/')

    study=crud.get_study_by_id(study_id)
    participant=crud.get_participant_by_id(participant_id)

    return render_template('/decisions.html', study=study, participant=participant)

# PROCESS PARTICIPANT DECISION TO RECEIVE RESULTS
@app.route('/decide/<study_id>/<participant_id>', methods=["POST"])
def save_receive_decisions(study_id, participant_id):
    """ save participant's decisions to receive results or not"""
    if "user" not in session : return redirect('/')

    study=crud.get_study_by_id(study_id)
    for result_plan in study.result_plans:
        receive_decision_pre = request.form.get(f"{result_plan.result_plan_id}-receive")
        if receive_decision_pre =="yes":
            receive_decision = True
        elif receive_decision_pre =="no":
            receive_decision = False
        else: 
            receive_decision = None
        
        #check if updating or making new
        if crud.get_result_by_result_plan_by_participant(participant_id, result_plan.result_plan_id):
            crud.update_receive_decision(
                participant_id=participant_id,
                result_plan_id=result_plan.result_plan_id,
                receive_decision=receive_decision)
        else:
            crud.create_result(
                participant_id=participant_id,
                result_plan_id=result_plan.result_plan_id
                receive_decision=receive_decision)
    if session["user_type"] == 'investigator':
        return redirect(f'/participants/{participant_id}')
    elif session["user_type"] == 'participant':
        return redirect(f'/participant/my-results')

# PROCESS FORM TO UPDATE PARTICIPANT RESULT
@app.route('/create-result', methods=["POST"])
def create_result():
    """ create a single result using participant_id, result_plan_id, urgent, result_value"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    participant_id = request.json.get("participantId")
    results = request.json.get("results")
    
    crud.update_result(results=results, participant_id=participant_id)
        
    return redirect(f'/results-add-email/{participant_id}')

# CHECK AND SEND EMAIL FOR PARTICIPANT AFTER RESULTS INPUT
@app.route('/results-add-email/<participant_id>')
def check_and_notify_after_results_added(participant_id):
    """ route after result is submitted to notify participants about results"""
    notification = crud.check_if_should_notify(participant_id)
    participant = crud.get_participant_by_id(participant_id)
    if notification['code'] != 0:
        msg = Message('Research Results Available', sender = 'return.of.results.dev@gmail.com', recipients = [participant.email])
        msg.body = notification['msg']
        msg.html = render_template('email.html', text=notification['msg'], name=participant.fname)
        mail.send(msg)
        crud.mark_notified(participant_id)

    return redirect(f'/participants/{participant_id}')

# CHECK AND SEND EMAIL FOR ALL STUDY PARTICIPANTS AFTER STATUS IS CHANGED
@app.route('/study-change-email/<study_id>')
def check_and_notify_after_study_status_changed(study_id):
    """ after a study status is changed check if participants should be notified of results and notify them"""
    participants = crud.return_all_study_participant_ids(study_id)

    for participantstudylink in participants:
        notification = crud.check_if_should_notify(participantstudylink.participant_id)
        participant = crud.get_participant_by_id(participantstudylink.participant_id)
        if notification['code'] != 0:
            msg = Message('Research Results Available', sender = 'return.of.results.dev@gmail.com', recipients = [participant.email])
            msg.body = notification['msg']
            msg.html = render_template('email.html', text=notification['msg'], name=participant.fname)
            mail.send(msg)
            crud.mark_notified(participantstudylink.participant_id)
    
    return 'Status updated and participants notified of results if applicable'


################## JSON ROUTES #############################

# RETURN LIST OF ALL STUDIES
@app.route('/studies.json')
def return_studies():
    """ return JSON dict of all study objects in db"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    results = crud.return_all_studies()
    studies = []

    for study in results:
        studies.append({"study_id": study.study_id, "study_name" : study.study_name})
            
    return jsonify(studies)

# CHECK IF PARTICIPANT IS ENROLLED IN STUDY
@app.route('/study-participants.json/<study_id>/<participant_id>')
def check_study_participants(study_id, participant_id):
    """ check if given participant ID is an enrolled study participant and include HCP info"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    participant_study_link = crud.check_study_participant(study_id, participant_id)
    result = {}

    if participant_study_link:
        # return if participant is enrolled in study
        participant = crud.get_participant_by_id(participant_id)
        result['code'] = 1
        result['msg'] = f'Adding results for: {participant.fname} {participant.lname}'
        result['hcp_fullname'] = f'{participant.hcp_fullname}'
        result['hcp_phone'] = f'{participant.hcp_phone}'
        result['hcp_email'] = f'{participant.hcp_email}'
        result['hcp_practice'] = f'{participant.hcp_practice}'
    else:
        # return if participant is not enrolled in study
        result['code'] = 0
        result['msg'] = 'No participant with that ID is enrolled in this study'
        
    return jsonify(result)

# RETURN ALL VISITS AND TESTS IN A STUDY
@app.route('/visits-results.json/<study_id>')
def return_visits(study_id):
    """ return JSON list of all tests and all visits of a given study"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    study = crud.get_study_by_id(study_id)
    results = []

    for result_plan in study.result_plans:
        results.append({
            "result_plan_id": result_plan.result_plan_id, 
            "test_name" : result_plan.test_name,
            "visit" : result_plan.visit,
            })
    return jsonify(results)

# RETURN DETAILS ABOUT A PARTICIPANT
@app.route('/participant-details.json/<participant_id>')
def return_participant_details(participant_id):
    """ return json object of select details about participant and their studies"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    participant = crud.get_participant_by_id(participant_id)
    results = {
        'fname' : participant.fname,
        'lname' : participant.lname,
        'id' : participant.participant_id,
        'phone': participant.phone,
        'email': participant.email,
        'studies': [],
        }

    for study in participant.studies:
        study_obj = {}
        study_obj['study_name'] = study.study_name
        study_obj['study_id'] = study.study_id
        study_obj['status'] = study.status
        results['studies'].append(study_obj)

    return jsonify(results)

# RETURN SELECT DETAILS OF A STUDY
@app.route('/study-details.json/<study_id>')
def return_study_details(study_id):
    """ return json object of select details about study"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    study = crud.get_study_by_id(study_id)
    results = {
        'name' : study.study_name,
        'id' : study.study_id,
        'product' : study.investigational_product,
        'status' : study.status,
        'investigator_fname' : study.investigator.fname,
        'investigator_lname' : study.investigator.lname,
        }
    return jsonify(results)

# CHECK IF PARTICIPANT IN DB AND RETURN DETAILS OR ERROR MSG
@app.route('/check-participant.json/<participant_id>')
def check_participant_id(participant_id):
    """ json route to check if an inputted participant ID is existing before they are enrolled"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    participant = crud.get_participant_by_id(participant_id)
    result = {}
    if participant:
        # return if participant is already in db
        result['code'] = 1
        result['msg'] = f'Enrolling: {participant.fname} {participant.lname}'
    else:
        # return if participant is not already in db
        result['code'] = 0
        result['msg'] = 'No participant with that ID exists, please check the ID or enroll as a new participant'
    return jsonify(result)

# UPDATE PARTICIPANT OR STUDY OR RESULT IN DB
@app.route('/update-by-attr.json/<category>/<item_id>', methods=["POST"])
def update_attr_by_category_and_id(category, item_id):
    """update attributes of participants or studies if already in db"""
    if "user" not in session : return redirect('/')

    input_dict = request.json
    update = crud.update_attr_by_category_and_id(input_dict, category, item_id)

    if update == 'success':
        return 'Changes saved'
    else:
        return 'Error - try again'



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

