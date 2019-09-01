import re
from api.serializers import *
from api.common import *
from rest_framework.authtoken.models import Token
from datetime import datetime
from api.offers import *


def inquiries(request):
    """
    Creates Json response with inquiries menu
    :param request: POST request from "Inquiries" dialogflow intent
    :return: Json response that contains spoken and display prompt and also list as Dialogflow conversation item
    """
    speech_text_pl = "Którą opcję wybierasz?"
    display_text_pl = "Którą opcję wybierasz?"
    list_pl = {
        "intent": "actions.intent.OPTION",
        "data": {
            "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
            "listSelect": {
                "items": [
                    {
                        "optionInfo": {
                            "key": "Wyszukaj zapytanie/odpowiedź",
                            "synonyms": [
                                "Wyszukaj zapytanie",
                                "Wyszukaj odpowiedź"
                            ]
                        },
                        "title": "Wyszukaj zapytanie/odpowiedź"
                    },
                    {
                        "optionInfo": {
                            "key": "Tworzenie zapytania",
                            "synonyms": [
                                "Twórz zapytanie",
                                "Stwórz zapytanie"
                            ]
                        },
                        "title": "Tworzenie zapytania"
                    },
                    {
                        "optionInfo": {
                            "key": "Tworzenie zapytania do oferty/zamówienia",
                            "synonyms": [
                                "Twórz zapytanie do oferty",
                                "Twórz zapytanie do zamówienia",
                            ]
                        },
                        "title": "Tworzenie zapytania do oferty/zamówienia"
                    },
                    {
                        "optionInfo": {
                            "key": "Czy są nieprzeczytane odpowiedzi",
                            "synonyms": [
                                "Czy istnieją nieprzeczytane odpowiedzi"
                            ]
                        },
                        "title": "Czy są nieprzeczytane odpowiedzi"
                    },
                    {
                        "optionInfo": {
                            "key": "Nieprzeczytane odpowiedzi",
                            "synonyms": [
                                "Lista nieprzeczytanych odpowiedzi",
                                "Wyświetl nieprzeczytane odpowiedzi",
                            ]
                        },
                        "title": "Nieprzeczytane odpowiedzi"
                    },
                    {
                        "optionInfo": {
                            "key": "Odpowiedzi do zapytania",
                            "synonyms": [
                                "Pokaż odpowiedzi do zapytania",
                                "Przeczytaj odpowiedzi do danego zapytania",
                            ]
                        },
                        "title": "Odpowiedzi do zapytania"
                    },
                    {
                        "optionInfo": {
                            "key": "Odpowiedzi do oferty/zamówienia",
                            "synonyms": [
                                "Przeczytaj odpowiedzi do oferty",
                                "Przeczytaj odpowiedzi do zamówienia",
                            ]
                        },
                        "title": "Odpowiedzi do oferty/zamówienia"
                    },
                    {
                        "optionInfo": {
                            "key": "Odpowiedz",
                            "synonyms": [
                                "Odpowiedz na odpowiedź admina",
                                "Do kiedy oferta będzie aktualna",
                            ]
                        },
                        "title": "Odpowiedz"
                    }
                ]
            }
        }
    }
    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                      {"title": "Inne"}]

    speech_text_en = "Which option do you choose?"
    display_text_en = "Which option do you choose?"
    list_en = {
        "intent": "actions.intent.OPTION",
        "data": {
            "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
            "listSelect": {
                "items": [
                    {
                        "optionInfo": {
                            "key": "Search inquiry/answer",
                            "synonyms": [
                                "Search answer",
                                "Search inquiry"
                            ]
                        },
                        "title": "Search inquiry/answer"
                    },
                    {
                        "optionInfo": {
                            "key": "Create a inquiry",
                            "synonyms": [
                                "Craete query"
                            ]
                        },
                        "title": "Create a inquiry"
                    },
                    {
                        "optionInfo": {
                            "key": "Creating a inquiry for an offer/order",
                            "synonyms": [
                                "Creating a inquiry for an offer",
                                "Creating a inquiry for an order",
                            ]
                        },
                        "title": "Creating a inquiry for an offer/order"
                    },
                    {
                        "optionInfo": {
                            "key": "Are there unread responses",
                            "synonyms": [
                                "Do unread responses exist?"
                            ]
                        },
                        "title": "Are there unread responses"
                    },
                    {
                        "optionInfo": {
                            "key": "Unread responses",
                            "synonyms": [
                                "List with unread responses",
                                "Show unread responses",
                            ]
                        },
                        "title": "Unread responses"
                    },
                    {
                        "optionInfo": {
                            "key": "Answers to the inquiry",
                            "synonyms": [
                                "Answers to the query",
                                "Show answers to the query",
                            ]
                        },
                        "title": "Answers to the inquiry"
                    },
                    {
                        "optionInfo": {
                            "key": "Answers to the offer/order",
                            "synonyms": [
                                "Answers to the offer",
                                "Answers to the order",
                            ]
                        },
                        "title": "Answers to the offer/order"
                    },
                    {
                        "optionInfo": {
                            "key": "Reply to admin",
                            "synonyms": [
                                "Answer to admin"
                            ]
                        },
                        "title": "Reply to admin"
                    }
                ]
            }
        }
    }
    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                      {"title": "Others"}]

    with open('api/response.json') as json_file:
        inquiries = json.load(json_file)

    part_to_modify = inquiries['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = display_text_pl
        part_to_modify['systemIntent'] = list_pl
        part_to_modify['richResponse']['suggestions'] = suggestions_pl
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = display_text_en
        part_to_modify['systemIntent'] = list_en
        part_to_modify['richResponse']['suggestions'] = suggestions_en

    inquiries['payload']['google'] = part_to_modify
    return inquiries


def create_inquiry(request):
    """
    Creates response with prompting user to give the title of the inquiry that user is creating
    :param request: POST request from "Create inquiry" Dialogflow intent
    :return: JSON with prompting user to give the title of the inquiry that user is creating
    """
    with open('api/response.json') as json_file:
        inquiry = json.load(json_file)

    part_to_modify = inquiry['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Podaj tytuł Twojego zapytania"
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Podaj tytuł zapytania"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Give the title of the inquiry that " \
                                                                                       "you are creating"
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Give the title of the inquiry that " \
                                                                                       "you are creating"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                         {"title": "Account"},{"title": "Others"}]

    inquiry['payload']['google'] = part_to_modify
    return inquiry


def get_inquiry_title_ask_text(request):
    """
    Create inquiry with first data. Creates response with prompting user to give the text of the inquiry that user is creating
    :param request: POST request from "Get inquiry title ask text" Dialogflow intent
    :return: JSON with prompting user to give the text of the inquiry that user is creating
    """
    inquiry_title = request.data["queryResult"]["queryText"]
    admin = User.objects.get(username="admin")
    date = datetime.now()
    inquiry_primary_key = ""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    custom_context = request.data["queryResult"]["outputContexts"]
    context_offers = ""
    context_orders = ""
    context_response_to_admin = ""
    for i in custom_context:
        if "offers_for_inquiry" in i["name"]:
            context_offers = i["parameters"]["offers"]
            break
        elif "orders_for_inquiry" in i["name"]:
            context_orders = i["parameters"]["orders"]
            break
        elif "create_response_to_admin" in i["name"]:
            context_response_to_admin = i["parameters"]["admin_response"]
            break

    if access_token and context_offers != "":
        profile_token = Token.objects.get(key=access_token)
        user = profile_token.user
        profile = Profile.objects.get(user=user)
        inquiry1 = Inquiry.objects.create(title=inquiry_title, admin=admin, customer=profile, text_or_remarks="",
                                          date=date, email=profile.email, phone_number=profile.phone_number)
        inquiry_primary_key = inquiry1.pk

        if type(context_offers) is list:
            for i in context_offers:
                offer1 = Offer.objects.get(pk=i)
                InquiriesOffers.objects.create(inquiry=inquiry1, offer=offer1)
        elif type(context_offers) is str:
            pk = int(context_offers)
            offer1 = Offer.objects.get(pk=pk)
            InquiriesOffers.objects.create(inquiry=inquiry1, offer=offer1)

    elif access_token is None and context_offers != "":
        inquiry1 = Inquiry.objects.create(title=inquiry_title, admin=admin, text_or_remarks="", date=date, email="",
                               phone_number="")
        inquiry_primary_key = inquiry1.pk

        if type(context_offers) is list:
            for i in context_offers:
                offer1 = Offer.objects.get(pk=i)
                InquiriesOffers.objects.create(inquiry=inquiry1, offer=offer1)
        elif type(context_offers) is str:
            pk = int(context_offers)
            offer1 = Offer.objects.get(pk=pk)
            InquiriesOffers.objects.create(inquiry=inquiry1, offer=offer1)
    elif access_token and context_response_to_admin != "":
        profile_token = Token.objects.get(key=access_token)
        user = profile_token.user
        profile = Profile.objects.get(user=user)
        inquiry1 = Inquiry.objects.create(title=inquiry_title, admin=admin, customer=profile, text_or_remarks="",
                                          date=date, email=profile.email, phone_number=profile.phone_number)
        inquiry_primary_key = inquiry1.pk

        pk = int(context_response_to_admin)
        response_to_customer1 = ResponseToCustomer.objects.get(pk=pk)
        InquiriesResponses.objects.create(inquiry=inquiry1, response=response_to_customer1)
    elif access_token and context_orders != "":
        pass
    elif access_token:
        profile_token = Token.objects.get(key=access_token)
        user = profile_token.user
        profile = Profile.objects.get(user=user)
        inquiry1 = Inquiry.objects.create(title=inquiry_title, admin=admin, customer=profile, text_or_remarks="", date=date,
                             email=profile.email, phone_number=profile.phone_number)
        inquiry_primary_key = inquiry1.pk
    else:
        inquiry1 = Inquiry.objects.create(title=inquiry_title, admin=admin, text_or_remarks="", date=date, email="",
                             phone_number="")
        inquiry_primary_key = inquiry1.pk

    with open('api/response.json') as json_file:
        inquiry = json.load(json_file)

    part_to_modify = inquiry['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Wprowadź tekst Twojego zapytania"
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Wprowadź tekst zapytania. Max 700 znaków"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Enter the text of the inquiry that " \
                                                                                       "you are creating"
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Enter the text of the inquiry that " \
                                                                                       "you are creating. Max 700 signs."
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                         {"title": "Account"},{"title": "Others"}]

    inquiry['payload']['google'] = part_to_modify

    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_inquiry".format(
            session_id),
        "lifespanCount": 5,
        "parameters": {
            "inquiry_primary_key": "{}".format(str(inquiry_primary_key))
        }
    }
    list_with_context = list()
    list_with_context.append(context)
    inquiry["outputContexts"] = list_with_context
    return inquiry


