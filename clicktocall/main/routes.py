from flask import jsonify, current_app, flash, session
from flask import render_template
from flask import request
from flask import url_for
from . import main
from clicktocall import db
from clicktocall.models import Message

from twilio import twiml
from twilio.rest import TwilioRestClient


# Route for Click to Call demo page.
@main.route('/')
def index():
    message = Message.query.first()

    return render_template('home.html',
                           configuration_error=None, message=message.messagetext)


# Voice Request URL
@main.route('/call', methods=['POST'])
def call():
    # Get phone number we need to call
    phone_number = request.form.get('phoneNumber', None)
    newmessage = request.form.get('message', None)
    message = Message.query.first()
    message.messagetext = newmessage
    db.session.add(message)
    db.session.commit()

    try:
        twilio_client = TwilioRestClient(current_app.config['TWILIO_ACCOUNT_SID'],
                                         current_app.config['TWILIO_AUTH_TOKEN'])
    except Exception as e:
        msg = 'Missing configuration variable: {0}'.format(e)
        return jsonify({'error': msg})

    try:

        twilio_client.calls.create(from_=current_app.config['TWILIO_CALLER_ID'],
                                   to=phone_number,
                                   url=url_for('.outbound',
                                               _external=True))

    except Exception as e:
        main.logger.error(e)
        return jsonify({'error': str(e)})

    flash('Call incoming')
    return render_template('home.html', message=message.messagetext)


@main.route('/outbound', methods=['POST'])
def outbound():
    response = twiml.Response()
    message = Message.query.first()
    response.say(message.messagetext,
                 voice='alice', language='fr')
    '''
    # Uncomment this code and replace the number with the number you want
    # your customers to call.
    with response.dial() as dial:
        dial.number("+16518675309")
    '''
    return str(response)


# Route for Landing Page after Heroku deploy.
@main.route('/landing')
def landing():
    return render_template('landing.html',
                           configuration_error=None)
