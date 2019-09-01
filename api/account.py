import re
from api.serializers import *
from api.common import *


def account(request):
    """
    Creates Json response with account menu
    :param request: POST request from "Account" dialogflow intent
    :return: Json response that contains spoken and display prompt and also list as Dialogflow conversation item
    """
    speech_text_pl = "Którą z poniższych opcji zarządzania kontem wybierasz?"
    display_text_pl = "Którą z poniższych opcji zarządzania kontem wybierasz?"
    list_pl = {
        "intent": "actions.intent.OPTION",
        "data": {
            "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
            "listSelect": {
                "items": [
                    {
                        "optionInfo": {
                            "key": "Zaloguj",
                            "synonyms": [
                                "Zaloguj się",
                                "Zaloguj mnie"
                            ]
                        },
                        "title": "Zaloguj"
                    },
                    {
                        "optionInfo": {
                            "key": "Zarejestruj się",
                            "synonyms": [
                                "Załóż konto",
                                "Utwórz konto",
                                "Stwórz konto",
                                "Zarejestruj mnie",
                                "Zarejestruj",
                                "Załóż mi konto"
                            ]
                        },
                        "title": "Zarejestruj się"
                    },
                    {
                        "optionInfo": {
                            "key": "Zmień dane konta",
                            "synonyms": [
                                "Edytuj moje dane",
                                "Edytuj dane mojego konta",
                            ]
                        },
                        "title": "Zmień ustawienia konta"
                    },
                    {
                        "optionInfo": {
                            "key": "Zmień jedno ustawienie konta",
                            "synonyms": [
                                "Edytuj tylko jedną informację na moim koncie",
                                "Edytuj moje konto",
                            ]
                        },
                        "title": "Zmień jedno z ustawień konta"
                    },
                    {
                        "optionInfo": {
                            "key": "Wyświetl wszystkie dane konta",
                            "synonyms": [
                                "Pokaż wszystkie dane mojego konta",
                                "Wyświetl wszystkie informacje na moim koncie",
                            ]
                        },
                        "title": "Wyświetl wszystkie ustawienia konta"
                    },
                    {
                        "optionInfo": {
                            "key": "Wyświetl jedną konkretną informację o użytkowniku",
                            "synonyms": [
                                "Wyświetl tylko jedną informację o użytkowniku",
                                "Wyświetl jedną konkretną informację",
                            ]
                        },
                        "title": "Wyświetl jedną konkretną informację o użytkowniku"
                    },
                    {
                        "optionInfo": {
                            "key": "Usuń konto",
                            "synonyms": [
                                "Usuń",
                                "Usuń moje konto",
                            ]
                        },
                        "title": "Usuń konto"
                    }
                ]
            }
        }
    }
    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                      {"title": "Inne"}]

    speech_text_en = "Which of the following account management options you choose?"
    display_text_en = "Which of the following account management options you choose?"
    list_en = {
        "intent": "actions.intent.OPTION",
        "data": {
            "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
            "listSelect": {
                "items": [
                    {
                        "optionInfo": {
                            "key": "Sign in",
                            "synonyms": [
                                "login",
                                "log on"
                            ]
                        },
                        "title": "Sign in"
                    },
                    {
                        "optionInfo": {
                            "key": "Sign up",
                            "synonyms": [
                                "Register",
                                "Enroll"
                            ]
                        },
                        "title": "Sign up"
                    },
                    {
                        "optionInfo": {
                            "key": "Change account details",
                            "synonyms": [
                                "Edit my profile",
                                "Edit account",
                                "Change my account data"
                            ]
                        },
                        "title": "Change account details"
                    },
                    {
                        "optionInfo": {
                            "key": "Change one account detail",
                            "synonyms": [
                                "Change in my profile one info",
                                "Change my one account information"
                            ]
                        },
                        "title": "Change one account detail"
                    },
                    {
                        "optionInfo": {
                            "key": "View all account details",
                            "synonyms": [
                                "Give me all account details",
                                "Give me all data account",
                            ]
                        },
                        "title": "View all account details"
                    },
                    {
                        "optionInfo": {
                            "key": "View one specific user information",
                            "synonyms": [
                                "Give me one my account detail",
                                "View my single account information",
                                "View one user information"
                            ]
                        },
                        "title": "View one specific user information"
                    },
                    {
                        "optionInfo": {
                            "key": "Delete account",
                            "synonyms": [
                                "Delete",
                                "Delete my account",
                            ]
                        },
                        "title": "Delete account"
                    }
                ]
            }
        }
    }
    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                      {"title": "Others"}]

    with open('api/response.json') as json_file:
        account_menu = json.load(json_file)

    part_to_modify = account_menu['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = display_text_pl
        part_to_modify['systemIntent'] = list_pl
        part_to_modify['richResponse']['suggestions'] = suggestions_pl
    else:
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = display_text_en
        part_to_modify['systemIntent'] = list_en
        part_to_modify['richResponse']['suggestions'] = suggestions_en

    account_menu['payload']['google'] = part_to_modify
    return account_menu


def access_google_account(request):
    """
    Call registration process by return appropriate Json to Dialogflow service
    :param request: POST request from "Access Google account" dialogflow intent
    :return: JSON with content that calls actions.intent.SIGN_IN intent
    """
    with open('api/sign_in_response.json') as json_file:
        response = json.load(json_file)
    return response


def after_sign_in(request):
    """
    Creates Json response that is spoken/display after sign in or sign up
    :param request: POST request from "After sign in" Dialogflow intent
    :return: Json with spoken and display text with info after sign in and also with Dialogflow suggestions
    """
    token = request.data['originalDetectIntentRequest']['payload']['user']['accessToken']
    user = User.objects.get(auth_token=token)
    profile = Profile.objects.get(user=user)
    speech_text_pl = "Witaj {} {}. Jesteś już zalogowany! W czym mogę Ci jeszcze pomóc?".format(profile.name, profile.surname)
    display_text_pl = "Witaj {} {}. Jesteś już zalogowany! W czym mogę Ci jeszcze pomóc?".format(profile.name, profile.surname)
    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                      {"title": "Inne"}]

    speech_text_en = "Hello {} {}. You are already logged in! How can I help you?".format(profile.name, profile.surname)
    display_text_en = "Hello {} {}. You are already logged in! How can I help you?".format(profile.name, profile.surname)
    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                      {"title": "Others"}]

    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']['richResponse']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
        part_to_modify['suggestions'] = suggestions_pl
    else:
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
        part_to_modify['suggestions'] = suggestions_en

    response['payload']['google']['richResponse'] = part_to_modify

    return response