def get_inquiry_text(request):
    """
    Save text in inquiry that is creating by user
    :param request: POST request from "Get inquiry text" Dialogflow intent
    :return: JSON with info about inquiry created or JSON with prompt user to give his phone number and email
    """
    custom_context = request.data["queryResult"]["outputContexts"]
    for i in custom_context:
        if "creating_inquiry" in i["name"]:
            inquiry_primary_key = i["parameters"]["inquiry_primary_key"]
            break
    searched_inquiry = Inquiry.objects.get(pk=inquiry_primary_key)
    searched_inquiry.text_or_remarks = request.data["queryResult"]["queryText"]
    searched_inquiry.save()

    with open('api/response.json') as json_file:
        inquiry = json.load(json_file)

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        part_to_modify = inquiry['payload']['google']

        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Twoje zapytanie zostało " \
                                                                                           "zapisane i wysłane. ID utworzonego" \
                                                                                           " zapytania to {}. Co chcesz" \
                                                                                           " jeszcze zrobić?".format(searched_inquiry.pk)
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Twoje zapytanie zostało " \
                                                                                           "zapisane i wysłane. ID utworzonego " \
                                                                                          "zapytania to {}. Co chcesz" \
                                                                                           " jeszcze zrobić?".format(searched_inquiry.pk)
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Your inquiry was sent. ID of created" \
                                                                                           " inquiry is {}. What do you" \
                                                                                           " want to do next?".format(searched_inquiry.pk)
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Your inquiry was sent. ID of created" \
                                                                                           " inquiry is {}. What do you" \
                                                                                           " want to do next?".format(searched_inquiry.pk)
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        inquiry['payload']['google'] = part_to_modify
        return inquiry
    else:
        part_to_modify = inquiry['payload']['google']

        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Podaj jeszcze email i numer " \
                                                                                           "telefonu"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Podaj jeszcze email i numer " \
                                                                                           "telefonu"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Provide an email and phone number"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Provide an email and phone number"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        inquiry['payload']['google'] = part_to_modify
        session_id = request.data["queryResult"]["outputContexts"][0]["name"]
        session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
        session_id = session_id.lstrip("sessions/").rstrip("/contexts")
        context = {
            "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_inquiry".format(
                session_id),
            "lifespanCount": 5,
            "parameters": {
                "inquiry_primary_key": "{}".format(str(inquiry_primary_key))
            }
        }
        list_with_context = list()
        list_with_context.append(context)
        inquiry["outputContexts"] = list_with_context
        return inquiry


