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
    bot.send_text_message(recipient_id, response)
    return "success"
    
@app.route('/api/lrtbot', methods=['GET','POST'])
def lrtbot():
    print('LRT Bot')
    if request.method == 'GET':
        #return 'Request method must be POST'
        # Your verify token. Should be a random string.
        #VERIFY_TOKEN = "eurekafille"
            
        # Parse the query params
        #mode = request.arg.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        return verify_fb_token(token)
            
        # Checks if a token and mode is in the query string of the request
        # if (mode and token) {
        
        #     # Checks the mode and token sent is correct
        #     if (mode == 'subscribe' and token == VERIFY_TOKEN) {
            
        #     # Responds with the challenge token from the request
        #     #console.log('WEBHOOK_VERIFIED');
        #     print('WEBHOOK_VERIFIED')
        #     res.status(200).send(challenge);
            
        #     } else {
        #     # Responds with '403 Forbidden' if verify tokens do not match
        #     res.sendStatus(403);      
        #     }
        # }
    
    elif request.method == 'POST':
        if request.headers['Content-Type'] != 'application/json':
            return 'No Json content found'

        print('User has sent something')
        #return str(request)
        output = request.get_json()
        print(output)
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # pass
                    #Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_message()
                        send_message(recipient_id, response_sent_text)
                    #if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
        return "Message Processed"


    return '<h2>Request method type not supported</h2>'

    # donors, c = donors_to_recommend(X_test, clf, index = 0, cluster_disp = False)
    # d = {'cluster': int(c), 'donors': donors['Donor ID'].tolist()}
    # print('Donors classified!')
    # return jsonify(d)


