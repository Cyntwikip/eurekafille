from flask import Flask, request, jsonify, json, url_for, redirect, session, render_template
from pymessenger.bot import Bot
from app import departures

ACCESS_TOKEN = 'EAALU1QUBIuYBAGgTmLKgqdgFVw7iVu1t0DU1Tt5GT3xFVcx8TtjqX0SGcPfIu42lU3x1xTFhWcFgvyEpQuvjnLDZB3utNM5KIZBZBqVBMSCwcr7bdY5ZAY2npmwPfycPDfFqjbAZBqBP19nvuT2ZCF50d4juzA5jGY15Yloio2cVqwYAc6jOt1'
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
    return "This is LRT chatbot"

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

    elif postback == 'Request_Directions':
        bot.send_text_message(recipient_id, 'Dummy directions')
    elif postback == 'Request_Time':
        #bot.send_text_message(recipient_id, 'Dummy time')
        departures.departure_menu(recipient_id)
    elif postback == 'Request_About':
        bot.send_text_message(recipient_id, 'Dummy about')
    elif postback == 'Request_Feedback':
        bot.send_text_message(recipient_id, 'Dummy feedback')
    # postback for request directions: ingress
    elif len(postback_splitted)==2 and postback_splitted[0]=='DepartureIngress':
        ingress = postback_splitted[1]
        print(ingress)
        departures.departure_ingress(recipient_id, ingress)
    # postback for request directions: egress
    elif len(postback_splitted)==3 and postback_splitted[0]=='DepartureEgress':
        ingress = postback_splitted[1]
        egress = postback_splitted[2]
        print(egress)
        departures.departure_egress(recipient_id, ingress, egress)
    else:
        bot.send_text_message(recipient_id, 'Unhandled postback')
    return
    
def parse_response(recipient_id, response):
    '''
    Parses the user's response.
    '''        
    if response.lower() == 'start':
        print('Get Started will be displayed! :)')
        parse_postbacks(recipient_id, 'EUREKAFILLE')
    else:
        send_message(recipient_id, get_default_message())
    return

def parse_quickreply(recipient_id, payload):
    '''
    Parses the user's quick reply response.
    '''        
    
    response_splitted = payload.split('_')
    # postback for request directions: ingress
    if len(response_splitted)==2 and response_splitted[0]=='DepartureIngress':
        ingress = response_splitted[1]
        print(ingress)
        departures.departure_ingress(recipient_id, ingress)
    # postback for request directions: egress
    elif len(response_splitted)==3 and response_splitted[0]=='DepartureEgress':
        ingress = response_splitted[1]
        egress = response_splitted[2]
        print(egress)
        departures.departure_egress(recipient_id, ingress, egress)
    else:
        bot.send_text_message(recipient_id, 'Unhandled quick reply')
    return