def get_email_phone_for_inquiry(request):
    """
    Save email and phone number in inquiry that is creating by user
    :param request: POST request from "Get email and phone number for inquiry" Dialogflow intent
    :return: JSON with info about saved inquiry
    """
    custom_context = request.data["queryResult"]["outputContexts"]
    for i in custom_context:
        if "creating_inquiry" in i["name"]:
            inquiry_primary_key = i["parameters"]["inquiry_primary_key"]
            break
    searched_inquiry = Inquiry.objects.get(pk=inquiry_primary_key)
    searched_inquiry.email = request.data["queryResult"]["parameters"]["Email"]
    searched_inquiry.phone_number = request.data["queryResult"]["parameters"]["telephone-number"]
    searched_inquiry.save()

    with open('api/response.json') as json_file:
        inquiry = json.load(json_file)

    part_to_modify = inquiry['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Twoje zapytanie zostało " \
                                                                                       "zapisane i wysłane. Numer id Twojego" \
                                                                                       " zapytania to {} Co chcesz" \
                                                                                       " jeszcze zrobić?".format(searched_inquiry.pk)
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Twoje zapytanie zostało " \
                                                                                      "zapisane i wysłane. Numer id Twojego" \
                                                                                      " zapytania to {} Co chcesz" \
                                                                                      " jeszcze zrobić?".format(searched_inquiry.pk)
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Your inquiry was sent. ID of created " \
                                                                                       "inquiry is {} What do you" \
                                                                                       " want to do next?".format(searched_inquiry.pk)
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Your inquiry was sent. ID of created " \
                                                                                      "inquiry is {} What do " \
                                                                                      "you want to do next?".format(searched_inquiry.pk)
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

    inquiry['payload']['google'] = part_to_modify
    return inquiry


def search_inquiry_response(request):
    """
    Creates response with prompting user to choose inquiry or response
    :param request: POST request from "Search inquiry or response" Dialogflow intent
    :return: JSON with prompting user to choose inquiry or response
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    with open('api/response.json') as json_file:
        inquiry = json.load(json_file)

    part_to_modify = inquiry['payload']['google']

    if access_token:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Chcesz wyszukać zapytanie czy " \
                                                                                            "odpowiedź?"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Chcesz wyszukać zapytanie czy " \
                                                                                            "odpowiedź?"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Zapytanie"}, {"title": "Odpowiedź"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Do you want to search an inquiry" \
                                                                                            " or response?"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Do you want to search an inquiry" \
                                                                                       " or response?"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Inquiry"}, {"title": "Response"}]

        inquiry['payload']['google'] = part_to_modify
        session_id = request.data["queryResult"]["outputContexts"][0]["name"]
        session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
        session_id = session_id.lstrip("sessions/").rstrip("/contexts")
        context = {
            "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/create_response_to_admin".format(
                session_id),
            "lifespanCount": 5
        }
        list_with_context = list()
        list_with_context.append(context)
        inquiry["outputContexts"] = list_with_context
        return inquiry
    else:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Musisz być zalogowany aby wyszukać " \
                                                                                           "zapytanie lub odpowiedź"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Musisz być zalogowany aby wyszukać " \
                                                                                          "zapytanie lub odpowiedź"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "You must be logged in to search" \
                                                                                           " for a inquiry or response"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "You must be logged in to search " \
                                                                                          "for a inquiry or response"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        inquiry['payload']['google'] = part_to_modify
        return inquiry


def ask_search_response(request):
    """
    Creates response with prompting user to give his response id
    :param request: POST request from "Ask search response" Dialogflow intent
    :return: JSON with prompting user to give his response id
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    with open('api/response.json') as json_file:
        inquiry = json.load(json_file)

    part_to_modify = inquiry['payload']['google']

    if access_token:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Wprowadź id odpowiedzi"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Wprowadź id odpowiedzi"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Enter the response id"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Enter the response id"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        inquiry['payload']['google'] = part_to_modify
        return inquiry
    else:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Musisz być zalogowany aby wyszukać " \
                                                                                           "zapytanie lub odpowiedź"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Musisz być zalogowany aby wyszukać " \
                                                                                          "zapytanie lub odpowiedź"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "You must be logged in to search" \
                                                                                           " for a inquiry or response"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "You must be logged in to search " \
                                                                                          "for a inquiry or response"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        inquiry['payload']['google'] = part_to_modify
        return inquiry


def ask_search_inquiry(request):
    """
    Creates response with prompting user to give his inquiry id
    :param request: POST request from "Ask search inquiry" Dialogflow intent
    :return: JSON with prompting user to give his inquiry id
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    with open('api/response.json') as json_file:
        inquiry = json.load(json_file)

    part_to_modify = inquiry['payload']['google']

    if access_token:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Wprowadź id zapytania"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Wprowadź id zapytania"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Enter the inquiry id"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Enter the inquiry id"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        inquiry['payload']['google'] = part_to_modify
        return inquiry
    else:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Musisz być zalogowany aby wyszukać " \
                                                                                           "zapytanie lub odpowiedź"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Musisz być zalogowany aby wyszukać " \
                                                                                          "zapytanie lub odpowiedź"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "You must be logged in to search" \
                                                                                           " for a inquiry or response"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "You must be logged in to search " \
                                                                                          "for a inquiry or response"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        inquiry['payload']['google'] = part_to_modify
        return inquiry


def search_inquiry(request):
    """
    Creates response with Dialogflow basic card that contains data of searched inquiry
    :param request: POST request from "Search inquiry" Dialogflow intent
    :return: JSON with basic card that contains data of searched inquiry
    """
    with open('api/response.json') as json_file:
        inquiry = json.load(json_file)

    part_to_modify = inquiry['payload']['google']

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        profile_token = Token.objects.get(key=access_token)
        user = profile_token.user
        profile = Profile.objects.get(user=user)
        inquiry = Inquiry.objects.get(pk=int(request.data["queryResult"]["parameters"]["number"]))
        if inquiry.customer is not None and profile.pk == inquiry.customer.pk:
            if request.data['queryResult']['languageCode'] == 'pl':
                speech_text_pl = "Oto szukane zapytanie"
                display_text_pl = "Oto szukane zapytanie"

                related_offers = list()
                related_orders = list()
                related_responses = list()

                if InquiriesOffers.objects.filter(inquiry=inquiry.pk).count() > 0:
                    inquiries = InquiriesOffers.objects.filter(inquiry=inquiry.pk)
                    for i in inquiries:
                        related_offers.append(i.offer.pk)
                else:
                    related_offers = ""

                if InquiriesOrders.objects.filter(inquiry=inquiry.pk).count() > 0:
                    inquiries = InquiriesOrders.objects.filter(inquiry=inquiry.pk)
                    for i in inquiries:
                        related_orders.append(i.order.pk)
                else:
                    related_orders = ""

                if InquiriesResponses.objects.filter(inquiry=inquiry.pk).count() > 0:
                    inquiries = InquiriesResponses.objects.filter(inquiry=inquiry.pk)
                    for i in inquiries:
                        related_responses.append(i.response.pk)
                else:
                    related_responses = ""

                date = str(inquiry.date)
                date = date[:10]
                basic_card_pl = {
                    "basicCard": {
                        "title": "Zapytanie nr {}".format(inquiry.pk),
                        "formattedText": "___Tytuł:___  {}  \n  \n__Data:__  {}  \n__Text:__  {}  \n  \n__Powiązane "
                                         "oferty:__ {}  \n__Powiązane zlecenia:__ {}  \n__Id odpowiedzi:__ {}"
                            .format(inquiry.title, date, inquiry.text_or_remarks, " ".join(str(offer) for offer in related_offers),
                                    " ".join(str(order) for order in related_orders), " ".join(str(response) for response in related_responses))
                    }
                }

                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]

                with open('api/response.json') as json_file:
                    response = json.load(json_file)
                part_to_modify = response['payload']['google']['richResponse']

                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                part_to_modify['items'].append(basic_card_pl)
                part_to_modify['suggestions'] = suggestions_pl
                response['payload']['google']['richResponse'] = part_to_modify
                return response

            elif request.data['queryResult']['languageCode'] == 'en':
                speech_text_en = "Here's the searched inquiry"
                display_text_en = "Here's the searched inquiry"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},{"title": "Account"},
                                 {"title": "Others"}]

                related_offers = list()
                related_orders = list()
                related_responses = list()

                if InquiriesOffers.objects.filter(inquiry=inquiry.pk).count() > 0:
                    inquiries = InquiriesOffers.objects.filter(inquiry=inquiry.pk)
                    for i in inquiries:
                        related_offers.append(i.offer.pk)
                else:
                    related_offers = ""

                if InquiriesOrders.objects.filter(inquiry=inquiry.pk).count() > 0:
                    inquiries = InquiriesOrders.objects.filter(inquiry=inquiry.pk)
                    for i in inquiries:
                        related_orders.append(i.order.pk)
                else:
                    related_orders = ""

                if InquiriesResponses.objects.filter(inquiry=inquiry.pk).count() > 0:
                    inquiries = InquiriesResponses.objects.filter(inquiry=inquiry.pk)
                    for i in inquiries:
                        related_responses.append(i.response.pk)
                else:
                    related_responses = ""

                date = str(inquiry.date)
                date = date[:10]
                basic_card_en = {
                    "basicCard": {
                        "title": "Inquiry number  {}".format(inquiry.pk),
                        "formattedText": "___Title:___  {}  \n  \n__Date:__  {}  \n__Text:__  {}  \n  \n__Related "
                                         "offers:__ {}  \n__Related orders:__ {}  \n__Responses Id:__ {}"
                            .format(inquiry.title, date, inquiry.text_or_remarks,
                                    " ".join(str(offer) for offer in related_offers),
                                    " ".join(str(order) for order in related_orders),
                                    " ".join(str(response) for response in related_responses))
                    }
                }

                with open('api/response.json') as json_file:
                    response = json.load(json_file)
                part_to_modify = response['payload']['google']['richResponse']

                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                part_to_modify['items'].append(basic_card_en)
                part_to_modify['suggestions'] = suggestions_en
                response['payload']['google']['richResponse'] = part_to_modify
                return response
        else:
            if request.data['queryResult']['languageCode'] == 'pl':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Nie posiadasz na swoim " \
                                                                                               "koncie zapytania o id " \
                                                                                               "równym {}".format(int(request.data["queryResult"]["parameters"]["number"]))
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Nie posiadasz na swoim " \
                                                                                               "koncie zapytania o id " \
                                                                                               "równym {}".format(int(request.data["queryResult"]["parameters"]["number"]))
                part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                                 {"title": "Konto"}, {"title": "Inne"}]
            elif request.data['queryResult']['languageCode'] == 'en':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "You don't have inquiry " \
                                                                                               "on your account that id is" \
                                                                                               "equal {}".format(int(request.data["queryResult"]["parameters"]["number"]))
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "You don't have inquiry " \
                                                                                               "on your account that id is" \
                                                                                               "equal {}".format(int(request.data["queryResult"]["parameters"]["number"]))
                part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                                 {"title": "Account"}, {"title": "Others"}]

            inquiry['payload']['google'] = part_to_modify
            return inquiry
    else:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Musisz być zalogowany aby wyszukać " \
                                                                                           "zapytanie lub odpowiedź"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Musisz być zalogowany aby wyszukać " \
                                                                                          "zapytanie lub odpowiedź"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "You must be logged in to search" \
                                                                                           " for a inquiry or response"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "You must be logged in to search " \
                                                                                          "for a inquiry or response"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        inquiry['payload']['google'] = part_to_modify
        return inquiry


def search_response(request):
    """
    Creates response with Dialogflow basic card that contains data searched response
    :param request: POST request from "Search response" Dialogflow intent
    :return:JSON with basic card that contains data searched response
    """
    with open('api/response.json') as json_file:
        inquiry = json.load(json_file)

    part_to_modify = inquiry['payload']['google']

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        profile_token = Token.objects.get(key=access_token)
        user = profile_token.user
        profile = Profile.objects.get(user=user)
        response = ResponseToCustomer.objects.get(pk=int(request.data["queryResult"]["parameters"]["number"]))
        if ResponsesProfiles.objects.filter(response=response.pk, profile=profile.pk).count() == 1:
            if request.data['queryResult']['languageCode'] == 'pl':
                speech_text_pl = "Oto szukana odpowiedź"
                display_text_pl = "Oto szukana odpowiedź"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]

                date = str(response.date)
                date = date[:10]
                basic_card_pl = {
                    "basicCard": {
                        "title": "Odpowiedź nr {}".format(response.pk),
                        "formattedText": "___Tytuł:___  {}  \n  \n__Data:__  {}  \n__Text:__  {}"
                            .format(response.title, date, response.text)
                    }
                }
                response.readed = True
                response.save()

                with open('api/response.json') as json_file:
                    response = json.load(json_file)
                part_to_modify = response['payload']['google']['richResponse']

                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                part_to_modify['items'].append(basic_card_pl)
                part_to_modify['suggestions'] = suggestions_pl
                response['payload']['google']['richResponse'] = part_to_modify
                return response
            elif request.data['queryResult']['languageCode'] == 'en':
                speech_text_en = "Here's the searched response"
                display_text_en = "Here's the searched response"
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                  {"title": "Others"}]

                date = str(inquiry.date)
                date = date[:10]
                basic_card_en = {
                    "basicCard": {
                        "title": "Response number {}".format(response.pk),
                        "formattedText": "___Title:___  {}  \n  \n__Date:__  {}  \n__Text:__  {}"
                            .format(response.title, date, response.text)
                    }
                }
                response.readed = True
                response.save()

                with open('api/response.json') as json_file:
                    response = json.load(json_file)
                part_to_modify = response['payload']['google']['richResponse']

                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                part_to_modify['items'].append(basic_card_en)
                part_to_modify['suggestions'] = suggestions_en
                response['payload']['google']['richResponse'] = part_to_modify
                return response
        else:
            if request.data['queryResult']['languageCode'] == 'pl':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Nie posiadasz na swoim " \
                                                                                               "koncie odpowiedzi o id " \
                                                                                               "równym {}".format(int(request.data["queryResult"]["parameters"]["number"]))
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Nie posiadasz na swoim " \
                                                                                               "koncie odpowiedzi o id " \
                                                                                               "równym {}".format(int(request.data["queryResult"]["parameters"]["number"]))
                part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                                 {"title": "Konto"}, {"title": "Inne"}]
            elif request.data['queryResult']['languageCode'] == 'en':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "You don't have response " \
                                                                                               "on your account that id is" \
                                                                                               "equal {}".format(int(request.data["queryResult"]["parameters"]["number"]))
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "You don't have response " \
                                                                                               "on your account that id is" \
                                                                                               "equal {}".format(int(request.data["queryResult"]["parameters"]["number"]))
                part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                                 {"title": "Account"}, {"title": "Others"}]

            inquiry['payload']['google'] = part_to_modify
            return inquiry
    else:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Musisz być zalogowany aby wyszukać " \
                                                                                           "zapytanie lub odpowiedź"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Musisz być zalogowany aby wyszukać " \
                                                                                          "zapytanie lub odpowiedź"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "You must be logged in to search" \
                                                                                           " for a inquiry or response"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "You must be logged in to search " \
                                                                                          "for a inquiry or response"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        inquiry['payload']['google'] = part_to_modify
        return inquiry


# def trigger_creating_inquiry_for_offer_order(request):
#     """
#     Create response with "trigger_creating_inquiry" Dialogflow event
#     :param request: POST request from one of the items in list
#     :return: JSON with "trigger_creating_inquiry" Dialogflow event
#     """
#     language = request.data['queryResult']['languageCode']
#     if language == "pl":
#         response = {
#             "followupEventInput": {
#                 "name": "trigger_creating_inquiry",
#                 "languageCode": "pl"
#             }
#         }
#     elif language == "en-us":
#         response = {
#             "followupEventInput": {
#                 "name": "trigger_creating_inquiry",
#                 "languageCode": "en-us"
#             }
#         }
#     return response


def ask_creating_inquiry_for(request):
    """
    Creates response with prompting user to give choice: creating inquiry for offer or order
    :param request: POST request from "Ask creating inquiry for" Dialogflow intent
    :return: JSON with prompting user to give choice: creating inquiry for offer or order
    """
    with open('api/response.json') as json_file:
        inquiry = json.load(json_file)

    part_to_modify = inquiry['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Chcesz stworzyć zapytanie dla oferty" \
                                                                                       " czy dla zlecenia?"
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Chcesz stworzyć zapytanie dla oferty" \
                                                                                       " czy dla zlecenia?"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Do you want to create a query " \
                                                                                       "for an offer or an order?"
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Do you want to create a query " \
                                                                                      "for an offer or an order?"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}]

    inquiry['payload']['google'] = part_to_modify
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_inquiry".format(
            session_id),
        "lifespanCount": 5
    }
    list_with_context = list()
    list_with_context.append(context)
    inquiry["outputContexts"] = list_with_context
    return inquiry


