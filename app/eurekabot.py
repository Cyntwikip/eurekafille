from flask import Flask, request, jsonify, json, url_for, redirect, session, render_template
from pymessenger.bot import Bot
from app import departures, directions, quiz
import random

ACCESS_TOKEN = 'EAALU1QUBIuYBAJqVfRTBssNcAx5sUe7pPZCcP9o0dnkZBOb6AKZCOK9p6oaxQ37SEYXu2IrfHA2LS2VShX005ZC9OPk6E9ZBJ4BmgmRB9YJIj9ZCO19V8dOlnESz8ZCyFKtALnIZCxMkz6q8ZA2TT3Uhxep784zFeYndX8KBpCAUOULO4Cj1IEujc'
VERIFY_TOKEN = 'eurekafille'
bot = Bot(ACCESS_TOKEN)

def verify_fb_token(token_sent):
    '''
    take token sent by facebook and verify it matches the verify token you sent
    if they match, allow the request, else return an error 
    '''
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

def get_default_message():
    '''
    Default message
    '''
    msg = [
        '''Did you know? LRT1 is the oldest running railway company in the Philippines? That’s your LRT1 Fact for the day! Please type ‘start’ to get started!''',
        '''At LRT1, we aim to give commuters #BiyahengBetterEveryday because you all deserve it! Now, please type ‘start’ to get started!''',
        '''Trivia Time! There are over 500,000 passengers daily riding the LRT1 with you! Please type ‘start’ to get started!''',
        '''You can do it! Whatever you’re going through right now, there will be better days ahead. #WeCare #BiyahengBetterEveryday. Please type ‘start’ to get started!''',
        '''We’re improving everyday! It’s our aim to give you #BiyahengBetterEveryday. Please type ‘start’ to get started!''',
        '''Move on, move on din, bes! Just like the  LRT trains you might miss if you don’t hurry up! Please type ‘start’ to get started.''',
        '''Umulan man, aaraw din! Today is a great day! Please type ‘start’ to get started.''',
        '''Hi! How are you today? Please type ‘start’ to get started.'''
        ]
    return random.choice(msg)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    '''
    sends user the text message provided via input response parameter
    '''
    bot.send_text_message(recipient_id, response)
    return

def parse_postbacks(recipient_id, postback):
    '''
    Parses the postback event that was triggered.
    '''
    
    postback_splitted = postback.split('_')

    if postback == 'EUREKAFILLE':
        #parse_response(recipient_id, 'Get Started')
        choices = [
            {
                "type":"postback",
                "title":"Directions",
                "payload":"Request_Directions"
            },
            {
                "type":"postback",
                "title":"Departure Times",
                "payload":"Request_Time"
            }
        ]
        bot.send_button_message(recipient_id, 'Hi! How may I help you?', choices)

    elif postback == 'EUREKAFILLE_QUIZ':
        choices = [
            {
                "type":"postback",
                "title":"Yes, bring it on!",
                "payload":"Quiz_Accept"
            },
            {
                "type":"postback",
                "title":"No, I’m good.",
                "payload":"Quiz_Reject"
            }
        ]
        bot.send_button_message(recipient_id, 'Want to check out today’s COFFEE TRIVIA QUIZ?', choices)

    elif postback == "Quiz_Accept":
        quiz.start_game(recipient_id)
    elif postback == "Quiz_Reject":
        bot.send_text_message(recipient_id, 'Thank you! See you next time.')
    # elif postback_splitted[0] == "QuizAnswer":
    #     quiz.answer_question(recipient_id, postback_splitted[1])
    elif postback == 'Request_Directions':
        directions.directions_menu(recipient_id)
    elif postback == 'Request_Time':
        departures.departure_menu(recipient_id)

    # elif postback == 'Request_About':
    #     bot.send_text_message(recipient_id, 'Dummy about')
    # elif postback == 'Request_Feedback':
    #     bot.send_text_message(recipient_id, 'Dummy feedback')

    # # postback for request directions: ingress
    # elif len(postback_splitted)==2 and postback_splitted[0]=='DepartureIngress':
    #     ingress = postback_splitted[1]
    #     print(ingress)
    #     departures.departure_ingress(recipient_id, ingress)
    # # postback for request directions: egress
    # elif len(postback_splitted)==3 and postback_splitted[0]=='DepartureEgress':
    #     ingress = postback_splitted[1]
    #     egress = postback_splitted[2]
    #     print(egress)
    #     departures.departure_egress(recipient_id, ingress, egress)
    else:
        bot.send_text_message(recipient_id, 'Unhandled postback')
    return
    
def parse_response(recipient_id, response):
    '''
    Parses the user's response.
    '''        
    start = ['start', 'ok', 'good morning', 'good afternoon', 
    'good evening', 'game', 'g', 'yes', 'hi', 'hello', 'hey']
    if response.lower() in start:
        print('Get Started will be displayed! :)')
        parse_postbacks(recipient_id, 'EUREKAFILLE')
    elif response.lower() == 'quiz':
        print('Quiz will be displayed! :)')
        parse_postbacks(recipient_id, 'EUREKAFILLE_QUIZ')
    else:
        send_message(recipient_id, get_default_message())
        #print('Get Started will be displayed! :)')
        #parse_postbacks(recipient_id, 'EUREKAFILLE')
    return

def parse_quickreply(recipient_id, payload, time_epoch):
    '''
    Parses the user's quick reply response.
    '''        
    print(payload)
    response_splitted = payload.split('_')
    # postback for request departure: ingress
    if len(response_splitted)==2 and response_splitted[0]=='DepartureIngress':
        ingress = response_splitted[1]
        print(ingress)
        if ingress.startswith('Next'):
            slicing = ingress.replace('Next', '')
            departures.parse_ingress(recipient_id, int(slicing))
        elif ingress.startswith('Prev'):
            slicing = ingress.replace('Prev', '')
            departures.parse_ingress(recipient_id, int(slicing))
        else:
            departures.parse_egress(recipient_id, ingress, 0)
    # postback for request departure: egress
    elif len(response_splitted)==3 and response_splitted[0]=='DepartureEgress':
        ingress = response_splitted[1]
        egress = response_splitted[2]
        print(ingress, egress)
        if egress.startswith('Next'):
            slicing = egress.replace('Next', '')
            departures.parse_egress(recipient_id, ingress, int(slicing))
        elif egress.startswith('Prev'):
            slicing = egress.replace('Prev', '')
            departures.parse_egress(recipient_id, ingress, int(slicing))
        else:
            departures.parse_final(recipient_id, ingress, egress, time_epoch)
    # postback for request directions
    elif len(response_splitted)==2 and response_splitted[0]=='DirectionIngress':
        ingress = response_splitted[1]
        print(ingress)
        if ingress.startswith('Next'):
            slicing = ingress.replace('Next', '')
            directions.parse_ingress(recipient_id, int(slicing))
        elif ingress.startswith('Prev'):
            slicing = ingress.replace('Prev', '')
            directions.parse_ingress(recipient_id, int(slicing))
        else:
            directions.parse_station(recipient_id, ingress)
    elif response_splitted[0] == "QuizAnswer":
        quiz.answer_question(recipient_id, response_splitted[1])
    # if 1==2:
    #     pass
    else:
        bot.send_text_message(recipient_id, 'Unhandled quick reply')
    return

def directions_get_location(recipient_id, coordinates):
    directions.get_location(recipient_id, coordinates)
    return