from app import app
import os
from flask import Flask, session

app.secret_key = "super secret key"

if __name__ == '__main__':
    # app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'
    # sess.init_app(app)

    port = int(os.environ.get('PORT', 5000)) #The port to be listening to — hence, the URL must be <hostname>:<port>/ inorder to send the request to this program
    app.run(host='0.0.0.0', port=port, debug=True) #Start listening