def ask_search_offer_for_creating_inquiry(request):
    """
    Creates response with prompting user to give data to search offer or offers
    :param request: POST request from "Ask search offer for creating inquiry" Dialogflow intent
    :return: JSON with prompting user to give data to search offer or offers
    """
    with open('api/response.json') as json_file:
        inquiry = json.load(json_file)

    part_to_modify = inquiry['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Podaj dane oferty jak na przykład" \
                                                                                       " miejsce odjazdu, miejsce docelowe, " \
                                                                                       "data odjazdu i tym podobne. Możesz zamiast" \
                                                                                       " tego podać id oferty"
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Podaj dane oferty jak na przykład" \
                                                                                       " miejsce odjazdu, miejsce docelowe, " \
                                                                                       "data odjazdu i tym podobne. Możesz zamiast" \
                                                                                       " tego podać id oferty"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Provide offer details such as place of departure," \
                                                                                       " destination, departure date etc." \
                                                                                       " You can enter the offer id instead"
        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Provide offer details such as place of departure," \
                                                                                       " destination, departure date etc." \
                                                                                       " You can enter the offer id instead"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

    inquiry['payload']['google'] = part_to_modify
    return inquiry


def ask_search_order_for_creating_inquiry(request):
    """
    Create response with prompting user to give data to search order or orders
    :param request: POST request from "Ask search order for creating inquiry" Dialogflow intent
    :return: JSON with prompting user to give data to search order or orders
     """
    pass


def get_offers_for_inquiry(request):
    """
    Search offers, create context with this offers as parameters, place in JSON offers to display
    :param request: POST request from "Get offers for inquiry" Dialogflow intent
    :return: JSON with offers to display and offers in created context "offers_for_inquiry"
    """
    parameters = request.data["queryResult"]["parameters"]
    if parameters["geo-city"] != "" and parameters["geo-city1"] != "":
        result = get_offers_in_list(request)
        if type(result) is not list:
            return result

        offers_pl = 0
        offers_en = 0
        for offer in result:
            if offer.language == 'pl':
                offers_pl += 1
            elif offer.language == 'en':
                offers_en += 1

        if request.data['queryResult']['languageCode'] == 'pl' and offers_pl > 1:
            with open('api/offers_list.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['systemIntent']["data"]["listSelect"]

            counter = 0
            offers_to_insert = []
            offers_to_context = list()
            part_to_modify["title"] = "Wyszukane oferty"
            for offer in result:
                if counter < 30:
                    if offer.language == 'pl':
                        offers_to_insert.append({
                            "optionInfo": {
                                "key": "{}".format(offer.pk)
                            },
                            "description": "{}({}) -> {}({}), Odjazd: {}, Przyjazd na miejsce: {}, Liczba palet: {}, Uwagi: "
                                           "{}, Cena: {}".format(
                                offer.loading_place.place.post_place, offer.loading_place.place.country,
                                offer.destination.place.post_place, offer.destination.place.country,
                                offer.loading_place.date, offer.destination.date, offer.pallets_number,
                                offer.remarks, offer.price),
                            "title": "Oferta nr {}".format(offer.pk)
                        })
                        offers_to_context.append(offer.pk)
                    counter += 1
                else:
                    break

            part_to_modify["items"] = offers_to_insert
            response['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
            part_to_modify = response['payload']['google']["richResponse"]
            part_to_modify['items'][0]['simpleResponse'][
                'textToSpeech'] = "Oto lista z ofertami dla których będzie tworzone zapytanie. Podaj tytuł zapytania"
            part_to_modify['items'][0]['simpleResponse'][
                'displayText'] = "Oto lista z ofertami dla których będzie tworzone zapytanie. Podaj tytuł zapytania"
            part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                             {"title": "Konto"}, {"title": "Inne"}]
            response['payload']['google']["richResponse"] = part_to_modify

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/offers_for_inquiry".format(session_id),
                "lifespanCount": 5,
                "parameters": {
                    "offers": offers_to_context
                }
            }
            list_with_context = list()
            list_with_context.append(context)
            response["outputContexts"] = list_with_context

            return response

        elif request.data['queryResult']['languageCode'] == 'en' and offers_en > 1:
            with open('api/offers_list.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['systemIntent']["data"]["listSelect"]

            counter = 0
            offers_to_insert = []
            offers_to_context = list()
            part_to_modify["title"] = "Searched offers"
            for offer in result:
                if counter < 30:
                    if offer.language == 'en':
                        offers_to_insert.append({
                            "optionInfo": {
                                "key": "{}".format(offer.pk)
                            },
                            "description": "{}({}) -> {}({}), Departure: {}, Arrival: {}, Pallets number: {}, remarks: "
                                           "{}, Price: {}".format(
                                offer.loading_place.place.post_place, offer.loading_place.place.country,
                                offer.destination.place.post_place, offer.destination.place.country,
                                offer.loading_place.date, offer.destination.date, offer.pallets_number,
                                offer.remarks, offer.price),
                            "title": "Offer number {}".format(offer.pk)
                        })
                        offers_to_context.append(offer.pk)
                    counter += 1
                else:
                    break

                part_to_modify["items"] = offers_to_insert
                response['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
                part_to_modify = response['payload']['google']["richResponse"]
                part_to_modify['items'][0]['simpleResponse'][
                    'textToSpeech'] = "Here is a list of offers for which the inquiry will be created. Enter the title " \
                                      "of the inquiry"
                part_to_modify['items'][0]['simpleResponse'][
                    'displayText'] = "Here is a list of offers for which the inquiry will be created. Enter the title " \
                                      "of the inquiry"
                part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                 {"title": "Account"}, {"title": "Others"}]
            response['payload']['google']["richResponse"] = part_to_modify

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/offers_for_inquiry".format(session_id),
                "lifespanCount": 5,
                "parameters": {
                    "offers": offers_to_context
                }
            }
            list_with_context = list()
            list_with_context.append(context)
            response["outputContexts"] = list_with_context

            return response

        elif request.data['queryResult']['languageCode'] == 'pl' and offers_pl == 1:
            speech_text_pl = "Oto oferta dla której będzie tworzone zapytanie. Podaj tytuł zapytania"
            display_text_pl = "Oto oferta dla której będzie tworzone zapytanie. Podaj tytuł zapytania"
            basic_card_pl = {
                "basicCard": {
                    "title": "Oferta nr {}".format(result[0].pk),
                    "formattedText": "___Skąd:___  {}({})  \n__Dokąd:__  {}({})  \n  \n__Odjazd:__  {} o godz. {}"
                                     "  \n__Przyjazd:__  {} o godz. {}  \n  \n__Liczba palet:__  {}  \n"
                                     "__Uwagi:__  {}  \n  \n__Cena:__  {} pln"
                        .format(result[0].loading_place.place.post_place, result[0].loading_place.place.country,
                                result[0].destination.place.post_place, result[0].destination.place.country,
                                result[0].loading_place.date, result[0].loading_place.hour,
                                result[0].destination.date, result[0].destination.hour,
                                result[0].pallets_number, result[0].remarks, result[0].price)
                }
            }
            suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                              {"title": "Inne"}]

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/offers_for_inquiry".format(session_id),
                "lifespanCount": 5,
                "parameters": {
                    "offers": "{}".format(str(result[0].pk))
                }
            }
            list_with_context = list()
            list_with_context.append(context)

            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']

            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
            part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
            part_to_modify['items'].append(basic_card_pl)
            part_to_modify['suggestions'] = suggestions_pl

            response['payload']['google']['richResponse'] = part_to_modify
            response["outputContexts"] = list_with_context

            return response

        elif request.data['queryResult']['languageCode'] == 'en' and offers_en == 1:
            speech_text_en = "Here is the offer for which the inquiry will be created. Enter the title of the inquiry"
            display_text_en = "Here is the offer for which the inquiry will be created. Enter the title of the inquiry"
            basic_card_en = {
                "basicCard": {
                    "title": "Offer number {}".format(result[0].pk),
                    "formattedText": "___From:___  {}({})  \n__To:__  {}({})  \n  \n__Departure:__  {} at {}"
                                     "  \n__Arrival:__  {} at {}  \n  \n__Pallets number:__  {}  \n"
                                     "__Remarks:__  {}  \n  \n__Price:__  {} pln"
                        .format(result[0].loading_place.place.post_place, result[0].loading_place.place.country,
                                result[0].destination.place.post_place, result[0].destination.place.country,
                                result[0].loading_place.date, result[0].loading_place.hour,
                                result[0].destination.date, result[0].destination.hour,
                                result[0].pallets_number, result[0].remarks, result[0].price
                                )
                }
            }
            suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                              {"title": "Others"}]

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/offers_for_inquiry".format(session_id),
                "lifespanCount": 5,
                "parameters": {
                    "offers": "{}".format(str(result[0].pk))
                }
            }
            list_with_context = list()
            list_with_context.append(context)

            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
            part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
            part_to_modify['items'].append(basic_card_en)
            part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            response["outputContexts"] = list_with_context

            return response
        else:
            return lack_searched_offer(request)
    else:
        offer = Offer.objects.get(pk=int(request.data["queryResult"]["parameters"]["number"]))
        if request.data['queryResult']['languageCode'] == 'pl':
            speech_text_pl = "Oto oferta dla której będzie tworzone zapytanie. Podaj tytuł zapytania"
            display_text_pl = "Oto oferta dla której będzie tworzone zapytanie. Podaj tytuł zapytania"
            basic_card_pl = {
                "basicCard": {
                    "title": "Oferta nr {}".format(offer.pk),
                    "formattedText": "___Skąd:___  {}({})  \n__Dokąd:__  {}({})  \n  \n__Odjazd:__  {} o godz. {}"
                                     "  \n__Przyjazd:__  {} o godz. {}  \n  \n__Liczba palet:__  {}  \n"
                                     "__Uwagi:__  {}  \n  \n__Cena:__  {} pln"
                        .format(offer.loading_place.place.post_place, offer.loading_place.place.country,
                                offer.destination.place.post_place, offer.destination.place.country,
                                offer.loading_place.date, offer.loading_place.hour,
                                offer.destination.date, offer.destination.hour,
                                offer.pallets_number, offer.remarks, offer.price)
                }
            }
            suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                              {"title": "Inne"}]

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/offers_for_inquiry".format(session_id),
                "lifespanCount": 5,
                "parameters": {
                    "offers": "{}".format(str(offer.pk))
                }
            }
            list_with_context = list()
            list_with_context.append(context)

            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']

            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
            part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
            part_to_modify['items'].append(basic_card_pl)
            part_to_modify['suggestions'] = suggestions_pl

            response['payload']['google']['richResponse'] = part_to_modify
            response["outputContexts"] = list_with_context

            return response
        elif request.data['queryResult']['languageCode'] == 'en':
            speech_text_en = "Here is the offer for which the inquiry will be created. Enter the title of the inquiry"
            display_text_en = "Here is the offer for which the inquiry will be created. Enter the title of the inquiry"
            basic_card_en = {
                "basicCard": {
                    "title": "Offer number {}".format(offer.pk),
                    "formattedText": "___From:___  {}({})  \n__To:__  {}({})  \n  \n__Departure:__  {} at {}"
                                     "  \n__Arrival:__  {} at {}  \n  \n__Pallets number:__  {}  \n"
                                     "__Remarks:__  {}  \n  \n__Price:__  {} pln"
                        .format(offer.loading_place.place.post_place, offer.loading_place.place.country,
                                offer.destination.place.post_place, offer.destination.place.country,
                                offer.loading_place.date, offer.loading_place.hour,
                                offer.destination.date, offer.destination.hour,
                                offer.pallets_number, offer.remarks, offer.price
                                )
                }
            }
            suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                              {"title": "Others"}]

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/offers_for_inquiry".format(session_id),
                "lifespanCount": 5,
                "parameters": {
                    "offers": "{}".format(str(offer.pk))
                }
            }
            list_with_context = list()
            list_with_context.append(context)

            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
            part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
            part_to_modify['items'].append(basic_card_en)
            part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify
            response["outputContexts"] = list_with_context

            return response


