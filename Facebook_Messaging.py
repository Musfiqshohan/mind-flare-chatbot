


def get_text_message(message, sender_id):
    request_body = {
        'recipient': {
            'id': sender_id
        },
        'message': {"text": message}
    }

    return request_body


def get_sender_action(data):
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    request_body_on = {
        "recipient": {
            "id": sender_id
        },
        "sender_action": "typing_on"
    }

    request_body_off = {
        "recipient": {
            "id": sender_id
        },
        "sender_action": "typing_off"
    }

    return request_body_on, request_body_off



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


def get_buttons(data):
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']
    request_body = {
        'recipient': {
            'id': sender_id
        },
        # 'message': {"text": "hello, shohan I am fixed!"}
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": "বন্ধু কোনটা দেখতে চাও?",
                    "buttons": [
                        {
                            "type": "web_url",
                            "url": "https://www.messenger.com",
                            "title": "মাইন্ড ফ্লেয়ার"
                        },
                        {
                            "type": "web_url",
                            "url": "https://www.youtube.com/",
                            "title": "ইউটিউব দেখতে মন চায়"
                        }
                    ]
                }
            }
        }

    }

    return request_body
