
# from flask_ngrok import run_with_ngrok

import credentials, requests
from flask import Flask, request
import gunicorn
app = Flask(__name__)

WEBHOOK_VERIFY_TOKEN="Mind-Flare-507163"
PAGE_TOKEN= "EAAINYZCdZAxdwBAEXxiZA7ZAJ4UoUo2pMMObh9yg3D5k0eQ9twvF9IpI02yAdxPQNIPmoLFGCwrorpLM9gDoZAvZCCZBGsr0z8xZBehQA2ICaziO0jtxxhPZBhObTg3KgCKrcgpqvMtdGFpMietZAQwexfqzxdZAoqVZBFhZBsgOcYVkWwwZDZD"
# Adds support for GET requests to our webhook
@app.route('/webhook',methods=['GET'])
def webhook():
    verify_token = request.args.get("hub.verify_token")
    # Check if sent token is correct
    # if verify_token == credentials.WEBHOOK_VERIFY_TOKEN:
    if verify_token == WEBHOOK_VERIFY_TOKEN:
        # Responds with the challenge token from the request
        return request.args.get("hub.challenge")
    return 'Unable to authorise.'



# Adds support for POST requests
@app.route("/webhook", methods=['POST'])
def webhook_handle():
    data = request.get_json()
    print(data)
    message = data['entry'][0]['messaging'][0]['message']
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    if message['text']:
        request_body = {
            'recipient': {
                'id': sender_id
            },
            'message': {"text": "hello, world! good luck"}
        }
        response = requests.post('https://graph.facebook.com/v5.0/me/messages?access_token=' + PAGE_TOKEN,
                                 json=request_body).json()
        return response
    return 'ok'


@app.route('/')
def hello_world():
    return 'Hello, World1!'

if __name__ == "__main__":
    app.run(threaded=True, port=5000)