def are_there_unread_responses(request):
    """
    Searches amount unreaded responses by user
    :param request: POST request form "Are there unread responses" Dialogflow intent
    :return: Json with amount unreaded responses by user
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz sprawdzić czy masz nieprzczeczytane odpowiedzi, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz sprawdzić czy masz nieprzczeczytane odpowiedzi. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't check if you have unread answers, because you do not have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't check if you have unread answers. Create an account by selecting the option below \"Sign up\""

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
            if ResponsesProfiles.objects.filter(profile=profile).count() > 0:
                responses_profiles = ResponsesProfiles.objects.filter(profile=profile)
                count = 0
                for i in responses_profiles:
                    if i.response.readed is False:
                        count += 1
                if count == 0:
                    response_pl = "Nie masz żadnych nieprzeczytanych odpowiedzi"
                    response_en = "You do not have any unread responses"
                elif count == 1:
                    response_pl = "Masz jedną nieprzeczytaną odpowiedź"
                    response_en = "You have one unread answer"
                else:
                    response_pl = "Masz {} nieprzeczytanych odpowiedzi".format(count)
                    response_en = "You have {} unread answers".format(count)
            elif ResponsesProfiles.objects.filter(profile=profile).count() == 0:
                response_pl = "Nie masz żadnych nieprzeczytanych odpowiedzi"
                response_en = "You do not have any unread responses"

            if language == "pl":
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                  {"title": "Konto"}, {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = response_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == 'en':
                suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                  {"title": "Account"}, {"title": "Others"}]
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


def unread_responses(request):
    """
    Creates Dialogflow list with unread responses by user or response about there isn't unread responses
    :param request: POST request from "Unread responses" Dialogflow intent
    :return: JSON with list that contains unread responses by user or with response about there isn't unread responses
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz przejrzeć nieprzeczytanych odpowiedzi, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz przejrzeć nieprzeczytanych odpowiedzi. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't view unread responses, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't view unread responses. Create an account by selecting the option below \"Sign up\""

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
            if ResponsesProfiles.objects.filter(profile=profile).count() > 0:
                responses_profiles = ResponsesProfiles.objects.filter(profile=profile)
                responses = list()
                for item in responses_profiles:
                    responses.append(item.response)

                unread_responses = list()
                number_unread_responses = 0
                for response in responses:
                    if response.readed is False:
                        number_unread_responses += 1
                        unread_responses.append(response)


                counter = 0
                responses_to_insert = list()
                if request.data['queryResult']['languageCode'] == 'pl' and number_unread_responses > 1:
                    with open('api/offers_list.json') as json_file:
                        responses_list = json.load(json_file)
                    part_to_modify = responses_list['payload']['google']["systemIntent"]["data"]["listSelect"]
                    part_to_modify["title"] = "Nieprzeczytane odpowiedzi"

                    for response in unread_responses:
                        if counter < 30:
                            responses_to_insert.append({
                                "optionInfo": {
                                    "key": "{}".format(response.pk)
                                },
                                "description": "Tytuł: {}, Data: {}, Tekst: {}".format(
                                    response.title, response.date, response.text),
                                "title": "Odpowiedź nr {}".format(response.pk)
                                }
                            )
                            response.readed = True
                            response.save()
                            counter += 1
                        else:
                            break

                    part_to_modify["items"] = responses_to_insert
                    responses_list['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
                    part_to_modify = responses_list['payload']['google']["richResponse"]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Oto lista nieprzeczytanych odpowiedzi"
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = "Oto lista nieprzeczytanych odpowiedzi"
                    part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                     {"title": "Konto"}, {"title": "Inne"}]
                    responses_list['payload']['google']["richResponse"] = part_to_modify
                    return responses_list
                elif request.data['queryResult']['languageCode'] == 'en' and number_unread_responses > 1:
                    with open('api/offers_list.json') as json_file:
                        responses_list = json.load(json_file)
                    part_to_modify = responses_list['payload']['google']["systemIntent"]["data"]["listSelect"]
                    part_to_modify["title"] = "Unread responses"

                    for response in unread_responses:
                        if counter < 30:
                            responses_to_insert.append({
                                "optionInfo": {
                                    "key": "{}".format(response.pk)
                                },
                                "description": "Title: {}, Date: {}, Text: {} ".format(
                                    response.title, response.date, response.text),
                                "title": "Response number {}".format(response.pk)
                                }
                            )
                            response.readed = True
                            response.save()
                            counter += 1
                        else:
                            break

                    part_to_modify["items"] = responses_to_insert
                    responses_list['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
                    part_to_modify = responses_list['payload']['google']["richResponse"]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Here is a list of unread responses"
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = "Here is a list of unread responses"
                    part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                     {"title": "Account"}, {"title": "Others"}]
                    responses_list['payload']['google']["richResponse"] = part_to_modify
                    return responses_list
                elif request.data['queryResult']['languageCode'] == 'pl' and number_unread_responses == 1:
                    speech_text_pl = "Oto jedna nieprzeczytana odpowiedź"
                    display_text_pl = "Oto jedna nieprzeczytana odpowiedź"
                    basic_card_pl = {
                        "basicCard": {
                            "title": "Odpowiedź nr {}".format(unread_responses[0].pk),
                            "formattedText": "___Tytuł:___  {}  \n__Data:__  {}  \n  \n__Tekst:__  {}"
                                .format(unread_responses[0].title, unread_responses[0].date, unread_responses[0].text)
                        }
                    }
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                      {"title": "Inne"}]

                    with open('api/response.json') as json_file:
                        response = json.load(json_file)
                    part_to_modify = response['payload']['google']['richResponse']
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['items'].append(basic_card_pl)
                    part_to_modify['suggestions'] = suggestions_pl

                    response['payload']['google']['richResponse'] = part_to_modify
                    return response
                elif request.data['queryResult']['languageCode'] == 'en' and number_unread_responses == 1:
                    speech_text_en = "Here is one unread response"
                    display_text_en = "Here is one unread response"
                    basic_card_en = {
                        "basicCard": {
                            "title": "Response number {}".format(unread_responses[0].pk),
                            "formattedText": "___Title:___  {}  \n__Date:__  {}  \n  \n__Text:__  {}"
                                .format(unread_responses[0].title, unread_responses[0].date, unread_responses[0].text)
                        }
                    }
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                      {"title": "Others"}]

                    with open('api/response.json') as json_file:
                        response = json.load(json_file)
                    part_to_modify = response['payload']['google']['richResponse']
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                    part_to_modify['items'].append(basic_card_en)
                    part_to_modify['suggestions'] = suggestions_en

                    response['payload']['google']['richResponse'] = part_to_modify
                    return response
                else:
                    with open('api/response.json') as json_file:
                        response = json.load(json_file)
                    part_to_modify = response['payload']['google']["richResponse"]

                    if request.data['queryResult']['languageCode'] == 'pl':
                        part_to_modify['items'][0]['simpleResponse'][
                            'textToSpeech'] = "Nie masz żadnych nieprzeczytanych odpowiedzi na Twoim koncie. Co chcesz jeszcze zrobić?"
                        part_to_modify['items'][0]['simpleResponse'][
                            'displayText'] = "Nie masz żadnych nieprzeczytanych odpowiedzi na Twoim koncie. Co chcesz jeszcze zrobić?"
                        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                         {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
                    elif request.data['queryResult']['languageCode'] == 'en-us':
                        part_to_modify['items'][0]['simpleResponse'][
                            'textToSpeech'] = "You don't have any unread responses on your account. What do you want to do next?"
                        part_to_modify['items'][0]['simpleResponse'][
                            'displayText'] = "You don't have any unread responses on your account. What do you want to do next?"
                        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                         {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

                    response['payload']['google']['richResponse'] = part_to_modify
                    return response
            else:
                with open('api/response.json') as json_file:
                    response = json.load(json_file)
                part_to_modify = response['payload']['google']["richResponse"]

                if request.data['queryResult']['languageCode'] == 'pl':
                    part_to_modify['items'][0]['simpleResponse'][
                        'textToSpeech'] = "Nie masz w ogóle żadnych odpowiedzi na Twoim koncie. Co chcesz jeszcze zrobić?"
                    part_to_modify['items'][0]['simpleResponse'][
                        'displayText'] = "Nie masz żadnych odpowiedzi na Twoim koncie. Co chcesz jeszcze zrobić?"
                    part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                     {"title": "Konto"}, {"title": "Inne"}]
                elif request.data['queryResult']['languageCode'] == 'en-us':
                    part_to_modify['items'][0]['simpleResponse'][
                        'textToSpeech'] = "You don't have any responses on your account. What do you want to do next?"
                    part_to_modify['items'][0]['simpleResponse'][
                        'displayText'] = "You don't have any responses on your account. What do you want to do next?"
                    part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                     {"title": "Account"}, {"title": "Others"}]

                response['payload']['google']['richResponse'] = part_to_modify
                return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def ask_responses_for_inquiry(request):
    """
    Creates Json response with prompting user to give inquiry id
    :param request: POST request from "Ask responses for inquiry" Dialogflow intent
    :return: JSON response with prompting user to give inquiry id
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz przeglądać odpowiedzi dla danego zapytania, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz przejrzeć odpowiedzi dla zapytania. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't view the responses for a given inquiry, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't view the responses for the inquiry. Create an account by selecting the option below \"Sign up\""

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

            if request.data['queryResult']['languageCode'] == 'pl':
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Podaj id zapytania, dla którego mam wyszukać odpowiedzi"
                part_to_modify['items'][0]['simpleResponse']['displayText'] = "Podaj id zapytania, dla którego mam wyszukać odpowiedzi"
                part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                 {"title": "Konto"}, {"title": "Inne"}]
            elif request.data['queryResult']['languageCode'] == 'en':
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Enter the id of the question for which I have to " \
                                                                               "search for answers"
                part_to_modify['items'][0]['simpleResponse']['displayText'] = "Enter the id of the question for which I have to " \
                                                                              "search for answers"
                part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                 {"title": "Account"}, {"title": "Others"}]

            response['payload']['google']['richResponse'] = part_to_modify

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/responses_for_inquiry".format(session_id),
                "lifespanCount": 5
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


def responses_for_inquiry(request):
    """
    Searches admin responses to customer for given inquiry in request
    :param request: POST request from "Responses for inquiry" Dialogflow intent
    :return: Json with admin responses to customer
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz przeglądać odpowiedzi dla danego zapytania, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz przejrzeć odpowiedzi dla zapytania. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't view the responses for a given inquiry, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't view the responses for the inquiry. Create an account by selecting the option below \"Sign up\""

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

            inquiry_id = request.data["queryResult"]["parameters"]["number"]
            if Inquiry.objects.filter(pk=inquiry_id).count() > 0:
                inquiry = Inquiry.objects.get(pk=inquiry_id)
                customer_id = inquiry.customer.pk
                profile_token = Token.objects.get(key=access_token)
                user = profile_token.user
                profile = Profile.objects.get(user=user)
                if customer_id == profile.pk:
                    if InquiriesResponses.objects.filter(inquiry=inquiry.pk).count() > 0:
                        responses = list()
                        inquiries_responses = InquiriesResponses.objects.filter(inquiry=inquiry.pk)
                        for i in inquiries_responses:
                            one_response = ResponseToCustomer.objects.get(pk=i.response.pk)
                            responses.append(one_response)
                        if len(responses) > 1:
                            counter = 0
                            responses_to_insert = list()
                            if request.data['queryResult']['languageCode'] == 'pl':
                                with open('api/offers_list.json') as json_file:
                                    responses_list = json.load(json_file)
                                part_to_modify = responses_list['payload']['google']["systemIntent"]["data"]["listSelect"]
                                part_to_modify["title"] = "Odpowiedzi dla Twojego zapytania"

                                for response in responses:
                                    if counter < 30:
                                        responses_to_insert.append({
                                            "optionInfo": {
                                                "key": "{}".format(response.pk)
                                            },
                                            "description": "Tytuł: {}, Data: {}, Tekst: {}".format(
                                                response.title, response.date, response.text),
                                            "title": "Odpowiedź nr {}".format(response.pk)
                                        }
                                        )
                                        response.readed = True
                                        response.save()
                                        counter += 1
                                    else:
                                        break

                                part_to_modify["items"] = responses_to_insert
                                responses_list['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
                                part_to_modify = responses_list['payload']['google']["richResponse"]
                                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Odpowiedzi dla Twojego zapytania"
                                part_to_modify['items'][0]['simpleResponse']['displayText'] = "Odpowiedzi dla Twojego zapytania"
                                part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},{"title": "Zapytania"},
                                                                 {"title": "Konto"}, {"title": "Inne"}]
                                responses_list['payload']['google']["richResponse"] = part_to_modify

                                return responses_list
                            elif request.data['queryResult']['languageCode'] == 'en':
                                with open('api/offers_list.json') as json_file:
                                    responses_list = json.load(json_file)
                                part_to_modify = responses_list['payload']['google']["systemIntent"]["data"]["listSelect"]
                                part_to_modify["title"] = "Responses for your inquiry"

                                for response in responses:
                                    if counter < 30:
                                        responses_to_insert.append({
                                            "optionInfo": {
                                                "key": "{}".format(response.pk)
                                            },
                                            "description": "Title: {}, Date: {}, Text: {}".format(
                                                response.title, response.date, response.text),
                                            "title": "Response number {}".format(response.pk)
                                        }
                                        )
                                        response.readed = True
                                        response.save()
                                        counter += 1
                                    else:
                                        break

                                part_to_modify["items"] = responses_to_insert
                                responses_list['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
                                part_to_modify = responses_list['payload']['google']["richResponse"]
                                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Responses for your inquiry"
                                part_to_modify['items'][0]['simpleResponse']['displayText'] = "Responses for your inquiry"
                                part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                                 {"title": "Account"}, {"title": "Others"}]
                                responses_list['payload']['google']["richResponse"] = part_to_modify

                                return responses_list
                        elif len(responses) == 1:
                            speech_text_pl = "Oto odpowiedź dla Twojego zapytania"
                            display_text_pl = "Oto odpowiedź dla Twojego zapytania"
                            speech_text_en = "Here's the answer for your inquiry"
                            display_text_en = "Here's the answer for your inquiry"

                            basic_card_pl = {
                                "basicCard": {
                                    "title": "Odpowiedź nr {}".format(responses[0].pk),
                                    "formattedText": "___Tytuł:___  {}  \n__Data:__  {}  \n  \n__Tekst:__  {}"
                                        .format(responses[0].title, responses[0].date, responses[0].text)
                                }
                            }
                            basic_card_en = {
                                "basicCard": {
                                    "title": "Response number {}".format(responses[0].pk),
                                    "formattedText": "___Title:___  {}  \n__Date:__  {}  \n  \n__Text:__  {}"
                                        .format(responses[0].title, responses[0].date, responses[0].text)
                                }
                            }

                            suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                              {"title": "Konto"}, {"title": "Inne"}]
                            suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                              {"title": "Account"}, {"title": "Others"}]

                            one_response = responses[0]
                            one_response.readed = True
                            one_response.save()

                            part_to_modify = response['payload']['google']['richResponse']
                            if request.data['queryResult']['languageCode'] == 'pl':
                                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                                part_to_modify['items'].append(basic_card_pl)
                                part_to_modify['suggestions'] = suggestions_pl
                            elif request.data['queryResult']['languageCode'] == 'en':
                                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                                part_to_modify['items'].append(basic_card_en)
                                part_to_modify['suggestions'] = suggestions_en

                            response['payload']['google']['richResponse'] = part_to_modify
                            return response
                    else:
                        part_to_modify = response['payload']['google']['richResponse']

                        if request.data['queryResult']['languageCode'] == 'pl':
                            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Nie ma żadnej odpowiedzi dla tego zapytania. " \
                                                                                           "Podaj jeszcze raz numer id lub " \
                                                                                           "wybierz co chcesz jeszcze zrobić"
                            part_to_modify['items'][0]['simpleResponse']['displayText'] = "Nie ma żadnej odpowiedzi dla tego zapytania." \
                                                                                          " Podaj jeszcze raz numer id lub " \
                                                                                          "wybierz co chcesz jeszcze zrobić"
                            part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                             {"title": "Zapytania"}, {"title": "Konto"}, {"title": "Inne"}]
                        elif request.data['queryResult']['languageCode'] == 'en':
                            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "There is no answer for this inquiry. " \
                                                                                           "Enter the id number again or choose " \
                                                                                           "what you want to do next"
                            part_to_modify['items'][0]['simpleResponse']['displayText'] = "There is no answer for this inquiry. " \
                                                                                          "Enter the id number again or choose " \
                                                                                          "what you want to do next"
                            part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                             {"title": "Inquiries"}, {"title": "Account"}, {"title": "Others"}]

                        response['payload']['google']['richResponse'] = part_to_modify

                        return response
                else:
                    part_to_modify = response['payload']['google']['richResponse']

                    if request.data['queryResult']['languageCode'] == 'pl':
                        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Nie możesz pobrać odpowiedzi dla tego zapytania. " \
                                                                                       "Podaj jeszcze raz numer id lub " \
                                                                                       "wybierz co chcesz jeszcze zrobić"
                        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Nie możesz pobrać odpowiedzi dla tego z" \
                                                                                      "apytania. Podaj jeszcze raz numer id lub " \
                                                                                      "wybierz co chcesz jeszcze zrobić"
                        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
                    elif request.data['queryResult']['languageCode'] == 'en':
                        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "You can't get an answer for this " \
                                                                                       "inquiry. Enter the id number again or choose " \
                                                                                       "what you want to do next"
                        part_to_modify['items'][0]['simpleResponse']['displayText'] = "You can't get an answer for this inquiry. " \
                                                                                      "Enter the id number again or choose " \
                                                                                      "what you want to do next"
                        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

                    response['payload']['google']['richResponse'] = part_to_modify

                    return response
            else:
                part_to_modify = response['payload']['google']['richResponse']

                if request.data['queryResult']['languageCode'] == 'pl':
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Nie ma zapytania o podanym przez Ciebie " \
                                                                                   "numerze id. Podaj jeszcze raz numer id lub " \
                                                                                   "wybierz co chcesz jeszcze zrobić"
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = "Nie ma zapytania o podanym numerze id. " \
                                                                                  "Podaj jeszcze raz numer id lub " \
                                                                                  "wybierz co chcesz jeszcze zrobić"
                    part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                     {"title": "Konto"}, {"title": "Inne"}]
                elif request.data['queryResult']['languageCode'] == 'en':
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "There is no inquiry about the ID number " \
                                                                                   "you provided. Enter the id number again " \
                                                                                   "or choose what you want to do next"
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = "There is no query for the given id number. " \
                                                                                  "Enter the id number again or choose " \
                                                                                  "what you want to do next"
                    part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                     {"title": "Account"}, {"title": "Others"}]

                response['payload']['google']['richResponse'] = part_to_modify

                return response
        else:
            return account_exist
    else:
        access_token = "There is no"
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        return account_exist


