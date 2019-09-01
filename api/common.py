import json
from rest_framework.authtoken.models import Token


def check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en, display_spoken_en):
    """
    Checks if token from request exists in database
    :param access_token: access token from request
    :param language: which language from request
    :param response_spoken_pl: content for spoken response in polish
    :param display_spoken_pl: content for written response in polish
    :param response_spoken_en: content for spoken response in english
    :param display_spoken_en: content for written response in polish
    :return: Json with info that the token does not exist or the "token exist" string
    """
    suggestions_pl_lack_account = [{"title": "Zarejestruj się"}, {"title": "Oferty"}, {"title": "Zlecenia"},
                                   {"title": "Zapytania"}, {"title": "Konto"}, {"title": "Inne"}]
    suggestions_en_lack_account = [{"title": "Sign up"}, {"title": "Offers"}, {"title": "Orders"},
                                   {"title": "Inquiries"}, {"title": "Account"}, {"title": "Others"}]

    if Token.objects.filter(key=access_token).count() == 0:
        with open('api/response.json') as json_file:
            response = json.load(json_file)
        part_to_modify = response['payload']['google']['richResponse']
        if language == 'pl':
            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
            part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
            part_to_modify['suggestions'] = suggestions_pl_lack_account
            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
            part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
            part_to_modify['suggestions'] = suggestions_en_lack_account
            response['payload']['google']['richResponse'] = part_to_modify
            return response
    return "token exist"
