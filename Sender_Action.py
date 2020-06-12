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
