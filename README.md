# Returning Important Research Data to Research Participants (Returning Research Results)

## Summary

**Returning Research Results** is a planning and implementation tool for research organizations and sites to use to share important research data to the participants who contribute towards their studies. It features a planning component that offers flexible control over what is shared and when, management components to enroll participants in studies and update their personal details, add their data, and send notifications about available results, and a "portal" for participants to log in and view their results, update their personal details, and obtain information relevant to the study(s) they are enrolled in.

## About the Developer

Returning Research Results was created by Lisa Murray. Learn more about the developer on [LinkedIn](https://www.linkedin.com/in/lisamichellemurray).

## Technologies

**Tech Stack:**

- Python
- Javascript
- React
- Flask
- SQLAlchemy
- Jinja2
- HTML5
- CSS
- AJAX
- Flask Mail
- Python unittest module
- Faker package


Returning Research Results is an app built on a Flask server with a PostgreSQL database, with SQLAlchemy as the ORM. The front end templating uses Jinja2 and occasional React rendering, the CSS is responsive thanks to flexbox and was made from scratch, and the Javascript uses AJAX to interact with the backend. Email notifications are sent using the Flask Mail module. The site is seeded with fake data using the Faker package for demonstration purposes. Server routes, login, and form submission are tested using the Python unittest module.


## Features


### Login, Registration, Permissions

Login/registration differentiate investigators from participants and restrict pages accordingly. Registration is limited to accounts that were set up by an investigator or administrator.

Participants are restricted from investigator pages and are limited to only viewing information about themselves.

Logged out users are automatically redirected to the log in page.

### Study and Result Planning with Dynamic Forms

The planning tool gets all of the required data to create an automated process to display results to participants at the right time (if at all). It allows for maximum flexibility for both investigators and participants and responds dynamically to user input.

### Enrollment in research studies & gathering participant decisions

Participants can be enrolled in studies as "new" or "existing" participants. The latter enrollment option includes a validation check to ensure that an input "existing participant" indeed exists and refers to the correct participant.

When a participant is enrolled in a study, they are immediately offered choices as to whether or not they would like to receive the results that will be returned from the study. This page includes all of the information that could be relevant to a participant to make their decision.

These decisions can be updated by participants themselves at any point, or by investigators if they are instructed to update them by participants.

### Dynamic Results Input Using React + Automated Email Notifications

The results input includes multiple input validations, auto-filled inputs based on query string parameters, dynamic selection of studies and tests based on the study's result plans, and the ability to add multiple results at once.

After a result is added for a given participant, the app automatically checks whether a participant should be notified of a new result in their portal, sends a notification email if so, and marks the participant as notified.

If a result is marked as urgent, the participant's healthcare provider contact info is displayed so that the investigator can also inform them of the urgent medical situation if appropriate.

### Detail Display and On-Page Edits using Javascript

On the Studies and Participant pages, the app displays key details of a selected item without loading a new page.

Specific Study/Participant pages feature all of the relevant details about a selected item, and both include methods to update information on that page directly, without reloading.

For studies, changing the study status triggers an automatic check for every enrolled participant to see if results can now be displayed to them (if any were withheld until a particular study status). As with results input, this check will notify them of their results and mark them as "notified".

### Most important business need: hiding/displaying results to participants based on heirerarchical factors

Conditional logic determines whether and when a result should be displayed to a participant on their portal. This is of paramount importance, as improper results return could un-blind participants and present a serious risk to study integrity, or end in legal ramifications if the participant either did not want to receive information that was given to them or was not informed of an urgent medical situation that the study revealed.

There are 4 factors that impact this result display to a participant: the initial plan to return the result or not, the planned timing of return (during or after a study), the particpant's decision to receive it or not, and whether the result is urgent (in which case it would be returned regardless of the other factors). 

Conditional logic has been worked into the server-side rendering of results to determine the appropriate results display depending on the above factors. The same logic is integrated into the app's notification system and gives a message depending on what prompted the result to be returned.

A key advantage of this automated process is that the investigator does not need to think through the factors and determine for each result for each participant whether or not it should be returned.

[Integration tests](https://github.com/lmmurray/returning-results/blob/753f154ae90e53c6793eb9f552e756fd545f9930/tests.py#L166) check various [combinations](https://github.com/lmmurray/returning-results/blob/753f154ae90e53c6793eb9f552e756fd545f9930/model.py#L152-L156) of these factors that determine result display.


## For Version 2.0

- **More data sanitization:** There are some checks in place to ensure data are properly formatted for their meaning, but more could be added to reduce opportunities for user error
- **Database codes instead of strings:** Some categorical fields were implemented in the database as strings for the sake of quick development. Future versions would be more flexible, simplified, and less error prone by implementing them as codes and having accompanying lookup tables for the codes' descriptions
- **Study summaries:**  Once a study staus has been changed to published, participant portals could display details about the study overall, aggregate results, and/or comparison's between a participant's given result and the study average for that result. This could at least be interesting to participants, but in many instance could give them information that is highly relevant to their medical care depending how they responded to the treatment
- **Security:** In future versions, passwords can be hashed before being stored in the database, and other security features could be implemented given the potentially sensitive nature of health information that is shared (and perhaps applicable regulations)