def delete_account(request):
    """
    Creates a JSON with the question of whether or not to delete the user's account
    :param request: POST request from 'Delete account' Dialogflow intent
    :return: Json with the question of whether or not to delete the user's account
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz usunąć konta, ponieważ jeszcze go u nas nie posiadasz. Jeśli chcesz założyć " \
                         "konto best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz usunąć konta. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't delete your account because you don't have it yet. If you want to create a best " \
                         "transport Polska account, select Sign up option below"
    display_spoken_en = "You can't delete the account. Create an account by selecting Sign up option below"

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            if language == 'pl':
                suggestions_pl = [{"title": "Tak"}, {"title": "Nie"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Czy na pewno chcesz usunąć swoje konto " \
                                                                               "w serwisie best transport Polska?"
                part_to_modify['items'][0]['simpleResponse']['displayText'] = "Czy na pewno chcesz usunąć swoje konto?"
                part_to_modify['suggestions'] = suggestions_pl
            else:
                suggestions_en = [{"title": "Yes"}, {"title": "No"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Are you sure you want to delete your " \
                                                                               "account on the best transport Polska website?"
                part_to_modify['items'][0]['simpleResponse']['displayText'] = "Are you sure you want to delete your " \
                                                                               "account?"
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/Deleteaccount-followup".format(
                    session_id),
                "lifespanCount": 2
            }
            list_with_context = list()
            list_with_context.append(context)
            response["outputContexts"] = list_with_context
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def delete_account_yes(request):
    """
    Deletes user account
    :param request: POST request from "Delete account - yes" Dialogflow intent
    :return: Json with information about account deleted
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']['accessToken']
    with open('api/response.json') as json_file:
        response = json.load(json_file)
    part_to_modify = response['payload']['google']['richResponse']
    profile_token = Token.objects.get(key=access_token)
    user = profile_token.user
    profile = Profile.objects.get(user=user)
    if profile.company is not None:
        profile.company.delete()
    if profile.address is not None:
        profile.address.delete()
    profile.user.delete()
    profile.delete()

    language = request.data['queryResult']['languageCode']
    if language == 'pl':
        suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                          {"title": "Inne"}]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Twoje konto Best Transport zostało usunięte. " \
                                                                       "Którą z poniższych opcji wybierasz?"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Konto usunięte. Którą z poniższych opcji wybierasz? "
        part_to_modify['suggestions'] = suggestions_pl
    else:
        suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},{"title": "Account"},
                          {"title": "Others"}]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Your Best Transport account has been deleted. " \
                                                                       "Which of the following options do you choose?"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Account deleted. Which of the following options " \
                                                                      "do you choose?"
        part_to_modify['suggestions'] = suggestions_en

        response['payload']['google']['richResponse'] = part_to_modify
    return response


