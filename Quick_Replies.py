from pymongo import MongoClient

from Text_Message import send_single_message

cluster = MongoClient(
    "mongodb://musfiq:shohan@mindflare-shard-00-00-sh7js.mongodb.net:27017,mindflare-shard-00-01-sh7js.mongodb.net:27017,mindflare-shard-00-02-sh7js.mongodb.net:27017/test?ssl=true&replicaSet=Mindflare-shard-0&authSource=admin&retryWrites=true&w=majority")
db = cluster["mindflare"]


def execute_intro(data):
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    message_text="Hi, I am your friend. I know I am not strong enough but I am improving and will try " \
                 "my best to serve you :D. Do you want to take a test? It consists of 20 questions"

    return get_quick_replies(sender_id,message_text)


def get_beck_result(beck_score):
    message_collection = db["mentalStateFormQuestion"]
    message_data = message_collection.find_one({"type": "messages"})

    if beck_score <= 3:
        state, message = "minimal", message_data['minimal']
    elif beck_score <= 8:
        state, message = "mild", message_data['mild']
    elif beck_score <= 14:
        state, message = "moderate", message_data['moderate']
    else:
        state, message = "severe", message_data['severe']

    return state, message

beck_score=0


def execute_psycho_test(sender_id, message , beck_questions, context_stack, PAGE_TOKEN):
    # sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    # message = data['entry'][0]['messaging'][0]['message']

    global beck_score
    if message == "No":
        beck_score += 1

    isEnd=False

    if len(beck_questions) == 0:
        state, beck_message=get_beck_result(beck_score)
        # message_text2="Thank you for your reply. According beck test, your" \
        #              "score is "+str(beck_score)+" which is a "+state+" situation. "+beck_message

        send_single_message(sender_id, "Thank you for your reply. According beck test, your"
                                       "score is "+str(beck_score)+" which is a "+state+" situation.", PAGE_TOKEN)

        send_single_message(sender_id, beck_message, PAGE_TOKEN)

        context_stack.pop() # "can we start?
        message_text = context_stack[-1][0]   # know features of our platform
        context_stack.pop()
        context_stack.append((message_text,None))

        isEnd=True
    else:
        message_text= beck_questions.pop()

    return isEnd, get_quick_replies(sender_id, message_text)


def get_quick_replies(sender_id, message_text):

    request_body = {
        'recipient': {
            'id': sender_id
        },
        "messaging_type": "RESPONSE",
        "message": {
            # "is_echo": False,
            # "text": "I look forward to the future with hope and enthusiasm.",
            "text": message_text,
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Yes",
                    "payload": "<POSTBACK_PAYLOAD>",

                }, {
                    "content_type": "text",
                    "title": "No",
                    "payload": "<POSTBACK_PAYLOAD>",

                }
            ]
        }

    }

    return request_body


# def get_quick_feature(sender_id, message_text):
#
#     request_body = {
#         'recipient': {
#             'id': sender_id
#         },
#         "messaging_type": "RESPONSE",
#         "message": {
#             # "is_echo": False,
#             # "text": "I look forward to the future with hope and enthusiasm.",
#             "text": message_text,
#             "quick_replies": [
#                 {
#                     "content_type": "text",
#                     "title": "Personal Volunteers \n",
#                     "payload": "volunteers",
#
#                 }, {
#                     "content_type": "text",
#                     "title": "Expert Psychologist \n",
#                     "payload": "psychologist",
#
#                 }
#                 # ,
#                 # {
#                 #     "content_type": "text",
#                 #     "title": "Blog for Thoughts",
#                 #     "payload": "blog",
#                 #
#                 # },{
#                 #     "content_type": "text",
#                 #     "title": "Psychological tests",
#                 #     "payload": "tests",
#                 #
#                 # }
#             ]
#         }
#
#     }
#
#     return request_body
