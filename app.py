import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')
 
# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC52be533d1a3715519852d4682b10d3f6'
    TWILIO_SYNC_SERVICE_SID = 'ISd49274b9c759c8419535a01807c17aed'
    TWILIO_API_KEY = 'SK98476ff207acbd92e4792b4dceffebe3'
    TWILIO_API_SECRET = '4z61iZPd4QHPMZuRqlABS6nQp2mlzxjk'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    tfn = request.form['text']

    with open('workfile.txt', 'w') as f:
        f.write(tfn)

    ptst = 'workfile.txt'

    return send_file(ptst, as_attachment=True)
    

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