def delete_account_no(request):
    """
    Creates Json with information after select item "No delete account"
    :param request: POST request from "Delete account - no" Dialogflow intent
    :return: Json with information after select item "No delete account"
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)
    part_to_modify = response['payload']['google']['richResponse']

    language = request.data['queryResult']['languageCode']
    if language == 'pl':
        suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                          {"title": "Inne"}]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Ok, nie ma sprawy. Którą z poniższych opcji " \
                                                                       "wybierasz?"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Ok. Którą z poniższych opcji wybierasz? "
        part_to_modify['suggestions'] = suggestions_pl
    else:
        suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                          {"title": "Others"}]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "OK no problem. Which of the following options " \
                                                                       "do you choose??"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Ok. Which of the following options you choose?"
        part_to_modify['suggestions'] = suggestions_en

        response['payload']['google']['richResponse'] = part_to_modify
    return response


def one_user_information(request):
    """
    Loads appropriate Json that contains Dialogflow list with user information to choose.
    :param request: POST request from "One user information" dialogflow intent
    :return: Json that contains Dialogflow list with user information to choose.
    """
    language = request.data['queryResult']['languageCode']
    if language == "pl":
        with open('api/one_user_information_pl.json') as json_file:
            response = json.load(json_file)
    else:
        with open('api/one_user_information_en.json') as json_file:
            response = json.load(json_file)
    return response


def tell_name(request):
    """
    Search user name in user account settings and return it in JSON
    :param request: POST request from "Tell name" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with user name
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić imienia, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz założyć konto " \
                         "w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić imienia. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't display the name, because you don't have an account yet. If you " \
                         "want to create a best transport Poland account, select the option \"Sign up\" below."
    display_spoken_en = "You can't display your name. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            if language == "pl":
                response_spoken_pl = "Imie na Twoim koncie to {}".format(profile.name)
                display_spoken_pl = profile.name
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            else:
                response_spoken_en = "The name on your account is {}".format(profile.name)
                display_spoken_en = profile.name
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_surname(request):
    """
    Search user surname in user account settings and return it in JSON
    :param request: POST request from "Tell surname" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with user surname
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić nazwiska, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz założyć konto " \
                         "w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić nazwiska. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't display the surname, because you don't have an account yet. If you " \
                         "want to create a best transport Poland account, select the option \"Sign up\" below."
    display_spoken_en = "You can't display your surname. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            if language == "pl":
                response_spoken_pl = "Nazwisko na Twoim koncie to {}".format(profile.surname)
                display_spoken_pl = profile.surname
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            else:
                response_spoken_en = "The surname on your account is {}".format(profile.surname)
                display_spoken_en = profile.surname
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_username(request):
    """
    Search username in user account settings and return it in JSON
    :param request: POST request from "Tell surname" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with username
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz uzyskać nazwy Twojego konta, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz uzyskać nazwy Twojego konta. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't obtain your account name because you don't have an account yet. If you want to " \
                         "create a best transport Poland account, select the option \"Sig up\" below"
    display_spoken_en = "You can't obtain your account name. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            if language == "pl":
                response_spoken_pl = "Nazwa twojego konta to {}".format(user.username)
                display_spoken_pl = user.username
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            else:
                response_spoken_en = "The username of your account is {}".format(user.username)
                display_spoken_en = user.username
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_email(request):
    """
    Search user email in user account settings and return it in JSON
    :param request: POST request from "Tell email" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with user email
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz pobrać adresu email, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz pobrać adresu email. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't get the email address because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't get the email address. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            if language == "pl":
                response_spoken_pl = "Adres email jaki jest zapisany w ustawieniach konta to {}".format(profile.email)
                display_spoken_pl = profile.email
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},{"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            else:
                response_spoken_en = "Email address saved on your account settings is {}".format(profile.email)
                display_spoken_en = profile.email
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_phone_number(request):
    """
    Search user phone number in user account settings and return it in JSON
    :param request: POST request from "Tell phone number" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with user phone number
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić swojego numeru telefonu, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić swojego numeru telefonu. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't view your phone number because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't view your phone number. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            if language == "pl":
                response_spoken_pl = "Numer telefonu jaki zapisałeś w ustawieniach"
                display_spoken_pl = profile.phone_number
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            else:
                response_spoken_en = "Phone number that you saved in your setings"
                display_spoken_en = profile.phone_number
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},{"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_tax_number(request):
    """
    Search user tax number in user account settings and return it in JSON
    :param request: POST request from "Tell tax number" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with user tax number
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić Twojego numeru podatnika, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić Twojego numeru płatnika. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't view your tax number because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't view your tax number. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            if language == "pl" and profile.tax_number != "":
                response_spoken_pl = "Numer podatnika na Twoim koncie to {}".format(profile.tax_number)
                display_spoken_pl = profile.tax_number
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and profile.tax_number != "":
                response_spoken_en = "Your tax number on your account is {}".format(profile.tax_number)
                display_spoken_en = profile.tax_number
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz zapisanego numeru podatnika w ustawieniach konta"
                display_spoken_pl = "Nie masz zapisanego numeru podatnika na Twoim koncie"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},{"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "You don't have tax number saved in your account"
                display_spoken_en = "You don't have any tax number on you account"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_place_name(request):
    """
    Search user place name in user account settings and return it in JSON
    :param request: POST request from "Tell place name" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with user place name
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić swojego miejsca zamieszkania, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić swojego miejsca zamieszkania,. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't view your place of residence because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't view your place of residence. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            place_name = profile.address
            if language == "pl" and place_name.place_name != "":
                response_spoken_pl = "Miejsce zamieszkania jakie jest zapisane na Twoim koncie to {}".format(place_name.place_name)
                display_spoken_pl = place_name.place_name
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and place_name.place_name != "":
                response_spoken_en = "The place of residence that is saved in your account is {}".format(place_name.place_name)
                display_spoken_en = place_name.place_name
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz zapisanego miejsca zamieszkania na Twoim koncie"
                display_spoken_pl = "Nie masz zapisanego miejsca zamieszkania na Twoim koncie"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "You don't have place of residence saved in your account"
                display_spoken_en = "You don't have any place of residence"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_street(request):
    """
    Search user street in user account settings and return it in JSON
    :param request: POST request from "Tell street" Dialogflow intent or from apropriate selected in from Dialogflow list
    :return: Json with user street
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić ulicy, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić ulicy. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't get your street because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't get your street. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            address = profile.address
            if language == "pl" and address.street != "":
                response_spoken_pl = "Nazwa ulicy zapisana na Twoim koncie to {}".format(address.street)
                display_spoken_pl = address.street
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and address.street != "":
                response_spoken_en = "The name of street that is saved in your account is {}".format(address.street)
                display_spoken_en = address.street
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz zapisanej żadnej informacji o ulicy na Twoim koncie"
                display_spoken_pl = "Nie masz informacji o ulicy na Twoim koncie"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en-us":
                response_spoken_en = "You don't have any street information saved on your account."
                display_spoken_en = "You don't have street information on your account"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_post_code(request):
    """
    Search user post code in user account and return it in JSON
    :param request: POST request from "Tell post code" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with user post code
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić Twojego kodu pocztowego, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić Twojego kodu pocztowego. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't view your post code because you don't have an account yet. If you want to create a Best" \
                         " Transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't view your post code. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            address = profile.address
            if language == "pl" and address.post_code != "":
                response_spoken_pl = "Twój kod pocztowy to {}".format(address.post_code)
                display_spoken_pl = address.post_code
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and address.post_code != "":
                response_spoken_en = "Your postal code is {}".format(address.post_code)
                display_spoken_en = address.post_code
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz żadnej informacji o Twoim kodzie pocztowym w ustawieniach"
                display_spoken_pl = "Nie masz informacji o kodzie pocztowym w ustawieniach"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "You don't have any post code information in your settings."
                display_spoken_en = "You don't have any post code information in your settings"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_post_place(request):
    """
    Search user post place in user account settings and return it in JSON
    :param request: POST request from "Tell post place" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with user post place
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić miejscowości twojej poczty, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić miejscowości twojej poczty. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't view your post place, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign ign\" below"
    display_spoken_en = "You can't view your post place. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            address = profile.address
            if language == "pl" and address.place != "":
                response_spoken_pl = "Miejscowość Twojej poczty to {}".format(address.place)
                display_spoken_pl = address.place
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and address.place != "":
                response_spoken_en = "Your post place is {}".format(address.place)
                display_spoken_en = address.place
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz zapisanej żadnej informacji o Twojej poczcie"
                display_spoken_pl = "Nie masz zapisanej żadnej informacji o Twojej poczcie"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},{"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "You don't have any information about your post place"
                display_spoken_en = "You don't have any information about your post place"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_country(request):
    """
    Search user country in user account settings and return it in JSON
    :param request: POST request from "Tell country" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with user country
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić kraju, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić kraju. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't view your country because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't view your country. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            address = profile.address
            if language == "pl" and address.country != "":
                response_spoken_pl = "Kraj w ustawieniach twojego konta to {}".format(address.country)
                display_spoken_pl = address.country
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and address.country != "":
                response_spoken_en = "The country in settings of your account is {}".format(address.country)
                display_spoken_en = address.country
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz żadnej informacji o kraju na Twoim koncie"
                display_spoken_pl = "Nie masz żadnej informacji o kraju na Twoim koncie"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en-us":
                response_spoken_en = "You don't have any country within information saved on your account"
                display_spoken_en = "You don't have country within information on your account"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_company_tax_number(request):
    """
    Search company tax number in user account settings
    :param request: POST request from "Tell company tax number" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with company tax number for user account
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz uzyskać numeru podatkowego dla firmy zapisanej na Twoim koncie, ponieważ nie posiadasz " \
                         "jeszcze konta. Jeśli chcesz założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz uzyskać numeru płatnika dla firmy zapisanej na Twoim koncie. Załóż konto przez " \
                        "wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't obtain a tax number for a company registered on your account, because you don't " \
                         "have an account yet. If you want to create a best transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't obtain a tax number for a company registered on your account. Create an account by selecting " \
                        "the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            company = ""
            if profile.company:
                company = profile.company

            if language == "pl" and company != "" and company.tax_number != "":
                response_spoken_pl = "Numer płatnika dla Twojej firmy to {}".format(company.tax_number)
                display_spoken_pl = company.tax_number
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and company != "" and company.tax_number != "":
                response_spoken_en = "The tax number for the company registered on your account is {}".format(company.tax_number)
                display_spoken_en = company.tax_number
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz żadnej firmy na Twoim profilu"
                display_spoken_pl = "Nie masz żadnej firmy na Twoim profilu"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "You don't have any company on your profile"
                display_spoken_en = "You don't have any company on your profile"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_company_email(request):
    """
    Search company email in user account settings
    :param request: POST request from "Tell company email" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with company email
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz uzyskać adresu email twojej firmy, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz uzyskać adresu email twojej firmy. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't obtain email address to your company, because you do not have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't obtain email address to your company. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            company = ""
            if profile.company:
                company = profile.company

            if language == "pl" and company != "" and company.email != "":
                response_spoken_pl = company.email
                display_spoken_pl = company.email
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and company != "" and company.email != "":
                response_spoken_en = "The email address for the company saved on your profile is {}".format(company.email)
                display_spoken_en = company.email
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie posiadasz na koncie żadnej firmy, a tym samym jej adresu email"
                display_spoken_pl = "Nie masz firmy, a tym samym jej adresu email"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "You don't have any company on your account, and also company's email address"
                display_spoken_en = "You don't have a company and its email address also"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_company_phone_number(request):
    """
    Search company phone number in user account settings
    :param request: POST request from "Tell company phone number" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with company phone number
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę wyświetlić numeru telefonu Twojej firmy, ponieważ nie posiadasz jeszcze " \
                         "konta. Jeśli chcesz założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę wyświetlić numeru telefonu Twojej firmy. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't display your business phone number, because you do not have an account yet. If you " \
                         "want to create a best transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "I cant't display your business phone number. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            company = ""
            if profile.company:
                company = profile.company

            if language == "pl" and company != "" and company.phone_number != "":
                response_spoken_pl = "Telefon do Twojej firmy"
                display_spoken_pl = company.phone_number
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and company != "" and company.phone_number != "":
                response_spoken_en = "Phone number to your company {}".format(company.phone_number)
                display_spoken_en = company.phone_number
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie mogę znaleźć numeru telefonu do Twojej firmy, ponieważ nie masz go zapisanego " \
                                     "w ustawieniach konta."
                display_spoken_pl = "Nie masz w ustawieniach numeru telefonu do firmy"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en-us":
                response_spoken_en = "I can't find a phone number for your company because you don't have it in your " \
                                     "account settings."
                display_spoken_en = "You don't have a business phone number in your account settings"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_company_name(request):
    """
    Search company name in user account settings
    :param request: POST request from "Tell company name" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with company name
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie masz żadnej firmy w informacjach Twojego konta, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie masz żadnej firmy ani konta w naszym serwisie. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You don't have any company and any account in our service, because you don't have an account yet. If you" \
                         " want to create a best transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You don't have any company and any account in our service. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            address = ""
            if profile.company and profile.company.address:
                address = profile.company.address

            if language == "pl" and address != "" and address.place_name != "":
                response_spoken_pl = "Nazwa firmy którą znalazłem to {}".format(address.place_name)
                display_spoken_pl = address.place_name
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and address != "" and address.place_name != "":
                response_spoken_en = "The name of the company I found is {}".format(address.place_name)
                display_spoken_en = address.place_name
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz żadnej firmy w naszym serwisie"
                display_spoken_pl = "Nie masz żadnej firmy w naszym serwisie"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "You don't have any company in our service"
                display_spoken_en = "You don't have any company in our service"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_company_street(request):
    """
    Search company street in user account settings
    :param request: POST request from "Tell company street" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with company street
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę uzyskać nazwy ulicy dla Twojej firmy, ponieważ nie posiadasz jeszcze konta. " \
                         "Jeśli chcesz założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę uzyskać nazwy ulicy dla Twojej firmy. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't get a street name for your business, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "I can't get a street name for your business. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            address = ""
            if profile.company and profile.company.address:
                address = profile.company.address

            if language == "pl" and address != "" and address.street != "":
                response_spoken_pl = "Nazwa ulicy gdzie mieści się twoja firma to {}".format(address.street)
                display_spoken_pl = address.street
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and address != "" and address.street != "":
                response_spoken_en = "Street name where your company is located is {}".format(address.street)
                display_spoken_en = address.street
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz żadnej firmy w ustawieniach konta"
                display_spoken_pl = "Nie masz żadnej firmy w ustawieniach konta"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "You don't have any company in the account settings"
                display_spoken_en = "You don't have any company in the account settings"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_company_post_code(request):
    """
    Search company post code in user account settings
    :param request: POST request from "Tell company post code" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with company post code
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę tego dla Ciebie zrobić, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę tego dla Ciebie zrobić. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't do this for you, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "I can't do this for you. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            address = ""
            if profile.company and profile.company.address:
                address = profile.company.address

            if language == "pl" and address != "" and address.post_code != "":
                response_spoken_pl = "Kod pocztowy firmy to {}".format(address.post_code)
                display_spoken_pl = address.post_code
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and address != "" and address.post_code != "":
                response_spoken_en = "Post code for your company is {}".format(address.post_code)
                display_spoken_en = address.post_code
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz informacji o kodzie pocztowym dla jakielkolwiek firmy."
                display_spoken_pl = "Nie masz informacji o kodzie pocztowym dla jakielkolwiek firmy"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "You don't have information about the postal code for any company"
                display_spoken_en = "You don't have information about the postal code for any company"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_company_post_place(request):
    """
    Search company post place in user account settings
    :param request: POST request from "Tell company post place" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with company post place
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę tego dla Ciebie zrobić, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę tego dla Ciebie zrobić. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't do this for you, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "I can't do this for you. Create an account by selecting the option below \"Sign up\'"

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            address = ""
            if profile.company and profile.company.address:
                address = profile.company.address

            if language == "pl" and address != "" and address.post_place != "":
                response_spoken_pl = "Miejsce poczty dla firmy zapisanej w ustawieniach to {}".format(address.post_place)
                display_spoken_pl = address.post_place
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and address != "" and address.post_place != "":
                response_spoken_en = "Place of Post for the company saved in settings is {}".format(address.post_place)
                display_spoken_en = address.post_place
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz żadnej tego typu informacji w ustawieniach konta"
                display_spoken_pl = "Nie masz żadnej tego typu informacji w ustawieniach konta"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "You do not have any such information in the account settings"
                display_spoken_en = "You do not have any such information in the account settings"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_company_country(request):
    """
    Search company country in user account settings
    :param request: POST request from "Tell company country" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with company country
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić kraju dla firmy na Twoim koncie, ponieważ nie posiadasz jeszcze konta. " \
                         "Jeśli chcesz założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić kraju dla firmy na Twoim koncie. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't display the country for the company in your account, because you don't have an account yet. " \
                         "If you want to create a best transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't display the country for the company in your account. Create an account by selecting the " \
                        "option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            address = ""
            if profile.company and profile.company.address:
                address = profile.company.address

            if language == "pl" and address != "" and address.country != "":
                response_spoken_pl = "Kraj w którym znajduje się firma to {}".format(address.country)
                display_spoken_pl = address.country
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en" and address != "" and address.country != "":
                response_spoken_en = "The company country in information of your account is {}".format(address.country)
                display_spoken_en = address.country
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en
            elif language == "pl":
                response_spoken_pl = "Nie masz żadnej takiej informacji"
                display_spoken_pl = "Nie masz żadnej takiej informacji"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "You don't have any such information"
                display_spoken_en = "You don't have any such information"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def tell_all_account_information(request):
    """
    Retrieve all account information
    :param request: POST request from "Tell all account information" Dialogflow intent
    :return: JSON with all account settings
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić ustawień swojego konta, ponieważ jeszcze go nie posiadasz. " \
                         "Jeśli chcesz założyć konto best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić ustawień swojego konta. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't display your account settings because you don't have it yet. If you want to create " \
                         "a best transport Polska account, select the option Sign up below"
    display_spoken_en = "You can't display your account settings. Create an account by selecting the option below Sign up"

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            data = {
                "name": profile.name,
                "surname": profile.surname,
                "username": profile.user.username,
                "email": profile.email,
                "phone number": profile.phone_number,
                "tax number": profile.tax_number if profile.tax_number else "",
                "place name": profile.address.place_name if profile.address else "",
                "street": profile.address.street if profile.address else "",
                "post code": profile.address.post_code if profile.address else "",
                "post place": profile.address.post_place if profile.address else "",
                "country": profile.address.country if profile.address else "",
                "company place name": profile.company.address.place_name if profile.company else "",
                "company street": profile.company.address.street if profile.company else "",
                "company post code": profile.company.address.post_code if profile.company else "",
                "company post place": profile.company.address.post_place if profile.company else "",
                "company country": profile.company.address.country if profile.company else "",
                "company email": profile.company.email if profile.company else "",
                "company phone number": profile.company.phone_number if profile.company else "",
                "company tax number": profile.company.tax_number if profile.company else ""
            }

            speech_text_pl = "Wyświetlam wszystkie ustawienia Twojego konta. W czym mogę Ci jeszcze pomóc? "
            display_text_pl = "Wyświetlam wszystkie ustawienia Twojego konta. W czym mogę Ci jeszcze pomóc?"
            basic_card_pl = {
                "basicCard": {
                    "title": "Ustawienia konta",
                    "formattedText": "___Nazwa konta:___  {}  \n__Imię:__  {}  \n__Nazwisko:__  {}  \n__Email:__  {}  \n"
                                     "__Numer telefonu:__  {}  \n__Numer płatnika:__  {}  \n__Miejscowość zamieszkania:__"
                                     "  {}  \n__Ulica:__  {}  \n__Kod pocztowy:__  {}  \n__Poczta:__  {}  \n__Kraj:__  {}"
                                     "  \n  \n  \n__Nazwa firmy:__  {}  \n__Ulica firmy:__  {}  \n__Kod pocztowy:__  {}  \n"
                                     "__Poczta:__  {}  \n__Kraj:__  {}  \n__Email firmy:__  {}  \n__Numer telefonu:__  {}  \n"
                                     "__Numer płatnika:__  {}"
                        .format(data["username"],data["name"], data["surname"], data["email"], data["phone number"], data["tax number"],
                                data["place name"], data["street"], data["post code"], data["post place"],
                                data["country"], data["company place name"], data["company street"], data["company post code"],
                                data["company post place"], data["company country"], data["company email"],
                                data["company phone number"], data["company tax number"])
                }
            }
            suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                              {"title": "Inne"}]

            speech_text_en = "I display all settings of your account. What can I help you with?"
            display_text_en = "I display all settings of your account. What can I help you with?"
            basic_card_en = {
                "basicCard": {
                    "title": "Account settings",
                    "formattedText": "___Account name:___  {}  \n__Name:__  {}  \n__Surname:__  {}  \n__Email:__  {}  \n"
                                     "__Phone number:__  {}  \n__Tax number:__  {}  \n__Residence place:__"
                                     "  {}  \n__Street:__  {}  \n__Post code:__  {}  \n__Post place:__  {}  \n__Country:__  {}"
                                     "  \n  \n  \n__Company name:__  {}  \n__Company street:__  {}  \n__Post code:__  {}  \n"
                                     "__Post place:__  {}  \n__Country:__  {}  \n__Company Email:__  {}  \n__Phone number:__  {}  \n"
                                     "__Tax number:__  {}"
                        .format(data["username"], data["name"], data["surname"], data["email"], data["phone number"],
                                data["tax number"], data["place name"], data["street"], data["post code"], data["post place"],
                                data["country"], data["company place name"], data["company street"],
                                data["company post code"], data["company post place"], data["company country"], data["company email"],
                                data["company phone number"], data["company tax number"])
                }
            }
            suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                              {"title": "Others"}]

            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']

            if request.data['queryResult']['languageCode'] == 'pl':
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                part_to_modify['items'].append(basic_card_pl)
                part_to_modify['suggestions'] = suggestions_pl
            else:
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                part_to_modify['items'].append(basic_card_en)
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def ask_change_account_settings(request):
    """
    Creates response with prompting user to change his company or personal data on account settings
    :param request: POST request from "Ask change account settings" Dialogflow intent
    :return: JSON with response prompting user to change his company or personal data on account settings
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę zmienić żadnych ustawień, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę zmienić żadnych ustawień. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't change any settings, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "I can't change any settings. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            if language == "pl":
                response_spoken_pl = 'Jeśli chcesz zmienić swoje dane osobowe w naszym serwisie wybierz "Dane osobowe".' \
                                     ' Jeśli natomiast chcesz zmienić dane firmy na twoim koncie wybierz "Dane firmy".'
                display_spoken_pl = 'Jeśli chcesz zmienić dane osobowe wybierz "Dane osobowe". Jeśli chcesz zmienić ' \
                                    'dane firmy wybierz "Dane firmy".'
                suggestions_pl = [{"title": "Dane osobowe"}, {"title": "Dane firmy"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = 'If you want to change your personal data in our service, select "Personal data". ' \
                                     'If you want to change the company\'s data in your account, select "Company data".'
                display_spoken_en = 'If you want to change your personal information, select "Personal data". If you ' \
                                    'want to change the company\'s data, select "Company data".'
                suggestions_en = [{"title": "Personal data"}, {"title": "Company data"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def change_personal_data_settings(request):
    """
    Creates a question with summarized data to be changed
    :param request: POST request from "Change personal data settings" Dialogflow intent
    :return: JSON with summarized data to be changed
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę zmienić żadnych ustawień, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę zmienić żadnych ustawień. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't change any settings, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "I can't change any settings. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            parameters_from_request = request.data["queryResult"]["parameters"]
            if language == "pl":
                entities_pl = {'First_name': 'imię', 'Surname': "nazwisko", 'Email': 'email', 'telephone-number': 'numer telefonu',
                               'geo-city': 'miejsce zamieszkania', 'post-code': 'kod pocztowy','geo-country': 'kraj',
                               'tax_number': "numer płatnika"}
                response_pl = "Czy na pewno chcesz zmienić "
                for k,v in parameters_from_request.items():
                    if v != "" and k in entities_pl:
                        response_pl += entities_pl[k] + " na " + v + ", "
                response_pl = response_pl[:-2]
                response_pl += "?"
                suggestions_pl = [{"title": "Tak"}, {"title": "Nie"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = response_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                entities_en = {'First_name': 'name', 'Surname': "surname", 'Email': 'email',
                               'telephone-number': 'phone number', 'geo-city': 'residence place', 'post-code': 'post code',
                               'geo-country': 'country', 'tax_number': "tax number"}
                response_en = "Are you sure you want to change "
                for k, v in parameters_from_request.items():
                    if v != "" and k in entities_en:
                        response_en += entities_en[k] + " to " + v + ", "
                response_en = response_en[:-2]
                response_en += "?"
                suggestions_en = [{"title": "Yes"}, {"title": "No"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = response_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def change_personal_settings_yes(request):
    """
    Change user personal data in database
    :param request: POST request from "Change personal settings - yes" Dialogflow intent
    :return: JSON with info about data has been changed
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę tego dla Ciebie zrobić, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę tego dla Ciebie zrobić. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't do this for you, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "I can't do this for you. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            parameters_from_request = request.data["queryResult"]["outputContexts"]
            parameters = dict()
            for i in parameters_from_request:
                if "parameters" in i:
                    parameters = i["parameters"]

            for k, v in parameters.items():
                if k == "First_name":
                    profile.name = v
                elif k == "Surname":
                    profile.surname = v
                elif k == "Email":
                    profile.email = v
                elif k == "telephone-number":
                    profile.phone_number = v
                elif k == "geo-city":
                    profile.address.place_name = v
                    profile.address.post_place = v
                elif k == "post-code":
                    profile.address.post_code = v
                elif k == "geo-country":
                    profile.address.country = v
                elif k == "tax_number":
                    profile.address.tax_number = v

            profile.address.save()
            profile.save()

            if language == "pl":
                response_spoken_pl = "Twoje dane osobowe zostały zmienione. W czym mogę Ci jeszcze pomóc?"
                display_spoken_pl = "Twoje dane osobowe zostały zmienione. W czym mogę Ci jeszcze pomóc?"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},{"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "Your personal details have been changed. How can I help you?"
                display_spoken_en = "Your personal details have been changed. How can I help you?"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},{"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def change_personal_settings_no(request):
    """
    Creates response about no change user personal data
    :param request: POST request from "Change personal settings - no" Dialogflow intent
    :return: JSON with info about data hasn't been changed
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę tego dla Ciebie zrobić, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę tego dla Ciebie zrobić. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't do this for you, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "I can't do this for you. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            if language == "pl":
                response_spoken_pl = "Nie ma sprawy, wybierz co chcesz jeszcze zrobić."
                display_spoken_pl = "Nie ma sprawy, wybierz co chcesz jeszcze zrobić."
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "No problem, choose what you want to do."
                display_spoken_en = "No problem, choose what you want to do."
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def change_company_data_settings(request):
    """
    Creates a question with summarized user company data to be changed
    :param request: POST request from "Change company data settings" Dialogflow intent
    :return: JSON with summarized data to be changed
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę zmienić danych twojej firmy, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę zmienić danych twojej firmy. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't change data for your company, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "I can't change data for you company. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            parameters_from_request = request.data["queryResult"]["parameters"]

            if language == "pl":
                entities_pl = {'Email': 'email firmy','telephone-number': 'firmowy numer telefonu',
                               'geo-city': 'pocztę firmy', 'post-code': 'kod pocztowy dla firmy', 'geo-country': 'kraj firmy',
                               'tax_number': 'numer płatnika'}
                response_pl = "Czy na pewno chcesz zmienić "
                for k, v in parameters_from_request.items():
                    if v != "" and k in entities_pl:
                        response_pl += entities_pl[k] + " na " + v + ", "
                response_pl = response_pl[:-2]
                response_pl += "?"
                suggestions_pl = [{"title": "Tak"}, {"title": "Nie"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = response_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                entities_en = {'Email': 'company email', 'telephone-number': 'phone number for company',
                               'geo-city': 'company post office', 'post-code': 'post code for company',
                               'geo-country': 'company country', 'tax_number': 'tax number'}
                response_en = "Are you sure you want to change "
                for k, v in parameters_from_request.items():
                    if v != "" and k in entities_en:
                        response_en += entities_en[k] + " to " + v + ", "
                response_en = response_en[:-2]
                response_en += "?"
                suggestions_en = [{"title": "Yes"}, {"title": "No"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = response_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def change_company_settings_yes(request):
    """
    Change user company data in database
    :param request: POST request from "Change company settings - yes" Dialogflow intent
    :return: JSON with info about data has been changed
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę tego dla Ciebie zrobić, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę tego dla Ciebie zrobić. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't do this for you, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "I can't do this for you. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            profile_token = Token.objects.get(key=access_token)
            user = profile_token.user
            profile = Profile.objects.get(user=user)
            parameters_from_request = request.data["queryResult"]["outputContexts"]
            parameters = dict()
            for i in parameters_from_request:
                if "parameters" in i:
                    parameters = i["parameters"]

            for k, v in parameters.items():
                if k == "Email":
                    profile.company.email = v
                elif k == "telephone-number":
                    profile.company.phone_number = v
                elif k == "geo-city":
                    profile.company.address.post_place = v
                elif k == "post-code":
                    profile.company.address.post_code = v
                elif k == "geo-country":
                    profile.company.address.country = v
                elif k == 'tax_number':
                    profile.company.address.tax_number = v

            profile.company.address.save()
            profile.company.save()
            profile.save()

            if language == "pl":
                response_spoken_pl = "Dane firmy zapisanej na Twoim koncie zostały zmienione. W czym mogę Ci jeszcze pomóc?"
                display_spoken_pl = "Dane firmy zostały zmienione. W czym mogę Ci jeszcze pomóc?"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},{"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en-us":
                response_spoken_en = "The company's details saved on your account have been changed. How can I help you?"
                display_spoken_en = "Your company details have been changed. How can I help you?"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},{"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def change_company_settings_no(request):
    """
    Create response about no change user company data
    :param request: POST request from "Change company settings - no" Dialogflow intent
    :return: JSON with info about data hasn't been changed
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę tego dla Ciebie zrobić, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę tego dla Ciebie zrobić. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't do this for you, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "I can't do this for you. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            if language == "pl":
                response_spoken_pl = "Nie ma sprawy, wybierz co chcesz jeszcze zrobić."
                display_spoken_pl = "Nie ma sprawy, wybierz co chcesz jeszcze zrobić."
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en-us":
                response_spoken_en = "No problem, choose what you want to do."
                display_spoken_en = "No problem, choose what you want to do."
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def change_one_account_information(request):
    """
    Load appropriate Json with user information to choose from the list
    :param request: POST request from "Change one account information" dialogflow intent
    :return: Json with user information to choose from the list
    """
    language = request.data['queryResult']['languageCode']
    if language == "pl":
        with open('api/change_one_information_pl.json') as json_file:
            response = json.load(json_file)
    elif language == "en-us":
        with open('api/change_one_information_en.json') as json_file:
            response = json.load(json_file)
    return response


def change_user_name_list(request):
    """
    Create response with "trigger_change_name" Dialogflow event
    :param request: POST request from one of the items in list
    :return: JSON with "trigger_change_name" Dialogflow event
    """
    language = request.data['queryResult']['languageCode']
    if language == "pl":
        response = {
            "followupEventInput": {
                "name": "trigger_change_name",
                "languageCode": "pl"
            }
        }
    elif language == "en-us":
        response = {
            "followupEventInput": {
                "name": "trigger_change_name",
                "languageCode": "en-us"
            }
        }
    return response


def change_user_name(request):
    """
    Create response with prompting user to give his new name
    :param request: POST request from "Change user name" Dialogflow intent
    :return: JSON with response prompting user to give his new name
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę zmienić dla Ciebie imienia w ustawieniach twojego konta, ponieważ nie posiadasz jeszcze " \
                         "konta. Jeśli chcesz założyć konto Best Transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę zmienić imienia w Twoich ustawieniach. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't do this for you, because you do not have an account yet. If you want to create a Best" \
                         " Transport Polska account, select the option Sign up below"
    display_spoken_en = "I can't do this for you. Create an account by selecting the option below Sign up"

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            if language == "pl":
                response_spoken_pl = "Nie ma sprawy. Podaj teraz tylko i wyłącznie swoje nowe imię"
                display_spoken_pl = "Podaj teraz tylko i wyłącznie swoje nowe imię"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en-us":
                response_spoken_en = "No prolem. Give me now only your new name"
                display_spoken_en = "No prolem. Give me now only your new name"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                  {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/Changeusername_followup".format(
                    session_id),
                "lifespanCount": 2
            }
            list_with_context = list()
            list_with_context.append(context)
            response["outputContexts"] = list_with_context

            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def change_user_name_custom(request):
    """
    Change user name in database
    :param request: POST request from "Change user name - custom" Dialogflow intent
    :return: Json with info data has been changed
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']['accessToken']
    profile_token = Token.objects.get(key=access_token)
    user = profile_token.user
    profile = Profile.objects.get(user=user)
    profile.name = request.data['queryResult']['queryText']
    profile.save()
    with open('api/response.json') as json_file:
        response = json.load(json_file)
    part_to_modify = response['payload']['google']['richResponse']
    language = request.data['queryResult']['languageCode']

    if language == "pl":
        response_spoken_pl = "Twoje imię w ustawieniach konta zostało zmienione. Wybierz co chcesz jeszcze zrobić."
        display_spoken_pl = "Twoje imię zostało zmienione"
        suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                          {"title": "Inne"}]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
        part_to_modify['suggestions'] = suggestions_pl
    elif language == "en-us":
        response_spoken_en = "Your name in the account settings has been changed. Choose what you want to do next."
        display_spoken_en = "Your name has been changed. Choose what you want to do next."
        suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                          {"title": "Others"}]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
        part_to_modify['suggestions'] = suggestions_en

    response['payload']['google']['richResponse'] = part_to_modify
    return response


def change_user_surname_list(request):
    """
    Create response with "trigger_change_surname" Dialogflow event
    :param request: POST request from one of the items in list
    :return: JSON with "trigger_change_surname" Dialogflow event
    """
    language = request.data['queryResult']['languageCode']
    if language == "pl":
        response = {
            "followupEventInput": {
                "name": "trigger_change_surname",
                "languageCode": "pl"
            }
        }
    elif language == "en-us":
        response = {
            "followupEventInput": {
                "name": "trigger_change_surname",
                "languageCode": "en-us"
            }
        }
    return response


def change_user_surname(request):
    """
    Create response with prompting user to give his new surname
    :param request: POST request from "Change user surname" Dialogflow intent
    :return: JSON with response prompting user to give his new surname
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę zmienić dla Ciebie nazwiska w ustawieniach twojego konta, ponieważ nie posiadasz jeszcze " \
                         "konta. Jeśli chcesz założyć konto Best Transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę zmienić nazwiska w Twoich ustawieniach. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't change surname for you, because you do not have an account yet. If you want to create a Best" \
                         " Transport Polska account, select the option Sign up below"
    display_spoken_en = "I can't change surname for you. Create an account by selecting the option below Sign up"

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            if language == "pl":
                response_spoken_pl = "Nie ma sprawy. Podaj teraz, tylko i wyłącznie swoje nowe nazwisko"
                display_spoken_pl = "Podaj teraz, tylko i wyłącznie swoje nowe nazwisko"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en-us":
                response_spoken_en = "No prolem. Give me now only your new surname"
                display_spoken_en = "No prolem. Give me now only your new surname"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/Changeusersurname_followup".format(
                    session_id),
                "lifespanCount": 2
            }
            list_with_context = list()
            list_with_context.append(context)
            response["outputContexts"] = list_with_context

            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def change_user_surname_custom(request):
    """
    Change user surname in database
    :param request: POST request from "Change user surname - custom" Dialogflow intent
    :return: Json with info data has been changed
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']['accessToken']
    profile_token = Token.objects.get(key=access_token)
    user = profile_token.user
    profile = Profile.objects.get(user=user)
    profile.surname = request.data['queryResult']['queryText']
    profile.save()
    with open('api/response.json') as json_file:
        response = json.load(json_file)
    part_to_modify = response['payload']['google']['richResponse']
    language = request.data['queryResult']['languageCode']

    if language == "pl":
        response_spoken_pl = "Twoje nazwisko w ustawieniach konta zostało zmienione. Wybierz co chcesz jeszcze zrobić."
        display_spoken_pl = "Twoje nazwisko zostało zmienione"
        suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                          {"title": "Inne"}]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
        part_to_modify['suggestions'] = suggestions_pl
    elif language == "en-us":
        response_spoken_en = "Your surname in the account settings has been changed. Choose what you want to do next."
        display_spoken_en = "Your surname has been changed. Choose what you want to do next."
        suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                          {"title": "Others"}]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
        part_to_modify['suggestions'] = suggestions_en

    response['payload']['google']['richResponse'] = part_to_modify
    return response


def change_user_username_list(request):
    """
    Create response with "trigger_change_username" Dialogflow event
    :param request: POST request from one of the items in list
    :return: JSON with "trigger_change_username" Dialogflow event
    """
    language = request.data['queryResult']['languageCode']
    if language == "pl":
        response = {
            "followupEventInput": {
                "name": "trigger_change_username",
                "languageCode": "pl"
            }
        }
    elif language == "en-us":
        response = {
            "followupEventInput": {
                "name": "trigger_change_username",
                "languageCode": "en-us"
            }
        }
    return response


def change_user_username(request):
    """
    Create response with prompting user to give his new username
    :param request: POST request from "Change user username" Dialogflow intent
    :return: JSON with response prompting user to give his new username
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie mogę tego zmienić nie posiadasz jeszcze " \
                         "konta. Jeśli chcesz założyć konto Best Transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie mogę tego zmienić w ustawieniach. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "I can't change it, because you do not have an account yet. If you want to create a Best" \
                         " Transport Polska account, select the option Sign up below"
    display_spoken_en = "I can't change it. Create an account by selecting the option below Sign up"

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            if language == "pl":
                response_spoken_pl = "Nie ma sprawy. Podaj teraz, tylko i wyłącznie nową nazwę twojego konta"
                display_spoken_pl = "Podaj teraz tylko i wyłącznie nową nazwę twojego konta"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en-us":
                response_spoken_en = "No prolem. Give me now only your new username."
                display_spoken_en = "No prolem. Give me now only your new username"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                  {"title": "Account"}, {"title": "Others"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/Changeuserusername_followup".format(
                    session_id),
                "lifespanCount": 2
            }
            list_with_context = list()
            list_with_context.append(context)
            response["outputContexts"] = list_with_context

            return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def change_user_username_custom(request):
    """
    Change user username in database
    :param request: POST request from "Change user username - custom" Dialogflow intent
    :return: Json with info data has been changed
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']['accessToken']
    profile_token = Token.objects.get(key=access_token)
    user = profile_token.user
    user.username = request.data['queryResult']['queryText']
    user.save()
    with open('api/response.json') as json_file:
        response = json.load(json_file)
    part_to_modify = response['payload']['google']['richResponse']
    language = request.data['queryResult']['languageCode']

    if language == "pl":
        response_spoken_pl = "Nazwa użytkownika Twojego konta została zmieniona. Wybierz co chcesz jeszcze zrobić."
        display_spoken_pl = "Nazwa użytkownika została zmieniona"
        suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                          {"title": "Inne"}]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
        part_to_modify['suggestions'] = suggestions_pl
    elif language == "en-us":
        response_spoken_en = "Username in our account has been changed. Choose what you want to do next."
        display_spoken_en = "Username has been changed. Choose what you want to do next."
        suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                          {"title": "Others"}]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_en
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_en
        part_to_modify['suggestions'] = suggestions_en

    response['payload']['google']['richResponse'] = part_to_modify
    return response