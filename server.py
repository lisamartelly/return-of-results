
from flask import Flask, render_template, redirect, flash, session, request, jsonify
from model import connect_to_db
import jinja2
import crud
from faker import Faker
from jinja2 import StrictUndefined
import json

fake = Faker()
app = Flask(__name__)

# A secret key is needed to use Flask sessioning features
app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.
app.jinja_env.undefined = jinja2.StrictUndefined

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True

@app.route('/')
def show_homepage():
    if "user" in session:
        return render_template('home.html')
    else:
        return render_template('home-logged-out.html')

@app.route('/login', methods=["POST"])
def login_user():

    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user-type")

    if user_type == "investigator":
        user = crud.get_investigator_by_email(email)
        if user:
            user_id = user.investigator_id
    elif user_type == "participant":
        user = crud.get_participant_by_email(email)
        if user:
            user_id = user.participant_id
    
    if user:
        if password == user.password:
            session['user'] = user.email
            session['user_type'] = user_type
            session['user_id'] = user_id
            print(session)
        else:
            flash("Incorrect password, try again.")
    else:
        flash("User not registered.")

    return redirect('/')

@app.route('/register', methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")
    user_type = request.form.get("user-type")

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
    
@app.route('/logout')
def logout_user():
    if "user" in session:
        session.pop("user")
        session.pop("user_type")
        # session.pop("user_id")
        return render_template('home-logged-out.html')
    else:
        return render_template('home-logged-out.html')


@app.route('/studies')
def show_studies():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')
   
    studies = crud.return_all_studies()
    return render_template('studies.html', studies=studies)

@app.route('/studies/<study_id>')
def show_study_details(study_id):
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    study = crud.get_study_by_id(study_id)
    return render_template('study_details.html', study=study)

@app.route('/planning-1')
def plan_one():
    """ gather study details"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    investigators = crud.return_all_investigators()
    return render_template('planning-1.html', investigators=investigators)

@app.route('/planning-2', methods=["POST"])
def plan_two():
    """ get number of tests per each visit"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    dict_visits = {visit: 0 for visit in request.form.getlist("visits")}
    investigator_id = request.form.get("study-investigator")
    study_name = request.form.get("study-name")
    num_visits = request.form.get('num-visits')

    for i in range(int(num_visits)):
        dict_visits[f'study-visit-{i+1}'] = 0

    session['visits'] = dict_visits
    session['study_name'] = study_name
    session['investigator_id'] = investigator_id

    print("session 2: ",session)

    if session['study_name'] == '':
        return redirect('/planning-1')
    else:
        dict_visits = session['visits']
        return render_template('/planning-2.html', dict_visits=dict_visits)


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

@app.route('/plan-study', methods=["POST"])
def plan_study():
    """ after getting all needed data, process into result_plans and redirect to study details"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    # study details from session:
    study_name = session['study_name']
    investigator_id = session['investigator_id']
    investigational_product = fake.unique.license_plate()

    study = crud.create_study(investigator_id, study_name, investigational_product, status_code=1)

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

            return_timing = request.form.get(f"{visit}-test{i}-return_timing")
         
            result_plan = crud.create_result_plan(study_id, result_category, visit, urgency_potential, return_plan, test_name, return_timing)

    session['visits'] = ''
    session['study_name'] = ''
    session['investigator_id'] = ''

    return redirect(f'/studies/{study.study_id}')

@app.route('/enroll-participant')
def enroll_participant_form():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    studies = crud.return_all_studies()
    return render_template('enroll_participant.html', studies=studies)

@app.route('/enroll', methods=["POST"])
def create_participant_in_db():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    # print("form", request.form)
    # my_data = request.form
    # for key in my_data:
    #     print(f'form key,{key},{my_data[key]}')
    # return jsonify(request.form)

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

@app.route('/decisions/<study_id>/<participant_id>')
def get_result_decisions(study_id, participant_id):
    """ ask participants which results they want to receive"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    study=crud.get_study_by_id(study_id)
    participant=crud.get_participant_by_id(participant_id)

    return render_template(f'/decisions.html', study=study, participant=participant)

@app.route('/decide/<study_id>/<participant_id>', methods=["POST"])
def save_result_decisions(study_id, participant_id):
    """ save participant's decisions to receive results or not"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    study=crud.get_study_by_id(study_id)
    for result in study.result_plans:
        return_decision_pre = request.form.get(f"{result.result_plan_id}-receive")
        if return_decision_pre =="yes": 
            return_decision = True
        else: 
            return_decision = False
        
        #check if updating or  making new
        if crud.get_rd_by_rp_by_participant(participant_id, result):
            crud.update_return_decision(participant_id, result, return_decision)
        else:
            crud.create_result_decision(
                participant_id=participant_id,
                result_plan_id=result.result_plan_id,
                return_decision=return_decision)
    return redirect(f'/participants/{participant_id}')

@app.route('/participants')
def show_all_participant():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    participants = crud.return_all_participants()
    return render_template('/participants.html', participants=participants)

@app.route('/participants/<participant_id>')
def show_all_participant_details(participant_id):
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    participant = crud.get_participant_by_id(participant_id)
    print("participant.studies", participant.studies)
    return render_template('participant_all_details.html', participant=participant)

@app.route('/update.json/<participant_id>', methods=["POST"])
def add_hcp(participant_id):
    """ update info in participant's record in db"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    jsondict = request.json
    crud.update_participant(jsondict, participant_id)
    
    return 'Changes saved!'

@app.route('/results')
def show_add_results_page():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    return render_template('add-results.html')

@app.route('/studies.json')
def return_studies():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    """ return JSON dict of all study objects in db"""
    results = crud.return_all_studies()
    studies = []

    for study in results:
        studies.append({"study_id": study.study_id, "study_name" : study.study_name})
            
    return jsonify(studies)

@app.route('/study-participants.json/<study_id>/<participant_id>')
def check_study_participants(study_id, participant_id):
    """ check if given participant ID is an enrolled study participants"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    participant_study_link = crud.check_study_participant(study_id, participant_id)
    result = {}

    if participant_study_link:
        # return if participant is enrolled in study
        participant = crud.get_participant_by_id(participant_id)
        result['code'] = 1
        result['msg'] = f'Adding results for: {participant.fname} {participant.lname}'
    else:
        # return if participant is not enrolled in study
        result['code'] = 0
        result['msg'] = 'No participant with that ID is enrolled in this study'
        
    return jsonify(result)

@app.route('/visits-results.json/<study_id>')
def return_visits(study_id):
    """ return JSON dict of all study objects in db"""
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    study = crud.get_study_by_id(study_id)
    results = []

    for result in study.result_plans:
        results.append({
            "result_plan_id": result.result_plan_id, 
            "test_name" : result.test_name,
            "visit" : result.visit,
            })
            
    return jsonify(results)

@app.route('/create-result', methods=["POST"])
def create_result():
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    """ create a single result using participant_id, result_plan_id, urgent, result_value"""

    participant_id = request.json.get("participantId")
    results = request.json.get("results")
    for result in results:
        result_plan_id = result["result_plan_id"]
        if result["urgent"] is True:
            urgent = True
        else:
            urgent = False
        result_value = result["result_value"]

        crud.create_result(
            participant_id=participant_id,
            result_plan_id=result_plan_id,
            urgent=urgent,
            result_value=result_value
            )
    
    return "200 OK"

@app.route('/check-participant.json/<participant_id>')
def check_participant_id(participant_id):
    if "user" not in session or session["user_type"] != "investigator" : return redirect('/')

    """ json route to check if an inputted participant ID is existing before they are enrolled"""

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

# ROUTES FOR PARTICIPANT-ONLY VIEWS

@app.route('/participant/my-details')
def show_participant_their_details():
    if "user" not in session: return redirect('/')

    participant_id = session['user_id']
    participant = crud.get_participant_by_id(participant_id)
    print("participant.studies", participant.studies)
    return render_template('participant-my-details.html', participant=participant)

@app.route('/participant/my-studies')
def show_participant_their_studies():
    if "user" not in session: return redirect('/')

    participant_id = session['user_id']
    participant = crud.get_participant_by_id(participant_id)
    print("participant.studies", participant.studies)
    return render_template('participant-my-studies.html', participant=participant)

@app.route('/participant/my-results')
def show_participant_their_results():
    if "user" not in session: return redirect('/')

    participant_id = session['user_id']
    participant = crud.get_participant_by_id(participant_id)
    print("participant.studies", participant.studies)
    return render_template('participant-my-results.html', participant=participant)



if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

