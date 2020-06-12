

from Button_Feature import get_url_buttons


def show_feature_details(sender_id, payload, feature_dict):
    text = ""
    url = ""

    print(payload)
    for feature in feature_dict:
        if feature == payload:
            text, url = feature_dict[feature]['text'], feature_dict[feature]['url']
            break

    request_body = get_url_buttons(sender_id, text, url)

    return request_body



# feature_dict = {}
# sender_id="123"
# # global feature_dict
# if len(feature_dict) == 0:
#     collection = db["platform_features"]
#     feature_dict = collection.find()[0]
# request_body = show_feature_details(sender_id, "volunteers", feature_dict)
# print(request_body)
