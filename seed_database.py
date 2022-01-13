"""Automatically drop, recreate, and populate database"""

import os
from random import randint
from faker import Faker
import crud
import model
import server

os.system('dropdb irr')
os.system('createdb irr')

model.connect_to_db(server.app)
model.db.create_all()

fake = Faker()

for i in range(10):
    # create investigator
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
    
    crud.create_study(investigator_id=investigator_id, study_name=study_name, investigational_product=investigational_product, status_code=status_code)

# create 10 participants per study
for k in range(100):

    # participant details
    p_fname = fake.first_name()
    p_lname = fake.last_name()
    p_phone = fake.phone_number()
    p_domain = fake.free_email_domain()
    p_dob = fake.date_of_birth(minimum_age=0, maximum_age=60)
    p_email = f'{p_lname}.{p_fname}@{p_domain}'
    study_id = randint(1,10)

    crud.create_participant(email=p_email, fname=p_fname, lname=p_lname, dob=p_dob, phone=p_phone, study_id=study_id)

