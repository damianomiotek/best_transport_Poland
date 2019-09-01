import re
from api.serializers import *
from api.common import *


def offers(request):
    """
    Create Json response with offers menu
    :param request: POST request from "Offers" dialogflow intent
    :return: Json response that contains spoken and display prompt and also list as Dialogflow conversation item
    """
    speech_text_pl = "Która opcja Cię interesuje?"
    display_text_pl = "Która opcja Cię interesuje?"
    list_pl = {
        "intent": "actions.intent.OPTION",
        "data": {
            "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
            "listSelect": {
                "items": [
                    {
                        "optionInfo": {
                            "key": "Przeglądaj oferty",
                            "synonyms": [
                                "Przejrzyj oferty"
                            ]
                        },
                        "title": "Przeglądaj oferty"
                    },
                    {
                        "optionInfo": {
                            "key": "Wyszukaj oferty",
                            "synonyms": [
                                "Znajdź oferty",
                                "Znajdź ofertę"
                            ]
                        },
                        "title": "Wyszukaj oferty"
                    },
                    {
                        "optionInfo": {
                            "key": "Wyszukaj ofertę po id",
                            "synonyms": [
                                "Znajdź ofertę po id"
                            ]
                        },
                        "title": "Wyszukaj ofertę po id"
                    },
                    {
                        "optionInfo": {
                            "key": "Do kiedy jest ważna oferta",
                            "synonyms": [
                                "Ważnosć oferty",
                                "Do kiedy oferta będzie aktualna",
                            ]
                        },
                        "title": "Do kiedy jest ważna oferta"
                    }
                ]
            }
        }
    }
    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                      {"title": "Inne"}]

    speech_text_en = "Which option are you interested in?"
    display_text_en = "Which option are you interested in?"
    list_en = {
        "intent": "actions.intent.OPTION",
        "data": {
            "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
            "listSelect": {
                "items": [
                    {
                        "optionInfo": {
                            "key": "Browse offers",
                            "synonyms": [
                                "View offers",
                                "Display offers"
                            ]
                        },
                        "title": "Browse offers"
                    },
                    {
                        "optionInfo": {
                            "key": "Search offers",
                            "synonyms": [
                                "Search active offers"
                            ]
                        },
                        "title": "Search offers"
                    },
                    {
                        "optionInfo": {
                            "key": "Search offer after id",
                            "synonyms": [
                                "Search offer according to id"
                            ]
                        },
                        "title": "Search offer after id"
                    },
                    {
                        "optionInfo": {
                            "key": "Until when is the offer valid",
                            "synonyms": [
                                "Offer valid",
                                "Until when is the offer valid?",
                            ]
                        },
                        "title": "Until when is the offer valid"
                    }
                ]
            }
        }
    }
    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                      {"title": "Others"}]

    with open('api/response.json') as json_file:
        offers = json.load(json_file)

    part_to_modify = offers['payload']['google']

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

    offers['payload']['google'] = part_to_modify
    return offers