def ask_search_response_for(request):
    """
    Creates response with prompting user to give choice: search response for offer or order
    :param request: POST request from "Ask search response for" Dialogflow intent
    :return: JSON with prompting user to give choice: search response for offer or order
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyszukać odpowiedzi, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyszukać odpowiedzi. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't search response, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't search response. Create an account by selecting the option below \"Sign up\""

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

            part_to_modify = response['payload']['google']

            if request.data['queryResult']['languageCode'] == 'pl':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Chcesz wyszukać odpowiedź do oferty " \
                                                                                               "czy do zamówienia?"
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Chcesz wyszukać odpowiedź do oferty " \
                                                                                               "czy do zamówienia?"
                part_to_modify['richResponse']['suggestions'] = [{"title": "Oferta"}, {"title": "Zamówienie"}]
            elif request.data['queryResult']['languageCode'] == 'en':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Do you want to search an answer " \
                                                                                               "to the offer or to the order?"
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Do you want to search an answer " \
                                                                                              "to the offer or to the order?"
                part_to_modify['richResponse']['suggestions'] = [{"title": "Offer"}, {"title": "Order"}]

            response['payload']['google'] = part_to_modify
            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/search_response_for".format(session_id),
                "lifespanCount": 3
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


def ask_search_response_for_offer(request):
    """
    Creates response with prompting user to give data to search offer
    :param request: POST request from "Ask search response for offer" Dialogflow intent
    :return: JSON with prompting user to give data to search offer
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyszukać odpowiedzi, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyszukać odpowiedzi. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't search response, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't search response. Create an account by selecting the option below \"Sign up\""

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

            part_to_modify = response['payload']['google']

            if request.data['queryResult']['languageCode'] == 'pl':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Podaj dane dla jednej oferty jak na przykład" \
                                                                                               " miejsce odjazdu, miejsce docelowe, " \
                                                                                               "data odjazdu i tym podobne. Możesz zamiast" \
                                                                                               " tego podać id oferty"
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Podaj dane dla jednej  oferty jak na przykład" \
                                                                                               " miejsce odjazdu, miejsce docelowe, " \
                                                                                               "data odjazdu i tym podobne. Możesz zamiast" \
                                                                                               " tego podać id oferty"
                part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                                     {"title": "Konto"}, {"title": "Inne"}]
            elif request.data['queryResult']['languageCode'] == 'en':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Provide data for one offer such as place of departure," \
                                                                                               " destination, departure date etc." \
                                                                                               " You can enter the offer id instead"
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Provide data for one offer such as place of departure," \
                                                                                               " destination, departure date etc." \
                                                                                               " You can enter the offer id instead"
                part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                                     {"title": "Account"}, {"title": "Others"}]

            response['payload']['google'] = part_to_modify
            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/response_for_offer".format(session_id),
                "lifespanCount": 3
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


