"""Automatically drop, recreate, and populate database"""

import os
from random import randint, choice
from faker import Faker
import crud
import model
import server

os.system('dropdb irr')
os.system('createdb irr')

model.connect_to_db(server.app)
model.db.create_all()

fake = Faker()

#make specific investigator for testing
investigator = crud.create_investigator(fname="admin fname", lname="admin lname", email="test@test.com", phone="123456")
investigator.password = "test"

#make specific participant for testing
participant = crud.create_participant(email="test@test.com", fname="test fname", lname="test lname", dob="01/01/2020", phone="123456")
participant.password = "test"

#make fake investigators for db, no pws:
for i in range(10):
    i_fname = fake.first_name()
    i_lname = fake.last_name()
    i_phone = fake.phone_number()
    i_domain = fake.free_email_domain()
    i_email = f'{i_lname}.{i_fname}@{i_domain}'

    investigator = crud.create_investigator(fname=i_fname, lname=i_lname, email=i_email, phone=i_phone)

study_names = [ 
    'Covid-19 Vaccine Study - Adults',
    'Covid-19 Vaccine Study - Children',
    'Alzheimers Medication Trial',
    'Impact of Vitamin D on Depression',
    'Genetic Screening for Non-Treatable Diseases',
    'Effectiveness of Chemotherapy vs. Placebo',
    'Comparison of Vitamin D Supplements vs. Vacation on Depression',
    'Comparison of Covid-19 Vaccine to Placebo',
    'Accuracy of Colon Cancer Screening',
    'Accuracy of At-Home Covid-19 Tests']

for j in range(10):
    #create study details and study object
    investigator_id = randint(1,10)
    study_name = study_names[j]
    investigational_product = fake.unique.license_plate()
    status_code = randint(1,4)
    
    study = crud.create_study(investigator_id=investigator_id, study_name=study_name, investigational_product=investigational_product, status_code=status_code)

    #create three results to return per study:
    for visit in ['recruitment', 'consent', 'study-visit-1']:
        result_category = choice(['actionable','unknwon','personally valuable'])
        urgency_potential = choice([True, False])
        return_timing = choice(['during', 'after'])
        return_plan = choice([True, False])
        result_plan = crud.create_result_plan(
            study_id=study.study_id,
            result_category=result_category,
            visit=visit,
            urgency_potential=urgency_potential,
            return_plan=return_plan,
            test_name=f"{visit} test",
            return_timing=return_timing)


# create 10 participants per study
for k in range(100):

    # participant details
    p_fname = fake.first_name()
    p_lname = fake.last_name()
    p_phone = fake.phone_number()
    p_domain = fake.free_email_domain()
    p_dob = fake.date_of_birth(minimum_age=0, maximum_age=60)
    p_email = f'{p_lname}.{p_fname}@{p_domain}'
    # study_id = randint(1,10)

    crud.create_participant(email=p_email, fname=p_fname, lname=p_lname, dob=p_dob, phone=p_phone)

# enroll each participant in a random study
participants = crud.return_all_participants()

for participant in participants:
    crud.create_participantsstudies_link(
        participant_id=participant.participant_id,
        study_id=randint(1,10))
    crud.create_participantsstudies_link(
        participant_id=participant.participant_id,
        study_id=randint(1,10))

# choose to receive all results available in each study enrolled in:

for participant in participants:
    for study in participant.studies:
        for result in study.result_plans:
            crud.create_result_decision(participant_id=participant.participant_id, result_plan_id=result.result_plan_id, return_decision=True)



#create fake results for each study