
# from flask_ngrok import run_with_ngrok
from pymongo import MongoClient

import credentials, requests
from flask import Flask, request
import gunicorn

from Features import show_feature_details
from Messages import *
from Quick_Replies import get_quick_replies, execute_intro, execute_psycho_test
from Sender_Action import get_sender_action
from urllib.parse import urlencode
from urllib.request import Request, urlopen



cluster = MongoClient(
    "mongodb://musfiq:shohan@mindflare-shard-00-00-sh7js.mongodb.net:27017,mindflare-shard-00-01-sh7js.mongodb.net:27017,mindflare-shard-00-02-sh7js.mongodb.net:27017/test?ssl=true&replicaSet=Mindflare-shard-0&authSource=admin&retryWrites=true&w=majority")
db = cluster["mindflare"]
app = Flask(__name__)
# Callback URL= "https://mind-flare-chatbot.herokuapp.com/webhook"   for deploying from heroku
# #####################All options are not selected #################
WEBHOOK_VERIFY_TOKEN="Mind-Flare-507163"
PAGE_TOKEN= "EAAINYZCdZAxdwBAMLcoC3P6ZCg6xrhEu3KWAc72SNQnk1A5S7kYZAe2aCsMHPYQT4o1Hb2XIzPEduZBpHZAxZBhNW42GA7NYUUUj2rlYWpZAxdyXKwvC6awZBAtjIqOSUJJyFZCiCoEqjAlZCk0uDEW4eCXYUP1rpZBLZAMdf8PZCnYZBtDfQZDZD"



# Adds support for GET requests to our webhook
@app.route('/webhook',methods=['GET'])
def webhook():
    verify_token = request.args.get("hub.verify_token")
    # Check if sent token is correct
    # if verify_token == credentials.WEBHOOK_VERIFY_TOKEN:
    print("verify token",verify_token)
    if verify_token == WEBHOOK_VERIFY_TOKEN:
        # Responds with the challenge token from the request
        return request.args.get("hub.challenge")
    return 'Unable to authorise.'


def do_psycho_test(sender_id, message):
    global beck_questions
    if beck_questions == None:
        beck_questions = get_questions()

    isEnd, request_body = execute_psycho_test(sender_id, message, beck_questions, context_stack, PAGE_TOKEN)

    return request_body







position=0
current_state="Introduction"
prev_state="Introduction"
beck_questions=None
feature_dict={}
context_stack = []
decision_dict = {}
# Adds support for POST requests


def process_bot(sender_id, message, data):
    global position, current_state, prev_state, beck_questions

    # for typing on
    typing_req_on, typing_req_off = get_sender_action(data)  #
    post_request_typing = Request('https://graph.facebook.com/v5.0/me/messages?access_token=' + PAGE_TOKEN,
                                  urlencode(typing_req_on).encode())
    response_typing = urlopen(post_request_typing).read().decode()

    # send_single_message(sender_id, typing_req_on, PAGE_TOKEN)
    request_body = ""
    # if message:

    if len(context_stack) == 0:
        request_body = get_intro(sender_id, PAGE_TOKEN, context_stack, decision_dict)
    elif context_stack[-1][0] == "Can we start?" and context_stack[-1][1] == "Yes":
        func = decision_dict[context_stack[-1]]
        print(context_stack, decision_dict)
        request_body = eval(func)

    elif context_stack[-1][0] == "Which feature do you want to know about?":
        if message == "features":
            request_body = get_feature_intro(sender_id, PAGE_TOKEN, context_stack)
        else:
            global feature_dict
            if len(feature_dict) == 0:
                collection = db["platform_features"]
                feature_dict = collection.find()[0]

            print("all features", feature_dict)
            request_body = show_feature_details(sender_id, message, feature_dict)

    else:
        prev_context = context_stack.pop()
        new_context = (prev_context[0], message)
        context_stack.append(new_context)
        func = decision_dict[new_context]
        print(context_stack, decision_dict)
        request_body = eval(func)

    #
    # if prev_state == "Introduction":
    #     if message['text'] == "Yes":
    #         current_state = "Psycho_Test"
    #         beck_questions = get_questions()
    #     elif message['text'] == "No":
    #         current_state = prev_state
    #
    # if current_state == "Introduction":
    #     request_body = execute_intro(data)
    #     prev_state = "Introduction"
    #
    # if current_state == "Psycho_Test":
    #
    #     isEnd, request_body = execute_psycho_test(data, beck_questions)
    #     print("To user:", request_body)
    #     if isEnd == False:
    #         current_state = "Psycho_Test"
    #         prev_state= current_state
    #     else:
    #         prev_state=current_state
    #         current_state = "Motivation"
    #
    #
    #
    # print("Leaving the state as ", current_state)
    # pymessenger

    response = requests.post('https://graph.facebook.com/v5.0/me/messages?access_token=' + PAGE_TOKEN,
                             json=request_body).json()

    # for typing off
    post_request_typing = Request('https://graph.facebook.com/v5.0/me/messages?access_token=' + PAGE_TOKEN,
                                  urlencode(typing_req_off).encode())
    response_typing = urlopen(post_request_typing).read().decode()

    return response  #






@app.route("/webhook", methods=['POST'])
def webhook_handle():
    global position, current_state, prev_state, beck_questions
    data = request.get_json()
    print("Printing",data)
    message= None
    if 'message' in data['entry'][0]['messaging'][0]:
        message = data['entry'][0]['messaging'][0]['message']
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        #

        print("From User :", message)
        print("The state is", current_state,"but previous was",prev_state)

        if message['text']:
            return process_bot(sender_id, message['text'], data)
        else:
            return 'ok'

    elif 'postback' in data['entry'][0]['messaging'][0]:
        message = data['entry'][0]['messaging'][0]['postback']['payload']
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']

        print("postback", message)
        return process_bot(sender_id, message, data)

    else:
        return 'ok'


def get_questions():

    collection = db["mentalStateFormQuestion"]
    questions_dict = collection.find_one({"type": "questionsBeck"})

    questions=[]
    print("Questions",questions_dict)
    for key, value in questions_dict.items():
        if key != "_id" and key != "type":
            questions.append(key+": "+value)
            break

    questions.reverse()
    print("reveresed quesitons",questions)

    return questions



@app.route('/')
def hello_world():
    return 'Hello, World123!'

if __name__ == "__main__":

    app.run(threaded=True, port=5000)

