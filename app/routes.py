from app import app
from flask import Flask, request, jsonify, json, url_for, redirect, session, render_template
from app import eurekabot 

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
        #return render_template('index.html', labels=labels, categories=cat_list)
        #return 'Get request'

    elif request.method == 'POST':
        return 'Post request'

        #return redirect(url_for('predict_kaggle'))

    return '<h2>Request method type not supported</h2>' 
    
@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')

@app.route('/api/lrtbot', methods=['GET','POST'])
def lrtbot():
    #print('LRT Bot')
    if request.method == 'GET':
        print('LRT Bot GET method')
            
        # Parse the query params
        token = request.args.get('hub.verify_token')

        return eurekabot.verify_fb_token(token)
    
    elif request.method == 'POST':
        print('LRT Bot POST method')

        #Check if there is a header
        if request.headers['Content-Type'] != 'application/json':
            print('No header')
            return 'No Json content found'

        output = request.get_json()
        print("JSON input: ", output)

        for event in output['entry']:
            messaging = event['messaging']
            time_epoch = event['time']
            for message in messaging:
                recipient_id = message['sender']['id']
                
                #Check if there is a postback.payload key inside message
                #If there is, then process the postback
                if message.get('postback') and message['postback'].get('payload'):
                    postback = message['postback']['payload']
                    eurekabot.parse_postbacks(recipient_id, postback)

                elif message.get('message'):
                    #if user sends a quick reply
                    quick_reply = message['message'].get('quick_reply')
                    print(quick_reply)
                    if quick_reply and quick_reply.get('payload'):
                        payload = quick_reply.get('payload')
                        eurekabot.parse_quickreply(recipient_id, payload, time_epoch)
                        break

                    #Facebook Messenger ID for user so we know where to send response back to
                    response = message['message'].get('text')
                    if response:
                        eurekabot.parse_response(recipient_id, response)
                        break
                        
                    #if user sends us a GIF, photo,video, or any other non-text item
                    attachments = message['message'].get('attachments')
                    if attachments:
                        attachment = attachments[0]
                        attachment_type = attachment['type']
                        #response for send location in directions option
                        if attachment_type == 'location':
                            coordinates = attachment['payload']['coordinates']
                            eurekabot.directions_get_location(recipient_id, coordinates)

        return "Message Processed"

    return 'Request method type not supported'

