from urllib.parse import urlencode
from urllib.request import Request, urlopen


def send_single_message_reqbody(request_body, PAGE_TOKEN):


    post_request_typing = Request('https://graph.facebook.com/v5.0/me/messages?access_token=' + PAGE_TOKEN,
                                  urlencode(request_body).encode())
    response_typing = urlopen(post_request_typing).read().decode()

    return


def get_url_buttons(sender_id, message_text, url):
    request_body = {
        'recipient': {
            'id': sender_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": message_text,
                    "buttons": [
                        {
                            "type": "web_url",
                            "url":  url,
                            "title": "Request Personal Volunteer"
                        },
                        {
                            "type": "postback",
                            "title": "Other features",
                            "payload": "features"
                        }
                    ]
                }
            }
        }

    }

    return request_body


def get_feature_buttons(sender_id, message_text):
    request_body = {
        'recipient': {
            'id': sender_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": message_text,
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Personal Volunteers",
                            "payload": "volunteers"
                        },
                        {
                            "type": "postback",
                            "title": "Expert Psychologist",
                            "payload": "psychologist"
                        },

                        # {
                        #     "type": "postback",
                        #     "title": "Blog for thoughts",
                        #     "payload": "blog"
                        # },
                        {
                            "type": "postback",
                            "title": "Psychological tests",
                            "payload": "tests"
                        }
                    ]
                }
            }
        }

    }

    return request_body

def get_more_feature_buttons(sender_id, message_text):
    request_body = {
        'recipient': {
            'id': sender_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": message_text,
                    "buttons": [
                        {
                            "type": "postback",
                            "title": "Blog for Thoughts",
                            "payload": "blog"
                        },
                        {
                            "type": "postback",
                            "title": "About us",
                            "payload": "about"
                        }
                    ]
                }
            }
        }

    }

    return request_body
