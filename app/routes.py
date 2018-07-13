from app import app
from flask import Flask, request, jsonify, json, url_for, redirect, session, render_template
import pickle
import pandas as pd
from pymessenger.bot import Bot

ACCESS_TOKEN = 'EAALU1QUBIuYBAGgTmLKgqdgFVw7iVu1t0DU1Tt5GT3xFVcx8TtjqX0SGcPfIu42lU3x1xTFhWcFgvyEpQuvjnLDZB3utNM5KIZBZBqVBMSCwcr7bdY5ZAY2npmwPfycPDfFqjbAZBqBP19nvuT2ZCF50d4juzA5jGY15Yloio2cVqwYAc6jOt1'
VERIFY_TOKEN = 'eurekafille'
bot = Bot(ACCESS_TOKEN)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        
        #return render_template('index.html', labels=labels, categories=cat_list)
        return 'Get request'

    elif request.method == 'POST':
        return 'Post request'

        #return redirect(url_for('predict_kaggle'))

    return '<h2>Request method type not supported</h2>' 

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

#chooses a random message to send to the user
def get_message():
    #sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]
    # return selected item to the user
    #return random.choice(sample_responses)
    return "This is LRT chatbot"

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    #print("ID : ", recipient_id)
    #bot.send_text_message(recipient_id, response)
    bot.send_text_message(recipient_id, "This is LRT chatbot")
    return "success"

def parse_postbacks(recipient_id, postback):
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
            },
            # {
            #     "type":"postback",
            #     "title":"About the LRT1",
            #     "payload":"Request_About"
            # },
            # {
            #     "type":"postback",
            #     "title":"Send Feedback",
            #     "payload":"Request_Feedback"
            # },
        ]
        bot.send_button_message(recipient_id, 'Hi! How may I help you?', choices)

    elif postback == 'Request_Directions':
        bot.send_text_message(recipient_id, 'Dummy directions')
    elif postback == 'Request_Time':
        bot.send_text_message(recipient_id, 'Dummy time')
    elif postback == 'Request_About':
        bot.send_text_message(recipient_id, 'Dummy about')
    elif postback == 'Request_Feedback':
        bot.send_text_message(recipient_id, 'Dummy feedback')
    else:
        bot.send_text_message(recipient_id, 'Unhandled postback')
    return "success"
    

def parse_response(recipient_id, response):
    
    if response.lower() == 'button':
        choices = [
            {
                "type":"postback",
                "title":"Image",
                "payload":"Eureka_Image"
            },
            {
                "type":"postback",
                "title":"Text",
                "payload":"Eureka_Text"
            },
        ]
        bot.send_button_message(recipient_id, 'Get Started', choices)
        
    elif response.lower() == 'start':
        print('Get Started will be displayed! :)')
        parse_postbacks(recipient_id, 'EUREKAFILLE')
    else:
        send_message(recipient_id, response)
    return "success"
    
@app.route('/api/lrtbot', methods=['GET','POST'])
def lrtbot():
    print('LRT Bot')
    if request.method == 'GET':
        print('LRT Bot Get method')
        #return 'Request method must be POST'
        # Your verify token. Should be a random string.
        #VERIFY_TOKEN = "eurekafille"
            
        # Parse the query params
        #mode = request.arg.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        return verify_fb_token(token)
    
    elif request.method == 'POST':
        if request.headers['Content-Type'] != 'application/json':
            print('No header')
            return 'No Json content found'

        #print('User has sent something')
        #return str(request)
        output = request.get_json()
        print("JSON input: ", output)
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                recipient_id = message['sender']['id']
                
                if message.get('postback') and message['postback'].get('payload'):
                    postback = message['postback']['payload']
                    parse_postbacks(recipient_id, postback)
                    # if postback == 'EUREKAFILLE':
                    #     parse_response(recipient_id, 'Get Started')

                if message.get('message'):
                    # pass
                    #Facebook Messenger ID for user so we know where to send response back to
                    #recipient_id = message['sender']['id']
                    response = message['message'].get('text')
                    if response:
                        #response_sent_text = response
                        #send_message(recipient_id, response_sent_text)
                        parse_response(recipient_id, response)
                        
                    #if user sends us a GIF, photo,video, or any other non-text item
                    attachments = message['message'].get('attachments')
                    if attachments:
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
        return "Message Processed"


    return '<h2>Request method type not supported</h2>'

    # donors, c = donors_to_recommend(X_test, clf, index = 0, cluster_disp = False)
    # d = {'cluster': int(c), 'donors': donors['Donor ID'].tolist()}
    # print('Donors classified!')
    # return jsonify(d)


