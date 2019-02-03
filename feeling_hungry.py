"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""
from __future__ import print_function

import boto3, random

client = boto3.client('comprehend')

neutrals = [
    ['Ristorante Piccolo',
    '2.0 Miles',
    '1068 31st St NW'],
    ['Lupo Verde',
    '4.5 Miles',
    '1401 T St NW'],
    ['Pho Viet and Grille'
    , '2.0 Miles',
    '2721, 1639 Wisconsin Ave NW'],
    ['Shanghai Lounge',
    '2.0 Miles',
    '1734 Wisconsin Ave NW'],
    ['Kintaro',
    '1.8 Miles',
    '1039 33rd St Nw'],
    ['Bluefin Sushi',
    '2.0 Miles',
    '3073 Canal St NW'],
    ['Toro Toro',
    '3.8 Miles',
    '1300 I St NW'],
    ['El Centro DF',
    '2.4 Miles',
    '1218 Wisconsin Ave NW'],
    ['Curry and Pie',
    '2.3 Miles',
    '1204 34th St NW'],
    ['Taj of India',
    '2.2 Miles',
    '2809 M St NW']
    ]

negatives = [
    ['Chaia Tacos',
    '2.3 Miles',
    '3207 Grace St NW'],
    ['Casbah Cafe',
    '2.0 Miles',
    '1721 Wisconsin Ave NW'],
    ['Sweet green',
    '2.0 Miles',
    '1044 Wisconsin Ave NW'],
    ['Fruitive',
    '4.0 Miles',
    '1094 Palmer Alley NW'],
    ['Protein Bar and Kitchen',
    '4.9 Miles',
    '398 7th St NW'],
    ['Falafel Inc',
    '2.4 Miles',
    '1210 Potomac St NW'],
    ['The Little Beet',
    '4.2 Miles',
    '1212 18th St NW'],
    ['Peacock Cafe',
    '2.4 Miles',
    '20036, 3251 Prospect St NW'],
    ['Elizabeths gone raw',
    '3.7 Miles',
    '1341 L St NW'],
    ['Jardenea',
    '2.6 Miles',
    '2430 Pennsylvania Ave NW']
    ]

positives = [
    ['1789',
    '2.2 Miles',
    '1226 36th St NW'],
    ['Equinox',
    '3.3 Miles',
    '818 Connecticut Ave NW'],
    ['Fiola',
    '4.9 Miles',
    '601 Pennsylvania Avenue Northwest'],
    ['Bourbon Steak',
    '2.2 Miles',
    '2800 Pennsylvania Ave NW'],
    ['The Palm Washington DC',
    '3.5 Miles',
    '1225 19th St NW'],
    ['Thomas Sweet',
    '2.1 Miles',
    '3214 P St NW'],
    ['Insomnia Cookies',
    '2.3 Miles',
    '3204 O St NW'],
    ['Olivia Macaron',
    '1.8 Miles',
    '3222 M St NW'],
    ['Crepe away',
    '2.9 Miles',
    '2001 L St NW'],
    ['District Doughnut',
    '1.7 Miles',
    '3327 Cadys Alley NW']
    ]


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
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Hello, " \
                    "how are you feeling today?"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me how you're feeling."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_mood_attributes(mood):
    return {"myMood": mood}


def set_mood_in_session(intent, session):
    """ Sets the mood in the session and prepares the speech to reply to the
    user.
    """




    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'mood' in intent['slots']:
        current_mood = intent['slots']['mood']['value']
        session_attributes = create_mood_attributes(current_mood)

        sentiment = get_semantics(str(current_mood))

        if sentiment == 'POSITIVE':
            pos = random.randint(0, len(positives))
            restaurant = positives[pos]

        elif sentiment == 'NEGATIVE':
            neg = random.randint(0, len(negatives))
            restaurant = negatives[neg]

        elif sentiment == 'NEUTRAL' or sentiment == 'MIXED':
            mix = random.randint(0, len(neutrals))
            restaurant = neutrals[mix]

        speech_output = "Based on your mood, you might enjoy " + restaurant[0] + '. It is ' + \
        restaurant[1] + ' away.'

        reprompt_text = None
    else:
        speech_output = "I'm not sure what your mood is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your mmod is. " \
                        "You can tell me your mood by saying, " \
                        "I'm feeling happy."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_food_from_mood(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "myMood" in session.get('attributes', {}):
        current_mood = session['attributes']['myMood']

        sentiment = get_semantics(str(current_mood))


        if sentiment == 'POSITIVE':
            pos = random.randint(0, len(positives))
            restaurant = positives[pos]
        elif sentiment == 'NEGATIVE':
            neg = random.randint(0, len(negatives))
            restaurant = negatives[neg]
        elif sentiment == 'NEUTRAL' or sentiment == 'MIXED':
            mix = random.randint(0, len(neutrals))
            restaurant = neutrals[mix]


        speech_output = "Based on your previous mood,  " + current_mood + ", you should try " + restaurant[0] + '. It is ' + \
                        restaurant[1] + ' away.'

        should_end_session = False
    else:
        speech_output = "I'm not sure what your mood is. " \
                        "You can say, I'm feeling happy."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_semantics(mood):

    mood_sentiment = client.detect_sentiment(
    Text=mood,
    LanguageCode='en'
    )

    str_request = mood_sentiment['Sentiment']

    return str_request



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "setMoodIntent":
        return set_mood_in_session(intent, session)
    elif intent_name == "getFoodIntent":
        return get_food_from_mood(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
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