def search_responses_for_offer(request):
    """
    Searches responses for offer given in request
    :param request: POST request from "Get offers for inquiry" Dialogflow intent
    :return: JSON with offers to display and offers in created context "offers_for_inquiry"
    """
    parameters = request.data["queryResult"]["parameters"]
    if parameters["geo-city"] != "" and parameters["geo-city1"] != "":
        result = get_offers_in_list(request)
        if type(result) is not list:
            return result
    elif parameters["number"] != "":
        result = parameters["number"]
        if Offer.objects.filter(pk=result).count() == 0:
            with open('api/response.json') as json_file:
                response = json.load(json_file)

            part_to_modify = response['payload']['google']

            if request.data['queryResult']['languageCode'] == 'pl':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Nie istnieje oferta o podanym" \
                                                                                               "przez Ciebie numerze id. Podaj numer id jeszcze " \
                                                                                               "raz lub wybierz jedną z poniższych opcji."
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Nie istnieje oferta o podanym" \
                                                                                               " id. Podaj numer id jeszcze " \
                                                                                               "raz lub wybierz jedną z poniższych opcji."
                part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                                 {"title": "Konto"}, {"title": "Inne"}]
            elif request.data['queryResult']['languageCode'] == 'en':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "There isn't offer with the " \
                                                                                               "id number you provided. " \
                                                                                               "Enter the id number again or select" \
                                                                                               " one of the options below."
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "There isn't offer with the " \
                                                                                               "id number you provided. " \
                                                                                               "Enter the id number again or select" \
                                                                                               " one of the options below."
                part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                                 {"title": "Inquiries"},
                                                                 {"title": "Account"}, {"title": "Others"}]
            response['payload']['google'] = part_to_modify

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/response_for_offer".format(
                    session_id),
                "lifespanCount": 3
            }
            list_with_context = list()
            list_with_context.append(context)
            response["outputContexts"] = list_with_context
            return response
    if type(result) is list:
        if len(result) > 1:
            with open('api/response.json') as json_file:
                response = json.load(json_file)

            part_to_modify = response['payload']['google']

            if request.data['queryResult']['languageCode'] == 'pl':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Musisz podać dane tylko dla" \
                                                                                               " pojedynczej oferty."
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Musisz podać dane tylko dla" \
                                                                                               " pojedynczej oferty."
                part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                                 {"title": "Zapytania"},
                                                                 {"title": "Konto"}, {"title": "Inne"}]
            elif request.data['queryResult']['languageCode'] == 'en-us':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "You must provide data only for a single offer."
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "You must provide data only for a single offer."
                part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                                 {"title": "Inquiries"},
                                                                 {"title": "Account"}, {"title": "Others"}]
                response['payload']['google'] = part_to_modify

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/response_for_offer".format(
                    session_id),
                "lifespanCount": 3
            }
            list_with_context = list()
            list_with_context.append(context)
            response["outputContexts"] = list_with_context

            return response
        else:
            result = result[0].pk
    if InquiriesOffers.objects.filter(offer=result).count() > 0:
        inquiries_offers = InquiriesOffers.objects.filter(offer=result)
        inquiries = list()
        for io in inquiries_offers:
            inquiries.append(io.inquiry)
        responses = list()
        for i in inquiries:
            if InquiriesResponses.objects.filter(inquiry=i).count() > 0:
                responses_temp = InquiriesResponses.objects.filter(inquiry=i)
                for rt in responses_temp:
                    responses.append(rt.response)
        if len(responses) == 1:
            speech_text_pl = "Odpowiedź do podanej oferty"
            display_text_pl = "Odpowiedź do podanej oferty"
            speech_text_en = "Here's the answer for offer"
            display_text_en = "Here's the answer for offer"

            basic_card_pl = {
                "basicCard": {
                    "title": "Odpowiedź nr {}".format(responses[0].pk),
                    "formattedText": "___Tytuł:___  {}  \n__Data:__  {}  \n  \n__Tekst:__  {}"
                        .format(responses[0].title, responses[0].date, responses[0].text)
                }
            }
            basic_card_en = {
                "basicCard": {
                    "title": "Response number {}".format(responses[0].pk),
                    "formattedText": "___Title:___  {}  \n__Date:__  {}  \n  \n__Text:__  {}"
                        .format(responses[0].title, responses[0].date, responses[0].text)
                }
            }

            suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                              {"title": "Konto"}, {"title": "Inne"}]
            suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                              {"title": "Account"}, {"title": "Others"}]

            one_response = responses[0]
            one_response.readed = True
            one_response.save()

            with open('api/response.json') as json_file:
                response = json.load(json_file)

            part_to_modify = response['payload']['google']['richResponse']
            if request.data['queryResult']['languageCode'] == 'pl':
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                part_to_modify['items'].append(basic_card_pl)
                part_to_modify['suggestions'] = suggestions_pl
            elif request.data['queryResult']['languageCode'] == 'en':
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                part_to_modify['items'].append(basic_card_en)
                part_to_modify['suggestions'] = suggestions_en

            response['payload']['google']['richResponse'] = part_to_modify

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/response_for_offer".format(
                    session_id),
                "lifespanCount": 3
            }
            list_with_context = list()
            list_with_context.append(context)
            response["outputContexts"] = list_with_context

            return response
        elif len(responses) > 1:
            counter = 0
            responses_to_insert = list()
            if request.data['queryResult']['languageCode'] == 'pl':
                with open('api/offers_list.json') as json_file:
                    responses_list = json.load(json_file)
                part_to_modify = responses_list['payload']['google']["systemIntent"]["data"]["listSelect"]
                part_to_modify["title"] = "Odpowiedzi dla podanej oferty"

                for response in responses:
                    if counter < 30:
                        responses_to_insert.append({
                            "optionInfo": {
                                "key": "{}".format(response.pk)
                            },
                            "description": "Tytuł: {}, Data: {}, Tekst: {}".format(
                                response.title, response.date, response.text),
                            "title": "Odpowiedź nr {}".format(response.pk)
                        }
                        )
                        response.readed = True
                        response.save()
                        counter += 1
                    else:
                        break

                part_to_modify["items"] = responses_to_insert
                responses_list['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
                part_to_modify = responses_list['payload']['google']["richResponse"]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Odpowiedzi dla podanej oferty"
                part_to_modify['items'][0]['simpleResponse']['displayText'] = "Odpowiedzi dla podanej oferty"
                part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                 {"title": "Konto"}, {"title": "Inne"}]
                responses_list['payload']['google']["richResponse"] = part_to_modify

                session_id = request.data["queryResult"]["outputContexts"][0]["name"]
                session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
                session_id = session_id.lstrip("sessions/").rstrip("/contexts")
                context = {
                    "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/response_for_offer".format(
                        session_id),
                    "lifespanCount": 3
                }
                list_with_context = list()
                list_with_context.append(context)
                responses_list["outputContexts"] = list_with_context

                return responses_list
            elif request.data['queryResult']['languageCode'] == 'en':
                with open('api/offers_list.json') as json_file:
                    responses_list = json.load(json_file)
                part_to_modify = responses_list['payload']['google']["systemIntent"]["data"]["listSelect"]
                part_to_modify["title"] = "Responses for given offer"

                for response in responses:
                    if counter < 30:
                        responses_to_insert.append({
                            "optionInfo": {
                                "key": "{}".format(response.pk)
                            },
                            "description": "Title: {}, Date: {}, Text: {}".format(
                                response.title, response.date, response.text),
                            "title": "Response number {}".format(response.pk)
                        }
                        )
                        response.readed = True
                        response.save()
                        counter += 1
                    else:
                        break

                part_to_modify["items"] = responses_to_insert
                responses_list['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
                part_to_modify = responses_list['payload']['google']["richResponse"]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Responses for given offer"
                part_to_modify['items'][0]['simpleResponse']['displayText'] = "Responses for given offer"
                part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                 {"title": "Account"}, {"title": "Others"}]
                responses_list['payload']['google']["richResponse"] = part_to_modify

                session_id = request.data["queryResult"]["outputContexts"][0]["name"]
                session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
                session_id = session_id.lstrip("sessions/").rstrip("/contexts")
                context = {
                    "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/response_for_offer".format(
                        session_id),
                    "lifespanCount": 3
                }
                list_with_context = list()
                list_with_context.append(context)
                responses_list["outputContexts"] = list_with_context

                return responses_list
        else:
            with open('api/response.json') as json_file:
                response = json.load(json_file)

            part_to_modify = response['payload']['google']

            if request.data['queryResult']['languageCode'] == 'pl':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Nie ma odpowiedzi dla podanej oferty"
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Nie ma odpowiedzi dla podanej oferty"
                part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                                 {"title": "Konto"}, {"title": "Inne"}]
            elif request.data['queryResult']['languageCode'] == 'en':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "There is no answer for the given offer."
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "There is no answer for the given offer."
                part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                                 {"title": "Account"}, {"title": "Others"}]
                response['payload']['google'] = part_to_modify

            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/response_for_offer".format(
                    session_id),
                "lifespanCount": 3
            }
            list_with_context = list()
            list_with_context.append(context)
            response["outputContexts"] = list_with_context

            return response
    else:
        with open('api/response.json') as json_file:
            response = json.load(json_file)

        part_to_modify = response['payload']['google']

        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Nie ma odpowiedzi dla podanej oferty"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Nie ma odpowiedzi dla podanej oferty"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                             {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en-us':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "There is no answer for the given offer."
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "There is no answer for the given offer."
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                             {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]
            response['payload']['google'] = part_to_modify

        session_id = request.data["queryResult"]["outputContexts"][0]["name"]
        session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
        session_id = session_id.lstrip("sessions/").rstrip("/contexts")
        context = {
            "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/response_for_offer".format(
                session_id),
            "lifespanCount": 3
        }
        list_with_context = list()
        list_with_context.append(context)
        response["outputContexts"] = list_with_context

        return response


def ask_create_response_to_admnin(request):
    """
    Creates response with prompting user to give id admin response
    :param request: POST request from "Ask create response to admin" Dialogflow intent
    :return: Json with prompting user to give id admin response
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz stworzyć odpowiedzi, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz stworzyć odpowiedzi. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't create response, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't create response. Create an account by selecting the option below \"Sign up\""

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

            part_to_modify = response['payload']['google']

            if request.data['queryResult']['languageCode'] == 'pl':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = \
                    "Podaj id wiadomości admina, na którą mam odpowiedzieć"
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = \
                    "Podaj id wiadomości admina, na którą mam odpowiedzieć"
                part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                                 {"title": "Zapytania"}, {"title": "Konto"},
                                                                 {"title": "Inne"}]
            elif request.data['queryResult']['languageCode'] == 'en':
                part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = \
                    "Provide the ID of the admin message to which I will to respond"
                part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = \
                    "Provide the ID of the admin message to which I will to respond"
                part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                                 {"title": "Inquiries"},
                                                                 {"title": "Account"}, {"title": "Others"}]

            response['payload']['google'] = part_to_modify
            session_id = request.data["queryResult"]["outputContexts"][0]["name"]
            session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
            session_id = session_id.lstrip("sessions/").rstrip("/contexts")
            context = {
                "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/create_response_to_admin".format(session_id),
                "lifespanCount": 5
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


def create_response_to_admin(request):
    """
    Create response with basic card that contains admin response for which will be create user response. Prompting user to give
    response title. If admin response with given id from request doesn't exist return info about no create response
    :param request: POST requst from "Create response to admin" Dialogflow intent
    :return: JSON with basic card that contains admin response for which will be create user response, prompt user to give
    response title or info about no create response
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz stworzyć odpowiedzi, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz " \
                         "założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz stworzyć odpowiedzi. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't create response, because you don't have an account yet. If you want to create a best" \
                         " transport Poland account, select the option \"Sign up\" below"
    display_spoken_en = "You can't create response. Create an account by selecting the option below \"Sign up\""

    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        account_exist = check_token(access_token, language, response_spoken_pl, display_spoken_pl, response_spoken_en,
                                    display_spoken_en)
        if account_exist == "token exist":
            response_to_customer = request.data["queryResult"]["parameters"]["number"]
            if ResponseToCustomer.objects.filter(pk=response_to_customer).count() == 1:
                response_to_customer = ResponseToCustomer.objects.get(pk=response_to_customer)
            if InquiriesResponses.objects.filter(response=response_to_customer).count() > 0:
                inquiries = InquiriesResponses.objects.filter(response=response_to_customer)
                profile_token = Token.objects.get(key=access_token)
                user = profile_token.user
                profile = Profile.objects.get(user=user)
                if profile.pk == inquiries[0].inquiry.customer.pk:
                    speech_text_pl = "Odpowiedź dla której będzie tworzona wiadomość. Podaj tytuł wiadomości."
                    display_text_pl = "Odpowiedź dla której będzie tworzona wiadomość. Podaj tytuł wiadomości."
                    speech_text_en = "The answer for which the message will be created. Enter the title of the message."
                    display_text_en = "The answer for which the message will be created. Enter the title of the message."

                    basic_card_pl = {
                        "basicCard": {
                            "title": "Odpowiedź nr {}".format(response_to_customer.pk),
                            "formattedText": "___Tytuł:___  {}  \n__Data:__  {}  \n  \n__Tekst:__  {}"
                                .format(response_to_customer.title, response_to_customer.date, response_to_customer.text)
                        }
                    }
                    basic_card_en = {
                        "basicCard": {
                            "title": "Response number {}".format(response_to_customer.pk),
                            "formattedText": "___Title:___  {}  \n__Date:__  {}  \n  \n__Text:__  {}"
                                .format(response_to_customer.title, response_to_customer.date, response_to_customer.text)
                        }
                    }

                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                      {"title": "Account"}, {"title": "Others"}]

                    one_response = response_to_customer
                    one_response.readed = True
                    one_response.save()

                    with open('api/response.json') as json_file:
                        response = json.load(json_file)

                    part_to_modify = response['payload']['google']['richResponse']
                    if request.data['queryResult']['languageCode'] == 'pl':
                        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                        part_to_modify['items'].append(basic_card_pl)
                        part_to_modify['suggestions'] = suggestions_pl
                    elif request.data['queryResult']['languageCode'] == 'en':
                        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                        part_to_modify['items'].append(basic_card_en)
                        part_to_modify['suggestions'] = suggestions_en

                    response['payload']['google']['richResponse'] = part_to_modify

                    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
                    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
                    session_id = session_id.lstrip("sessions/").rstrip("/contexts")
                    context = {
                        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/create_response_to_admin".format(
                            session_id),
                        "lifespanCount": 5,
                        "parameters": {
                            "admin_response": "{}".format(str(response_to_customer.pk))
                        }
                    }
                    list_with_context = list()
                    list_with_context.append(context)
                    response["outputContexts"] = list_with_context

                    return response
                else:
                    with open('api/response.json') as json_file:
                        response = json.load(json_file)

                    part_to_modify = response['payload']['google']

                    if request.data['queryResult']['languageCode'] == 'pl':
                        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = \
                            "Nie masz takiej odpowiedzi od administratora systemu"
                        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = \
                            "Nie masz takiej odpowiedzi od administartora systemu"
                        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                                         {"title": "Zapytania"}, {"title": "Konto"},
                                                                         {"title": "Inne"}]
                    elif request.data['queryResult']['languageCode'] == 'en':
                        part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = \
                            "You do not have such a response from the system administrator"
                        part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = \
                            "You do not have such a response from the system administrator"
                        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                                         {"title": "Inquiries"},
                                                                         {"title": "Account"}, {"title": "Others"}]

                    response['payload']['google'] = part_to_modify
                    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
                    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
                    session_id = session_id.lstrip("sessions/").rstrip("/contexts")
                    context = {
                        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/create_response_to_admin".format(
                            session_id),
                        "lifespanCount": 5
                    }
                    list_with_context = list()
                    list_with_context.append(context)
                    response["outputContexts"] = list_with_context
                    return response
            else:
                with open('api/response.json') as json_file:
                    response = json.load(json_file)

                part_to_modify = response['payload']['google']

                if request.data['queryResult']['languageCode'] == 'pl':
                    part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = \
                        "Nie masz takiej odpowiedzi od administratora systemu"
                    part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = \
                        "Nie masz takiej odpowiedzi od administartora systemu"
                    part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                                     {"title": "Zapytania"}, {"title": "Konto"},
                                                                     {"title": "Inne"}]
                elif request.data['queryResult']['languageCode'] == 'en-us':
                    part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = \
                        "You do not have such a response from the system administrator"
                    part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = \
                        "You do not have such a response from the system administrator"
                    part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                                     {"title": "Inquiries"},
                                                                     {"title": "Account"}, {"title": "Others"}]

                response['payload']['google'] = part_to_modify
                session_id = request.data["queryResult"]["outputContexts"][0]["name"]
                session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
                session_id = session_id.lstrip("sessions/").rstrip("/contexts")
                context = {
                    "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/create_response_to_admin".format(
                        session_id),
                    "lifespanCount": 5
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
