
from flask import Flask, render_template, redirect, flash, session, request, jsonify
from model import connect_to_db
import jinja2
import crud
from faker import Faker
from jinja2 import StrictUndefined

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
    return render_template('home.html')


@app.route('/studies')
def show_studies():
    studies = crud.return_all_studies()
    return render_template('studies.html', studies=studies)


@app.route('/studies/<study_id>')
def show_study_details(study_id):
    study = crud.get_study_by_id(study_id)
    return render_template('study_details.html', study=study)

# @app.route('/plan-study-visits', methods=["POST"])
# def prep_for_results():
#     """Return a list of visits to create tests and plans for"""

#     return redirect('/planning-2')

@app.route('/planning-1')
def plan_one():
    """ gather study details"""

    investigators = crud.return_all_investigators()
    return render_template('planning-1.html', investigators=investigators)

@app.route('/planning-2', methods=["POST"])
def plan_two():
    """ get number of tests per each visit"""

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

    # my_data = request.form
    # for key in my_data:
    #     print(f'form key,{key},{my_data[key]}')

    # return jsonify(request.form)
    print("session 3 before loop/temp dict: ",session)
    temp_dict=dict(session['visits'])

    #visit details from form:
    for visit in session['visits']:
        num_visits = int(request.form.get(f"{visit}-num-visits"))
        temp_dict[visit] = num_visits
    
    session['visits'] = temp_dict
    print("session 3, temp dict: ",session)
    if session['study_name'] == '':
        return redirect('/planning-1')
    else:
        dict_visits = session['visits']
        return render_template('/planning-3.html', dict_visits=dict_visits)


@app.route('/plan-study', methods=["POST"])
def plan_study():
    """ after getting all needed data, process into result_plans and redirect to study details"""
    print("session end: ", session)
    # print("session['visits']: ", session['visits'])
    # my_data = request.form
    # for key in my_data:
    #     print(f'form key,{key},{my_data[key]}')

    # return jsonify(request.form)

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
            
            print()
            result_plan = crud.create_result_plan(study_id, result_category, visit, urgency_potential, return_plan, test_name, return_timing)
            print("result plan: ", result_plan)

    session['visits'] = ''
    session['study_name'] = ''
    session['investigator_id'] = ''

    return redirect(f'/studies/{study.study_id}')

# @app.route('/json_studies')
# def return_all_studies():
#     studies = crud.return_all_studies()
#     study_list = [study.study_name for study in studies]
#     return jsonify(study_list)

@app.route('/enroll-participant')
def enroll_participant_form():
    studies = crud.return_all_studies()
    return render_template('enroll_participant.html', studies=studies)

@app.route('/enroll', methods=["POST"])
def create_participant_in_db():

    my_data = request.form
    for key in my_data:
        print(f'form key,{key},{my_data[key]}')

    email = request.form.get("email")
    fname = request.form.get("fname")
    lname = request.form.get("lname")
    dob = request.form.get("dob")
    phone = email = request.form.get("phone")
    study_id = int(request.form.get("study_id"))

    participant = crud.create_participant(email, fname, lname, dob, phone)
    ps = crud.create_participantsstudies_link(participant.participant_id, study_id)
    return redirect(f'/participants/{participant.participant_id}')

@app.route('/participants')
def show_all_participant():

    participants = crud.return_all_participants()
    return render_template('/participants.html', participants=participants)

@app.route('/participants/<participant_id>')
def show_participant_details(participant_id):
    participant = crud.get_participant_by_id(participant_id)
    print("participant.studies", participant.studies)
    return render_template('participant_details.html', participant=participant)

@app.route('/login')
def login_user():
    pass


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)

