

from Button_Feature import get_feature_buttons, get_more_feature_buttons, send_single_message_reqbody
from Quick_Replies import get_quick_replies
from Text_Message import get_text_message, send_single_message


# def process_received_message(message):
#
#     question= stk.pop() + message['text']
#
#     cur_func=  execution[question]
#
#     return cur_func




def get_intro(sender_id, PAGE_TOKEN, context_stack, decision_dict):

    send_single_message(sender_id, "Hi, I am your friend. I am here to give you mental support",PAGE_TOKEN)
    send_single_message(sender_id, "We have a psychological platform where you can get help from "
                                   "volunteers anonymously",PAGE_TOKEN)

                                   # "Do you want to take a test?"
                                   # " It consists of 20 questions", PAGE_TOKEN)

    question= "Do you want to know the features of our platform?"
    send_message= get_quick_replies(sender_id, question)

    context_stack.append((question, None))
    decision_dict[(question, "Yes")] = "get_feature_intro(sender_id, PAGE_TOKEN, context_stack)"
    decision_dict[(question, "No")] = "get_psycho_intro(sender_id, PAGE_TOKEN, context_stack, decision_dict)"

    return send_message





def get_psycho_intro(sender_id, PAGE_TOKEN, context_stack, decision_dict):
    send_single_message(sender_id, "Okay, then Do you want to take a psychological test to "
                                   "understand yourself if you need help?", PAGE_TOKEN)
    send_single_message(sender_id, "20 questions, \"yes\" if you agree, \"no\" otherwise ",PAGE_TOKEN)

    question = "Can we start?"
    send_message = get_quick_replies(sender_id, question)
    context_stack.append((question, None))
    decision_dict[(question, "Yes")] = "do_psycho_test(sender_id, message)"
    decision_dict[(question, "No")] = "reply_default()"

    return send_message
# cur_func=process_received_message("No")
# eval(cur_func)


def get_feature_intro(sender_id, PAGE_TOKEN, context_stack):
    send_single_message(sender_id, "We are the platform that is specially built for"
                                   "providing psychological help to university students", PAGE_TOKEN)

    send_single_message(sender_id, "We can help in these following ways.",PAGE_TOKEN)

    question = "Which feature do you want to know about?"
    send_message1 = get_feature_buttons(sender_id, question)
    send_single_message_reqbody(send_message1, PAGE_TOKEN)

    question = "and:"
    send_message2 = get_more_feature_buttons(sender_id, question)

    if context_stack[-1][0] != "Which feature do you want to know about?":
        question = "Which feature do you want to know about?"
        context_stack.append((question, None))

    return send_message2




