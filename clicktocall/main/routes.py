from flask import jsonify
from flask import render_template
from flask import request
from flask import url_for
from . import main

from twilio import twiml
from twilio.rest import TwilioRestClient
# Route for Click to Call demo page.
@main.route('/')
def index():
    return render_template('home.html',
                           configuration_error=None)


# Voice Request URL
@main.route('/call', methods=['POST'])
def call():
    # Get phone number we need to call
    phone_number = request.form.get('phoneNumber', None)

    try:
        twilio_client = TwilioRestClient(main.config['TWILIO_ACCOUNT_SID'],
                                         main.config['TWILIO_AUTH_TOKEN'])
    except Exception as e:
        msg = 'Missing configuration variable: {0}'.format(e)
        return jsonify({'error': msg})

    try:
        twilio_client.calls.create(from_=app.config['TWILIO_CALLER_ID'],
                                   to=phone_number,
                                   url=url_for('.outbound',
                                               _external=True))
    except Exception as e:
        main.logger.error(e)
        return jsonify({'error': str(e)})

    return jsonify({'message': 'Call incoming!'})


@main.route('/outbound', methods=['POST'])
def outbound():
    response = twiml.Response()

    response.say("Bonjour, merci de contacter iDayit. Votre appel va etre redirige",
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
