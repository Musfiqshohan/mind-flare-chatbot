from urllib.parse import urlencode
from urllib.request import Request, urlopen

def send_single_message(sender_id, message_text, PAGE_TOKEN):

    request_body = get_text_message(sender_id, message_text)

    post_request_typing = Request('https://graph.facebook.com/v5.0/me/messages?access_token=' + PAGE_TOKEN,
                                  urlencode(request_body).encode())
    response_typing = urlopen(post_request_typing).read().decode()
    return


def get_text_message(sender_id, message, ):
    request_body = {
        'recipient': {
            'id': sender_id
        },
        'message': {"text": message}
    }

    return request_body