def browse_offers(request):
    """
    Creates Dialogflow list with best transport offers or basic card with one offer or response about no offers
    :param request: POST request from "Browse offers" Dialogflow intent
    :return: JSON with list contains best transport offers or basic card with one offer or response about no offers
    """
    active_offers = Offer.objects.filter(is_active=True)
    offers_pl = 0
    offers_en = 0
    for offer in active_offers:
        if offer.language == 'pl':
            offers_pl += 1
        elif offer.language == 'en':
            offers_en += 1

    counter = 0
    offers_to_insert = []
    if request.data['queryResult']['languageCode'] == 'pl' and offers_pl > 1:
        with open('api/offers_list.json') as json_file:
            offers_list = json.load(json_file)
        part_to_modify = offers_list['payload']['google']["systemIntent"]["data"]["listSelect"]
        part_to_modify["title"] = "Oferty"

        for offer in active_offers:
            if counter < 30:
                if offer.language == 'pl':
                    offers_to_insert.append({
                    "optionInfo": {
                        "key": "{}".format(offer.pk)
                    },
                    "description": "{}({}) -> {}({}) liczba palet: {}, data odjazdu: {}, cena: {}".format(
                        offer.loading_place.place.post_place, offer.loading_place.place.country,
                        offer.destination.place.post_place, offer.destination.place.country, offer.pallets_number,
                        offer.loading_place.date, offer.price),
                    "title": "Oferta nr {}".format(offer.pk)
                })
                counter += 1
            else:
                break

        part_to_modify["items"] = offers_to_insert
        offers_list['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
        part_to_modify = offers_list['payload']['google']["richResponse"]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Oto lista aktualnych ofert"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Oto lista aktualnych ofert"
        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                         {"title": "Konto"}, {"title": "Inne"}]
        offers_list['payload']['google']["richResponse"] = part_to_modify
        return offers_list
    elif request.data['queryResult']['languageCode'] == 'en' and offers_en > 1:
        with open('api/offers_list.json') as json_file:
            offers_list = json.load(json_file)
        part_to_modify = offers_list['payload']['google']["systemIntent"]["data"]["listSelect"]
        part_to_modify["title"] = "Offers"

        for offer in active_offers:
            if counter < 30:
                if offer.language == 'en':
                    offers_to_insert.append({
                    "optionInfo": {
                        "key": "{}".format(offer.pk)
                    },
                    "description": "{}({}) -> {}({}) number of pallets: {}, departure: {}, price: {}".format(
                        offer.loading_place.place.post_place, offer.loading_place.place.country,
                        offer.destination.place.post_place, offer.destination.place.country, offer.pallets_number,
                        offer.loading_place.date, offer.price),
                    "title": "Offer nr {}".format(offer.pk)
                })
                counter += 1
            else:
                break

        part_to_modify["items"] = offers_to_insert
        offers_list['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
        part_to_modify = offers_list['payload']['google']["richResponse"]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Here is a list of current offers"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Here is a list of current offers"
        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                                         {"title": "Others"}]
        offers_list['payload']['google']["richResponse"] = part_to_modify
        return offers_list
    elif request.data['queryResult']['languageCode'] == 'pl' and offers_pl == 1:
        for offer in active_offers:
            if offer.language == 'pl':
                offer_pl = offer
        speech_text_pl = "Obecnie mamy tylko jedną aktualną ofertę"
        display_text_pl = "Obecnie mamy tylko jedną aktualną ofertę"
        basic_card_pl = {
            "basicCard": {
                "title": "Oferta nr {}".format(offer_pl.pk),
                "formattedText": "___Skąd:___  {}({})  \n__Dokąd:__  {}({})  \n  \n__Odjazd:__  {} o godz. {}"
                                 "  \n__Przyjazd:__  {} o godz. {}  \n  \n__Liczba palet:__  {}  \n"
                                 "__Uwagi:__  {}  \n  \n__Cena:__  {} pln"
                    .format(offer_pl.loading_place.place.post_place, offer_pl.loading_place.place.country,
                            offer_pl.destination.place.post_place, offer_pl.destination.place.country,
                            offer_pl.loading_place.date, offer_pl.loading_place.hour,
                            offer_pl.destination.date, offer_pl.destination.hour,
                            offer_pl.pallets_number, offer_pl.remarks, offer_pl.price)
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
    elif request.data['queryResult']['languageCode'] == 'en' and offers_en == 1:
        for offer in active_offers:
            if offer.language == 'en':
                offer_en = offer
        speech_text_en = "We currently have only one current offer"
        display_text_en = "We currently have only one current offer"
        basic_card_en = {
            "basicCard": {
                "title": "Offer nr {}".format(offer_en.pk),
                "formattedText": "___From:___  {}({})  \n__To:__  {}({})  \n  \n__Departure:__  {} at {}"
                                 "  \n__Arrival:__  {} at {}  \n  \n__Pallets number:__  {}  \n"
                                 "__Remarks:__  {}  \n  \n__Price:__  {} pln"
                    .format(offer_en.loading_place.place.post_place, offer_en.loading_place.place.country,
                            offer_en.destination.place.post_place, offer_en.destination.place.country,
                            offer_en.loading_place.date, offer_en.loading_place.hour,
                            offer_en.destination.date, offer_en.destination.hour,
                            offer_en.pallets_number, offer_en.remarks, offer_en.price)
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
            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Brak ofert w serwisie. Co chcesz jeszcze zrobić?"
            part_to_modify['items'][0]['simpleResponse']['displayText'] = "Brak ofert w seriwsie. Co chcesz jeszcze zrobić?"
            part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en-us':
            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "No offers on the site. What do you want to do next?"
            part_to_modify['items'][0]['simpleResponse']['displayText'] = "No offers on the site. What do you want to do next?"
            part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google']["richResponse"] = part_to_modify
        return response


def ask_search_offers(request):
    """
    Creates response with prompting user to give data to search offer/offers
    :param request: POST request from "Ask search offers" Dialogflow intent
    :return: JSON with response prompting user to give data to search offer/offers
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)
    part_to_modify = response['payload']['google']["richResponse"]

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "<speak>Podaj dane po jakich chcesz wyszukać ofertę " \
                                                                       "lub oferty.<break time=\"200ms\"/> Na przykład: Z Amsterdamu do Warszawy, " \
                                                                       "dwadzieścia palet za 4100 zł.<break time=\"100ms\"/> " \
                                                                       "Odjazd 10 maja o dwunastej, przyjazd 13 maja o " \
                                                                       "czternastej</speak>"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Podaj dane. Na przykład: Z Amsterdamu do Warszawy " \
                                                                      "20 palet za 4100 zł. Odjazd 10 maja o 12:00, " \
                                                                      "przyjazd 13 maja o 14:00. Nie musisz podawać wszystkich " \
                                                                      "informacji"
        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "<speak>Enter the data by which you want to search for " \
                                                                       "an offer or offers. <break time=\"200ms\"/> For example: From Amsterdam " \
                                                                       "to Warsaw, <say-as interpret-as=\"ordinal\">20</say-as>" \
                                                                       "pallets for PLN 4,100. <break time=\"100ms\"/> Departure on May 10 at 12:00, " \
                                                                       "arrival on May 13 at 2:00 PM.</speak>"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Enter the data. For example: From Amsterdam to Warsaw," \
                                                                      " 20 pallets for PLN 4,100. Departure on May 10 at" \
                                                                      " 12:00, arrival on May 13 at 2:00 PM. You don't have to " \
                                                                      "provide all the information"
        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                      {"title": "Others"}]

    response['payload']['google']["richResponse"] = part_to_modify
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/search_offers".format(
            session_id),
        "lifespanCount": 5
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context
    return response


def lack_searched_offer(request):
    """
    Creates response with info about not finding offers
    :param request: request from Dialogflow service
    :return: JSON with info about not finding offers
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)
    part_to_modify = response['payload']['google']["richResponse"]

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Brak ofert dla podanych parametrów. Co chcesz jeszcze zrobić?"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Brak ofert dla podanych parametrów. Co chcesz jeszcze zrobić?"
        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Lack offers for given parameters. What do you want to do next?"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Lack offers for given parameters. What do you want to do next?"
        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                         {"title": "Account"}, {"title": "Others"}]

    response['payload']['google']["richResponse"] = part_to_modify
    return response


def get_offers_in_list(request):
    """
    Searches offers by parameters from request
    :param request: POST request from Dialogflow service
    :return: dict with info about no find appropriate offers or list with found offers
    """
    parameters = request.data["queryResult"]["parameters"]
    result = list()
    is_go = True

    if "amount" in parameters["unit-currency"]:
        price = int(parameters["unit-currency"]["amount"]) + 500
        all_offers = Offer.objects.all()
        for offer in all_offers:
            if int(offer.price) <= price:
                result.append(offer)
        if len(result) == 0:
            is_go = False

    if parameters["number"] != "" and is_go:
        pallets_number = int(parameters["number"])
        result_temp = list()
        if len(result) > 0:
            for offer in result:
                if int(offer.pallets_number) >= pallets_number:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            offers = Offer.objects.all()
            for offer in offers:
                if int(offer.pallets_number) >= pallets_number:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif is_go is False:
        return lack_searched_offer(request)

    from_city = parameters["geo-city"]
    from_country = parameters["geo-country"]
    if from_city != "" and from_country != "" and is_go:
        result_temp = list()
        if len(result) > 0:
            for offer in result:
                if str(offer.loading_place.place.post_place) == from_city and str(
                        offer.loading_place.place.country) == from_country:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if offer.loading_place.place.post_place == from_city and offer.loading_place.place.country == from_country:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif from_city != "" and is_go:
        result_temp = list()
        if len(result) > 0:
            for offer in result:
                if str(offer.loading_place.place.post_place) == from_city:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if str(offer.loading_place.place.post_place) == from_city:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif from_country != "" and is_go:
        result_temp = list()
        if len(result) > 0:
            for offer in result:
                if str(offer.loading_place.place.country) == from_country:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if str(offer.loading_place.place.country) == from_country:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif is_go is False:
        return lack_searched_offer(request)

    to_city = parameters["geo-city1"]
    to_country = parameters["geo-country1"]
    if to_city != "" and to_country != "" and is_go:
        result_temp = list()
        if len(result) > 0:
            for offer in result:
                if str(offer.destination.place.post_place) == to_city and str(
                        offer.destination.place.country) == to_country:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if str(offer.destination.place.post_place) == to_city and str(
                        offer.destination.place.country) == to_country:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif to_city != "" and is_go:
        result_temp = list()
        if len(result) > 0:
            for offer in result:
                if str(offer.destination.place.post_place) == to_city:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if str(offer.destination.place.post_place) == to_city:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif to_country != "" and is_go:
        result_temp = list()
        if len(result) > 0:
            for offer in result:
                if str(offer.destination.place.country) == to_country:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if offer.destination.place.country == to_country:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif is_go is False:
        return lack_searched_offer(request)

    departure_date_hour = parameters["date-time"]
    arrival_date_hour = parameters["date-time1"]
    if "date_time" in departure_date_hour and "date_time" in arrival_date_hour and is_go:
        result_temp = list()
        departure_date_hour = parameters["date-time"]["date_time"]
        arrival_date_hour = parameters["date-time1"]["date_time"]
        departure_date = re.search(r"^.{10}", departure_date_hour).group()
        arrival_date = re.search(r"^.{10}", arrival_date_hour).group()
        if len(result) > 0:
            for offer in result:
                if str(offer.loading_place.date) == departure_date or str(offer.destination.date) == arrival_date:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if str(offer.loading_place.date) == departure_date or str(offer.destination.date) == arrival_date:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif "date_time" in departure_date_hour and is_go:
        result_temp = list()
        departure_date_hour = parameters["date-time"]["date_time"]
        departure_date = re.search(r"^.{10}", departure_date_hour).group()
        if len(result) > 0:
            for offer in result:
                if str(offer.loading_place.date) == departure_date:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if str(offer.loading_place.date) == departure_date:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif "date_time" in arrival_date_hour and is_go:
        result_temp = list()
        arrival_date_hour = parameters["date-time1"]["date_time"]
        arrival_date = re.search(r"^.{10}", arrival_date_hour).group()
        if len(result) > 0:
            for offer in result:
                if str(offer.destination.date) == arrival_date:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if str(offer.destination.date) == arrival_date:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif is_go is False:
        return lack_searched_offer(request)

    departure_date = parameters["date"]
    arrival_date = parameters["date1"]
    if departure_date != "" and arrival_date != "" and is_go:
        result_temp = list()
        if len(result) > 0:
            for offer in result:
                if str(offer.loading_place.date) == departure_date or str(offer.destination.date) == arrival_date:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if str(offer.loading_place.date) == departure_date or str(offer.destination.date) == arrival_date:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif departure_date != "" and is_go:
        result_temp = list()
        if len(result) > 0:
            for offer in result:
                if str(offer.loading_place.date) == departure_date:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if str(offer.loading_place.date) == departure_date:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif arrival_date != "" and is_go:
        result_temp = list()
        if len(result) > 0:
            for offer in result:
                if str(offer.destination.date) == arrival_date:
                    result_temp.append(offer)
            if len(result_temp) == 0:
                is_go = False
            else:
                result = result_temp
        else:
            all_offers = Offer.objects.all()
            for offer in all_offers:
                if str(offer.destination.date) == arrival_date:
                    result.append(offer)
            if len(result) == 0:
                is_go = False
    elif is_go is False:
        return lack_searched_offer(request)

    return result


def search_offers(request):
    """
    Search offers by given parameters and returns them in Json
    :param request: POST request from "Search offers" Dialogflow intent
    :return: Json with information of found offers or json with info about not finding offers
    """
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
                counter += 1
            else:
                break

        part_to_modify["items"] = offers_to_insert
        response['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
        part_to_modify = response['payload']['google']["richResponse"]
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Lista ofert o podanych przez Ciebie parametrach. " \
                                                                       "W czym mogę Ci jeszcze pomóc?"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Lista ofert o podanych przez Ciebie parametrach. " \
                                                                      "W czym mogę Ci jeszcze pomóc?"
        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                         {"title": "Konto"}, {"title": "Inne"}]
        response['payload']['google']["richResponse"] = part_to_modify
        return response

    elif request.data['queryResult']['languageCode'] == 'en' and offers_en > 1:
        with open('api/offers_list.json') as json_file:
            response = json.load(json_file)
        part_to_modify = response['payload']['google']['systemIntent']["data"]["listSelect"]

        counter = 0
        offers_to_insert = []
        part_to_modify["title"] = "Searched offers"
        for offer in response:
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
                counter += 1
            else:
                break

            part_to_modify["items"] = offers_to_insert
            response['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
            part_to_modify = response['payload']['google']["richResponse"]
            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "List of offers with the parameters you provided. " \
                                                                           "How can I help you?"
            part_to_modify['items'][0]['simpleResponse']['displayText'] = "List of offers with the parameters you provided. " \
                                                                          "How can I help you?"
            part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                             {"title": "Account"}, {"title": "Others"}]
        response['payload']['google']["richResponse"] = part_to_modify
        return response

    elif request.data['queryResult']['languageCode'] == 'pl' and offers_pl == 1:
        speech_text_pl = "Znaleziono jedną ofertę o podanych parametrach. W czym mogę Ci jeszcze pomóc?"
        display_text_pl = "Znaleziono jedną ofertę o podanych parametrach. W czym mogę Ci jeszcze pomóc?"

        for offer in result:
            if offer.language == 'pl':
                offer_pl = offer
                break

        basic_card_pl = {
            "basicCard": {
                "title": "Oferta nr {}".format(offer_pl.pk),
                "formattedText": "___Skąd:___  {}({})  \n__Dokąd:__  {}({})  \n  \n__Odjazd:__  {} o godz. {}"
                                 "  \n__Przyjazd:__  {} o godz. {}  \n  \n__Liczba palet:__  {}  \n"
                                 "__Uwagi:__  {}  \n  \n__Cena:__  {} pln"
                    .format(offer_pl.loading_place.place.post_place, offer_pl.loading_place.place.country,
                            offer_pl.destination.place.post_place, offer_pl.destination.place.country,
                            offer_pl.loading_place.date, offer_pl.loading_place.hour,
                            offer_pl.destination.date, offer_pl.destination.hour,
                            offer_pl.pallets_number, offer_pl.remarks, offer_pl.price)
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

    elif request.data['queryResult']['languageCode'] == 'en' and offers_en == 1:
        speech_text_en = "One offer was found with the given parameters. How can I help you?"
        display_text_en = "One offer was found with the given parameters. How can I help you?"

        for offer in result:
            if offer.language == 'en':
                offer_en = offer
                break

        basic_card_en = {
            "basicCard": {
                "title": "Offer number {}".format(offer_en.pk),
                "formattedText": "___From:___  {}({})  \n__To:__  {}({})  \n  \n__Departure:__  {} at {}"
                                 "  \n__Arrival:__  {} at {}  \n  \n__Pallets number:__  {}  \n"
                                 "__Remarks:__  {}  \n  \n__Price:__  {} pln"
                    .format(offer_en.loading_place.place.post_place, offer_en.loading_place.place.country,
                            offer_en.destination.place.post_place, offer_en.destination.place.country,
                            offer_en.loading_place.date, offer_en.loading_place.hour,
                            offer_en.destination.date, offer_en.destination.hour,
                            offer_en.pallets_number, offer_en.remarks, offer_en.price
                            )
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
        return lack_searched_offer(request)


def ask_search_offer_id(request):
    """
    Create response with prompting user to give offer id number to search this offer
    :param request: POST request from "Ask search offer id" Dialogflow intent
    :return: JSON with response prompting user to give offer id number
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)
    part_to_modify = response['payload']['google']["richResponse"]

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Podaj numer id szukanej oferty"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Podaj numer id szukanej oferty"
        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Enter the id number of the offer you are looking for"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Enter the id number of the offer you are looking for"
        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                         {"title": "Account"}, {"title": "Others"}]

    response['payload']['google']["richResponse"] = part_to_modify

    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/search_offer_by_id".format(
            session_id),
        "lifespanCount": 5
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context

    return response


def search_offer_id(request):
    """
    Creates response with searched offer by id, or response about no offer was founded
    :param request: POST request from "Search offer id" Dialogflow intent
    :return: JSON with info about searched offer by id or about no offer was founded
    """
    if Offer.objects.filter(pk=int(request.data["queryResult"]["parameters"]["number"])).count() > 0:
        offer = Offer.objects.get(pk=int(request.data["queryResult"]["parameters"]["number"]))
    else:
        offer = None
    if request.data['queryResult']['languageCode'] == 'pl' and offer:
        speech_text_pl = "Oto oferta o podanym przez Ciebie numerze id"
        display_text_pl = "Oto oferta o podanym przez Ciebie numerze id:"
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

        with open('api/response.json') as json_file:
            response = json.load(json_file)
        part_to_modify = response['payload']['google']['richResponse']

        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
        part_to_modify['items'].append(basic_card_pl)
        part_to_modify['suggestions'] = suggestions_pl
        response['payload']['google']['richResponse'] = part_to_modify
        return response
    elif request.data['queryResult']['languageCode'] == 'en' and offer:
        speech_text_en = "Here is the offer with the id number you provided"
        display_text_en = "Here is the offer with the id number you provided"
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
            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Nie ma oferty o podanym numerze id"
            part_to_modify['items'][0]['simpleResponse']['displayText'] = "Nie ma oferty o podanym numerze id"
            part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en-us':
            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "There is no offer with given id number"
            part_to_modify['items'][0]['simpleResponse']['displayText'] = "There is no offer with given id number"
            part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google']["richResponse"] = part_to_modify
        return response


def ask_until_when_offer_valid(request):
    """
    Creates response with prompting user to give data to search offer/offers
    :param request: POST request from "Ask until when offer valid" Dialogflow intent
    :return: JSON with response prompting user to give data to search offer/offers
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)
    part_to_modify = response['payload']['google']["richResponse"]

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Podaj dane oferty jak np. data odjazdu, data dostarczenia, " \
                                                                       "miejsce odjazdu, miejsce docelowe i tym podobne, lub numer" \
                                                                       " id oferty"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Podaj dane oferty jak np. data odjazdu, data dostarczenia, " \
                                                                       "miejsce odjazdu, miejsce docelowe itp., lub numer" \
                                                                       " id oferty"
        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Give offer data for example departure date, delivery date," \
                                                                       "departure place, target place e.t.c, or id offer number"
        part_to_modify['items'][0]['simpleResponse']['displayText'] = "Give offer data for example departure date, delivery date," \
                                                                       "departure place, target place e.t.c, or id offer number"
        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                         {"title": "Account"}, {"title": "Others"}]

    response['payload']['google']["richResponse"] = part_to_modify
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/offer_valid".format(
            session_id),
        "lifespanCount": 5
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context
    return response


def check_offer_valid(request):
    """
    Searches offers by the given parameters and check to when they are valid
    :param request: POST request from "Check offer valid" Dialogflow intent
    :return: JSON with info about valid of offers or with info about no offers found
    """
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

    if request.data['queryResult']['languageCode'] == 'pl' and offers_pl > 0:
        speech_text = ""
        months_pl = {"01": "stycznia", "02": "lutego", "03": "marca", "04": "kwietnia", "05": "maja", "06": "czerwca",
                     "07": "lipca", "08": "sierpnia", "09": "września", "10": "października", "11": "listopada",
                     "12": "grudnia"}
        hours = {1: "pierwszej", 2: "drugiej", 3: "trzeciej", 4: "czwartej", 5: "piątej", 6: "szóstej", 7: "siódmej",
                 8: "ósmej", 9: "dziewiątej", 10: "dziesiątej", 11: "jedenastej", 12: "dwunatsej", 13: "trzynastej",
                 14: "czternatsej", 15: "piętnastej", 16: "szesnastej", 17: "siedemnastej", 18: "osiemnastej", 19: "dziewiętnastej",
                 20: "dwudziestej", 21: "dwudziestej pierwszej", 22: "dwudziestej drugiej", 23: "dwudziestej trzeciej",
                 0: "północy"}
        for offer in result:
            if offer.language == 'pl':
                date = str(offer.loading_place.date)
                day = date[8:]
                month = date[5:7]
                hour = str(offer.loading_place.hour)
                hour = int(hour[0:2])
                hour = hour - 2
                if hour == -2:
                    hour = 22
                elif hour == -1:
                    hour = 23
                speech_text += "Oferta nr {} jest ważna do {} {}, do godziny {} ".format(offer.pk, day, months_pl[month],
                                                                                         hours[hour])
        with open('api/response.json') as json_file:
            response = json.load(json_file)
        part_to_modify = response['payload']['google']['richResponse']
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text
        part_to_modify['items'][0]['simpleResponse']['displayText'] = speech_text
        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                         {"title": "Konto"}, {"title": "Inne"}]
        response['payload']['google']['richResponse'] = part_to_modify
        return response

    elif request.data['queryResult']['languageCode'] == 'en' and offers_en > 0:
        speech_text = ""
        months_en = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                     9: "September", 10: "October", 11: "November", 12: "December"}
        for offer in result:
            if offer.language == 'en':
                date = str(offer.loading_place.date)
                day = date[8:]
                month = date[5:7]
                hour = str(offer.loading_place.hour)
                hour = int(hour[0:2])
                hour = hour - 2
                if hour == -2:
                    hour = 22
                elif hour == -1:
                    hour = 23
                speech_text += "Offer number {} is valid to {} {}, to {} ".format(offer.pk, months_en[month], day, hour)

        with open('api/response.json') as json_file:
            response = json.load(json_file)
        part_to_modify = response['payload']['google']['richResponse']
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text
        part_to_modify['items'][0]['simpleResponse']['displayText'] = speech_text
        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google']['richResponse'] = part_to_modify
        return response
    else:
        return lack_searched_offer(request)


def check_offer_valid_id(request):
    """
    Check if offer is current after given in request offer id
    :param request: POST request from "Check offer valid id" Dialogflow intent
    :return: JSON with info if offer after given id is current
    """
    if Offer.objects.filter(pk=int(request.data["queryResult"]["parameters"]["number"])).count() == 1:
        offer = Offer.objects.get(pk=int(request.data["queryResult"]["parameters"]["number"]))
    else:
        offer = None

    if request.data['queryResult']['languageCode'] == 'pl' and offer:
        speech_text_pl = ""
        months_pl = {"01": "stycznia", "02": "lutego", "03": "marca", "04": "kwietnia", "05": "maja", "06": "czerwca",
                     "07": "lipca", "08": "sierpnia", "09": "września", "10": "pażdziernika", "11": "listopada",
                     "12": "grudnia"}
        hours = {1: "pierwszej", 2: "drugiej", 3: "trzeciej", 4: "czwartej", 5: "piątej", 6: "szóstej", 7: "siódmej",
                 8: "ósmej", 9: "dziewiątej", 10: "dziesiątej", 11: "jedenastej", 12: "dwunatsej", 13: "trzynastej",
                 14: "czternatsej", 15: "piętnastej", 16: "szesnastej", 17: "siedemnastej", 18: "osiemnastej",
                 19: "dziewiętnastej", 20: "dwudziestej", 21: "dwudziestej pierwszej", 22: "dwudziestej drugiej",
                 23: "dwudziestej trzeciej", 0: "północy"}
        date = str(offer.loading_place.date)
        day = date[8:]
        month = date[5:7]
        hour = str(offer.loading_place.hour)
        hour = int(hour[0:2])
        hour = hour - 2
        if hour == -2:
            hour = 22
        elif hour == -1:
            hour = 23
        speech_text_pl += "Oferta nr {} jest ważna do {} {}, do godziny {} ".format(offer.pk, day, months_pl[month],
                                                                                    hours[hour])

        suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                          {"title": "Inne"}]

        with open('api/response.json') as json_file:
            response = json.load(json_file)
        part_to_modify = response['payload']['google']['richResponse']

        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
        part_to_modify['items'][0]['simpleResponse']['displayText'] = speech_text_pl
        part_to_modify['suggestions'] = suggestions_pl
        response['payload']['google']['richResponse'] = part_to_modify
        return response
    elif request.data['queryResult']['languageCode'] == 'en' and offer:
        speech_text = ""
        months_en = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
                     9: "September", 10: "October", 11: "November", 12: "December"}
        date = str(offer.loading_place.date)
        day = date[8:]
        month = date[5:7]
        hour = str(offer.loading_place.hour)
        hour = int(hour[0:2])
        hour = hour - 2
        if hour == -2:
            hour = 22
        elif hour == -1:
            hour = 23
        speech_text += "Offer number {} is valid to {} {}, to {} ".format(offer.pk, months_en[month], day, hour)

        with open('api/response.json') as json_file:
            response = json.load(json_file)
        part_to_modify = response['payload']['google']['richResponse']
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text
        part_to_modify['items'][0]['simpleResponse']['displayText'] = speech_text
        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                         {"title": "Account"}, {"title": "Others"}]

        response['payload']['google']['richResponse'] = part_to_modify
        return response
    else:
        with open('api/response.json') as json_file:
            response = json.load(json_file)
        part_to_modify = response['payload']['google']["richResponse"]

        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Nie ma oferty o podanym numerze id"
            part_to_modify['items'][0]['simpleResponse']['displayText'] = "Nie ma oferty o podanym numerze id"
            part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en-us':
            part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "There is no offer with given id number"
            part_to_modify['items'][0]['simpleResponse']['displayText'] = "There is no offer with given id number"
            part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google']["richResponse"] = part_to_modify
        return response