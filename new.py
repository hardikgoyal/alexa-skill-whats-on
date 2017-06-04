from __future__ import print_function
from getMenu import getSpeech

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():

    session_attributes = {
        "meal":"none",
        "hall":"none"
    }
    card_title = "Welcome"
    speech_output = "Welcome to the What's cooking at USC dining Hall. " \
                    "What dining hall would you be interested in, " \
                    "You can say any of the three dining hall's name"
    # If the user either does not reply to the welcome message or says something
    reprompt_text = "What dining hall would you be interested in, " \
                    "You can say any of the three dining hall's name"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def MenuIntent(intent, session):
    card_title = intent['name']
    should_end_session = False
    sessionAttr = session.get('attributes', {});
    menu = [];
    if 'hall' in intent['slots'] and 'meal' in intent['slots']:
        session['attributes']['hall'] = intent['slots']['hall']['value']
        session['attributes']['meal'] = intent['slots']['meal']['value']
        menu = getMenu(session);
        reprompt_text = None;
        should_end_session = True;
        speech_output =  getSpeech (session['attributes']['hall'],session['attributes']['meal'])
        # Some more. 
    elif 'hall' in intent['slots']:
        session['attributes']['hall'] = intent['slots']['hall']['value']
        if session['attributes']['meal'] != "none":
            speech_output =  getSpeech (session['attributes']['hall'],session['attributes']['meal'])          
            reprompt_text = None;
            should_end_session = True;
        else:
            #Ask for dining Hall.
            speech_output = "What meal's menu are you looking at" + \
                            session['attributes']['hall'] + \
                            "?"                        
            reprompt_text = "What meal's menu are you looking at" + \
                            session['attributes']['hall'] + \
                            "?"
    elif 'meal' in intent['slots']:
        session['attributes']['meal'] = intent['slots']['meal']['value']
        if session['attributes']['meal'] != "none":
            # Information Complete;
            speech_output =  getSpeech (session['attributes']['hall'],session['attributes']['meal'])
            reprompt_text = None;
            should_end_session = True;
        else:
            #Ask for Meal Information.   
            speech_output = "What dining hall's" + \
                            session['attributes']['meal'] + " menu would you like ?"                        
            reprompt_text = "What dining hall's" + \
                            session['attributes']['meal'] + " menu would you like ?" 
    else:
        speech_output = "I'm not sure what you said. " \
                        "Please try Again."
        reprompt_text = "I'm not sure what you said. " \
                        "Please try Again"

    return build_response(session.get('attributes',{}), build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


#---------------- Events -------------------------------------------------------
def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    #to_store the data of the session, what dining hall, etc.

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    # Send Skill's Welcome Message
    return get_welcome_response()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "MenuIntent":
        return MenuIntent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):

    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # cleanup logic here



# --------------- Main handler --------------------------------------------------

def lambda_handler(event, context):
    
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])