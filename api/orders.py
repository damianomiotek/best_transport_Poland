import re
from api.serializers import *
from api.common import *
from rest_framework.authtoken.models import Token
import datetime
from api.offers import *
from api.models import *


def orders(request):
    """
    Creates Json response with orders menu
    :param request: POST request from "Orders" dialogflow intent
    :return: Json response that contains spoken and display prompt and also list as Dialogflow conversation item
    """
    speech_text_pl = "Oto lista opcji do wyboru"
    display_text_pl = "Lista opcji do wyboru"
    list_pl = {
        "intent": "actions.intent.OPTION",
        "data": {
            "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
            "listSelect": {
                "items": [
                    {
                        "optionInfo": {
                            "key": "Stwórz zlecenie",
                            "synonyms": [
                                "Tworzenie zamówienia",
                                "Złóż zlecenie"
                            ]
                        },
                        "title": "Stwórz zlecenie"
                    },
                    {
                        "optionInfo": {
                            "key": "Wyszukaj zlecenie",
                            "synonyms": [
                                "Wyszukiwanie zamówienia",
                                "Znajdź zamówienie"
                            ]
                        },
                        "title": "Wyszukaj zlecenie"
                    },
                    {
                        "optionInfo": {
                            "key": "Usuń zlecenie",
                            "synonyms": [
                                "Kasowanie zamówienie",
                                "Usuwanie zamówienia",
                            ]
                        },
                        "title": "Usuń zlecenie"
                    },
                    {
                        "optionInfo": {
                            "key": "Przeglądaj aktualne zlecenia",
                            "synonyms": [
                                "Przejrzyj aktualne zamówienia",
                                "Aktualne zamówienia",
                            ]
                        },
                        "title": "Przeglądaj aktualne zlecenia"
                    },
                    {
                        "optionInfo": {
                            "key": "Historia zleceń",
                            "synonyms": [
                                "Przeglądaj dawne zamówienia",
                                "Przejrzyj historyczne zamówienia",
                            ]
                        },
                        "title": "Historia zleceń"
                    },
                    {
                        "optionInfo": {
                            "key": "Czy zlecenie zostało przyjęte do realizacji",
                            "synonyms": [
                                "Czy zamówienie jest realizowane"
                            ]
                        },
                        "title": "Czy zlecenie zostało przyjęte do realizacji"
                    },
                    {
                        "optionInfo": {
                            "key": "Czy zlecenie zostało zrealizowane",
                            "synonyms": [
                                "Czy zrealizowano zamówienie"
                            ]
                        },
                        "title": "Czy zlecenie zostało zrealizowane"
                    },
                    {
                        "optionInfo": {
                            "key": "Czy do zlecenie są nowe odpowiedzi",
                            "synonyms": [
                                "Nowe odpowiedzi dla zamówienia"
                            ]
                        },
                        "title": "Czy do zlecenie są nowe odpowiedzi"
                    }
                ]
            }
        }
    }
    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                      {"title": "Inne"}]

    speech_text_en = "A list of options to choose from"
    display_text_en = "A list of options to choose from"
    list_en = {
        "intent": "actions.intent.OPTION",
        "data": {
            "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
            "listSelect": {
                "items": [
                    {
                        "optionInfo": {
                            "key": "Create an order",
                            "synonyms": [
                                "Create an order for me"
                            ]
                        },
                        "title": "Create an order"
                    },
                    {
                        "optionInfo": {
                            "key": "Search for the order",
                            "synonyms": [
                                "Search order"
                            ]
                        },
                        "title": "Search for the order"
                    },
                    {
                        "optionInfo": {
                            "key": "Delete an order",
                            "synonyms": [
                                "Order delete"
                            ]
                        },
                        "title": "Delete an order"
                    },
                    {
                        "optionInfo": {
                            "key": "Browse current orders",
                            "synonyms": [
                                "Current orders",
                            ]
                        },
                        "title": "Browse current orders"
                    },
                    {
                        "optionInfo": {
                            "key": "The history of orders",
                            "synonyms": [
                                "History orders"
                            ]
                        },
                        "title": "The history of orders"
                    },
                    {
                        "optionInfo": {
                            "key": "Is the order accepted for execution",
                            "synonyms": [
                                "Is the order agree for execution"
                            ]
                        },
                        "title": "Is the order accepted for execution"
                    },
                    {
                        "optionInfo": {
                            "key": "Has the order been executed",
                            "synonyms": [
                                "Is order executed"
                            ]
                        },
                        "title": "Has the order been executed"
                    },
                    {
                        "optionInfo": {
                            "key": "Are there any new answers to the order",
                            "synonyms": [
                                "New answers to the order"
                            ]
                        },
                        "title": "Are there any new answers to the order?"
                    }
                ]
            }
        }
    }
    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                      {"title": "Others"}]

    with open('api/response.json') as json_file:
        orders = json.load(json_file)

    part_to_modify = orders['payload']['google']

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

    orders['payload']['google'] = part_to_modify
    return orders


def get_performer(language):
    """
    Creates string with Best Transport company data
    :param language: language of conversation
    :return: string with Best Transport company data
    """
    best_transport = BestTransData.objects.get(email="kontakt@besttransport.com.pl")
    output_string = ""
    if language == 'pl':
        output_string = "{}, ulica: {}, {} {}, kraj: {}, {}, tel. {}".format(best_transport.address.place_name, best_transport.address.street,
                                                                            best_transport.address.post_code, best_transport.address.post_place,
                                                                            best_transport.address.country,
                                                                            best_transport.email, best_transport.phone_number)
    elif language == 'en':
        output_string = "{}, street: {}, {} {}, country: {}, {}, tel. {}".format(best_transport.address.place_name, best_transport.address.street,
                                                                            best_transport.address.post_code, best_transport.address.post_place,
                                                                            best_transport.address.country,
                                                                            best_transport.email, best_transport.phone_number)
    return output_string


def get_order_client(profile):
    """
    Create appropriate string with profile data
    :param profile: profile of user
    :return: string with profile data
    """
    profile_data = "{} {}, {}, tel. {}".format(profile.name, profile.surname, profile.email, profile.phone_number)
    if profile.company and profile.company.address:
        profile_data += "{}, ulica: {}, {} {}, {}".format(profile.company.address.place_name, profile.company.address.street,
                                                   profile.company.address.post_code, profile.company.address.post_place,
                                                   profile.company.address.country)
    return profile_data


def get_related_offers(order):
    """
    Search related offers to order from parameter
    :param order: client order
    :return: string with related offers to order from parameter or empty string
    """
    related_offers = ""
    if OrdersOffers.objects.filter(order=order).count() > 0:
        order_offers = OrdersOffers.objects.filter(order=order)
        for i in order_offers:
            related_offers += "{}, ".format(str(i.offer.pk))

    if related_offers != "":
        related_offers = related_offers[:-2]

    return related_offers


def get_is_active(language, order):
    """
    Checks if order is active or no and creates response in appropriate language
    :param language: language of conversation
    :param order: client order
    :return: string with info about if order is active or no
    """
    output_string = ""
    if language == 'pl':
        if order.is_active:
            output_string = "TAK"
        else:
            output_string = "Nie"
    elif language == 'en':
        if order.is_active:
            output_string = "YES"
        else:
            output_string = "NO"

    return output_string


def get_drivers(order):
    """
    Search drivers for order from parameter
    :param order: client order
    :return: string with drivers for order from parameter
    """
    output_string = ""
    if OrdersDrivers.objects.filter(order=order).count() > 0:
        orders_drivers = OrdersDrivers.objects.filter(order=order)
        for i in orders_drivers:
            output_string += "{} {}, tel. {}, ".format(i.driver.name, i.driver.surname, i.driver.phone_number)

    if output_string != "":
        output_string = output_string[:-2]

    return output_string


def get_trucks(order):
    """
    Search trucks for order from parameter
    :param order: client order
    :return: string with trucks for order from parameter
    """
    output_string = ""
    if OrdersVehicles.objects.filter(order=order).count() > 0:
        orders_vehicles = OrdersVehicles.objects.filter(order=order)
        for i in orders_vehicles:
            output_string += "{}, {}, {}, ".format(i.vehicle.brand, i.vehicle.type, i.vehicle.registration_number)

    if output_string != "":
        output_string = output_string[:-2]

    return output_string


def get_number_of_visited_places(order):
    """
    Counts number places to visit during executing order
    :param order: client order
    :return: string with number of places to visit during executing order
    """
    amount_loading_places = OrdersLoadingPlaces.objects.filter(order=order).count()
    amount_destination_places = OrdersDestinationPlaces.objects.filter(order=order).count()

    return amount_loading_places + amount_destination_places


def get_departure_places(order, language):
    """
    Creates appropriate string with departure places for order from parameter
    :param order: client order
    :param language: language of conversation
    :return: string with departure places for order from parameter
    """
    departure_places_string = ""
    departure_places = OrdersLoadingPlaces.objects.filter(order=order)
    counter = 1
    for i in departure_places:
        place = i.loading_place
        if language == 'pl':
            departure_places_string += "{}. {} godz. {}, {}, ulica: {}, {} {}, kraj: {}, liczba palet: {}, uwagi: {}\n".format(
                counter, str(place.date)[0:10], place.hour, place.place.place_name, place.place.street, place.place.post_code,
                place.place.post_place, place.place.country, place.palette_number.pallets_number, place.remarks)
        elif language == 'en':
            departure_places_string += "{}. {} hour: {}, {}, street: {}, {} {}, country: {}, number of pallets: {}, remarks: {}\n".format(
                counter, str(place.date)[0:10], place.hour, place.place.place_name, place.place.street, place.place.post_code,
                place.place.post_place, place.place.country, place.palette_number.pallets_number, place.remarks)
        counter += 1

    return departure_places_string


def get_destinations(order, language):
    """
    Creates appropriate string with destinations for order from parameter
    :param order: client order
    :param language: language of conversation
    :return: string with destinations for order from parameter
    """
    destinations_string = ""
    destinations = OrdersDestinationPlaces.objects.filter(order=order)
    counter = 1
    for i in destinations:
        place = i.destination_place
        if language == 'pl':
            destinations_string += "{}. {} godz. {}, {}, ulica: {}, {} {}, kraj: {}, liczba palet: {}, uwagi: {}\n".format(
                counter, str(place.date)[0:10], place.hour, place.place.place_name, place.place.street, place.place.post_code,
                place.place.post_place, place.place.country, place.palette_number.pallets_number, place.remarks)
        elif language == 'en':
            destinations_string += "{}. {} hour: {}, {}, street: {}, {} {}, country: {}, number of pallets: {}, remarks: {}\n".format(
                counter, str(place.date)[0:10], place.hour, place.place.place_name, place.place.street, place.place.post_code,
                place.place.post_place, place.place.country, place.palette_number.pallets_number, place.remarks)
        counter += 1

    return destinations_string


def get_loadings(order, language):
    """
    Creates string with info about loadings for order from parameter
    :param order: client order
    :return: String with info about loadings for order from parameter
    """
    orders_loadings = OrdersLoadingPlaces.objects.filter(order=order)
    loadings = list()
    for i in orders_loadings:
        loadings.append(i.loading_place)
    loadings.sort(key=lambda x: x.date, reverse=False)

    output_string = ""
    counter = 1
    for loading in loadings:
        if language == 'pl':
            output_string += "{} {}, {}, {} palet; ".format(counter, loading.place.post_place, str(loading.date)[0:10],
                                                            loading.palette_number.pallets_number)
        elif language == 'en':
            output_string += "{} {}, {}, {} pallets; ".format(counter, loading.place.post_place, str(loading.date)[0:10],
                                                            loading.palette_number.pallets_number)
        counter += 1

    output_string = output_string[:-2]
    return output_string


def get_unloadings(order, language):
    """
    Creates string with info about unloadings for order from parameter
    :param order: client order
    :return: String with info about unloadings for order from parameter
    """
    orders_unloadings = OrdersDestinationPlaces.objects.filter(order=order)
    unloadings = list()
    for i in orders_unloadings:
        unloadings.append(i.destination_place)
    unloadings.sort(key=lambda x: x.date, reverse=False)

    output_string = ""
    counter = 1
    for unloading in unloadings:
        if language == 'pl':
            output_string += "{} {}, {}, {} palet; ".format(counter, unloading.place.post_place, str(unloading.date)[0:10],
                                                            unloading.palette_number.pallets_number)
        elif language == 'en':
            output_string += "{} {}, {}, {} pallet; ".format(counter, unloading.place.post_place, str(unloading.date)[0:10],
                                                             unloading.palette_number.pallets_number)
        counter += 1

    output_string = output_string[:-2]
    return output_string


def browse_current_orders(request):
    """
    Searches active orders on user account and return it in JSON
    :param request: POST request from "Browse current orders" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with active user orders or Json with one user order, or info about no active user orders
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić twoich aktualnych zleceń, ponieważ nie posiadasz jeszcze konta. " \
                         "Jeśli chcesz założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić aktualnych zleceń. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't display your current orders, because you don't have an account yet. If you " \
                         "want to create a best transport Poland account, select the option \"Sign up\" below."
    display_spoken_en = "You can't display your current orders. Create an account by selecting the option below \"Sign up\""

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
            current_orders = list()
            if Order.objects.filter(customer=profile, is_active=True).count() > 0:
                current_orders = Order.objects.filter(customer=profile, is_active=True)
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']

            if len(current_orders) > 1:
                with open('api/offers_list.json') as json_file:
                    response = json.load(json_file)
                part_to_modify = response['payload']['google']['systemIntent']["data"]["listSelect"]

                counter = 0
                orders_to_insert = []
                if language == 'pl':
                    part_to_modify["title"] = "Twoje aktualne zlecenia"
                    for order in current_orders:
                        if counter < 30:
                            orders_to_insert.append({
                                "optionInfo": {
                                    "key": "Zlecenie numer {}".format(order.pk)
                                },
                                "description": "Załadunki: {} Rozładunki: {} cena: {}".format(
                                    get_loadings(order, language), get_unloadings(order, language), order.price),
                                "title": "Zlecenie numer {}".format(order.pk)
                            })
                            counter += 1
                        else:
                            break
                    speech_response = "Twoje aktualne zlecenia"
                    display_response = "Twoje aktualne zlecenia"
                    suggestions = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                   {"title": "Konto"}, {"title": "Inne"}]
                elif language == 'en':
                    part_to_modify["title"] = "Your current orders"
                    for order in current_orders:
                        if counter < 30:
                            orders_to_insert.append({
                                "optionInfo": {
                                    "key": "Order number {}".format(order.pk)
                                },
                                "description": "Loadings: {}; Unloadings: {}; price: {}".format(
                                    get_loadings(order, language), get_unloadings(order, language), order.price),
                                "title": "Order number {}".format(order.pk)
                            })
                            counter += 1
                        else:
                            break
                    speech_response = "Your current orders"
                    display_response = "Your current orders"
                    suggestions = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                   {"title": "Account"}, {"title": "Others"}]

                part_to_modify["items"] = orders_to_insert
                response['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
                part_to_modify = response['payload']['google']["richResponse"]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_response
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_response
                part_to_modify['suggestions'] = suggestions

                response['payload']['google']["richResponse"] = part_to_modify
                return response
            elif len(current_orders) == 1:
                number_of_visited_places = get_number_of_visited_places(current_orders[0])
                if language == "pl":
                    if number_of_visited_places <= 4:
                        basic_card_pl = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(current_orders[0].pk),
                                "formattedText": "___Data złożenia zlecenia:___  {}  \n__Wykonawca:__  {}  \n__Usługobiorca:__  {}"
                                                 "  \n__Miejsca odjazdów:__  \n{}  \n__Miejsca docelowe:__  \n{}"
                                                 "  \n__Powiązane oferty:__  {}  \n__Kierowcy:__  {}  \n__Samochody:__  {}"
                                                 "  \n__Możliwość edycji zlecenia:__  {}  \n"
                                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                                    .format(current_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(current_orders[0], language), get_destinations(current_orders[0], language),
                                            get_related_offers(current_orders[0]), get_drivers(current_orders[0]),
                                            get_trucks(current_orders[0]), get_is_active(language, current_orders[0]),
                                            current_orders[0].remarks, current_orders[0].price)
                            }
                        }
                    elif number_of_visited_places > 4:
                        basic_card_pl = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(current_orders[0].pk),
                                "formattedText": "___Data złożenia zlecenia:___  {}  \n__Wykonawca:__  {}  \n__Usługobiorca:__  {}"
                                                 "  \n__Miejsca odjazdów:__  \n{}  \n__Miejsca docelowe:__  \n{}"
                                                 "  \n__Powiązane oferty:__  {}  \n__Możliwość edycji zlecenia:__  {}  \n"
                                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                                    .format(current_orders[0], get_performer(language), get_order_client(profile),
                                            get_departure_places(current_orders[0], language), get_destinations(current_orders[0], language),
                                            get_related_offers(current_orders[0]),
                                            get_is_active(language, current_orders[0]),
                                            current_orders[0].remarks, current_orders[0].price)
                            }
                        }

                    speech_text_pl = "Masz jedno aktualne zlecenie"
                    display_text_pl = "Masz jedno aktualne zlecenie"
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['items'].append(basic_card_pl)
                    part_to_modify['suggestions'] = suggestions_pl

                elif language == "en":
                    if number_of_visited_places <= 4:
                        basic_card_en = {
                            "basicCard": {
                                "title": "Order no. {}".format(current_orders[0].pk),
                                "formattedText": "___Date of placing the order:___  {}  \n__Performer:__  {}  \n__Recipient:__  {}"
                                                 "  \n__Departure places:__  \n{}  \n__Destinations:__  \n{}"
                                                 "  \n__Related offers:__  {}  \n__Drivers:__  {}  \n__Trucks:__  {}"
                                                 "  \n__The order can be edited:__  {}  \n"
                                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                                    .format(current_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(current_orders[0], language), get_destinations(current_orders[0], language),
                                            get_related_offers(current_orders[0]), get_drivers(current_orders[0]),
                                            get_trucks(current_orders[0]), get_is_active(language, current_orders[0]),
                                            current_orders[0].remarks, current_orders[0].price)
                            }
                        }
                    elif number_of_visited_places > 4:
                        basic_card_en = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(current_orders[0].pk),
                                "formattedText": "___Date of placing the order:___  {}  \n__Performer:__  {}  \n__Recipient:__  {}"
                                                 "  \n__Departure places:__  \n{}  \n__Destinations:__  \n{}"
                                                 "  \n__Related offers:__  {}  \n__The order can be edited:__  {}  \n"
                                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                                    .format(current_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(current_orders[0], language), get_destinations(current_orders[0], language),
                                            get_related_offers(current_orders[0]),
                                            get_is_active(language, current_orders[0]),
                                            current_orders[0].remarks, current_orders[0].price)
                            }
                        }

                    speech_text_en = "You have one current order"
                    display_text_en = "You have one current order"
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiry"},
                                      {"title": "Account"}, {"title": "Others"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                    part_to_modify['items'].append(basic_card_en)
                    part_to_modify['suggestions'] = suggestions_en

                response['payload']['google']['richResponse'] = part_to_modify
                return response
            elif len(current_orders) == 0:
                if language == "pl":
                    speech_text_pl = "Nie masz żadnych aktualnych zamówień na swoim koncie"
                    display_text_pl = "Nie masz żadnych aktualnych zamówień na swoim koncie"
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['suggestions'] = suggestions_pl
                elif language == "en":
                    speech_text_en = "You don't have any current orders on your account"
                    display_text_en = "You don't have any current orders on your account"
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                      {"title": "Account"}, {"title": "Others"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
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


def orders_history(request):
    """
    Searches past orders on user account and return it in JSON
    :param request: POST request from "The history of orders" Dialogflow intent or from apropriate selected item in Dialogflow list
    :return: Json with past user orders or Json with one user orders, or info about no active user orders
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić twoich przeszłych zleceń, ponieważ nie posiadasz jeszcze konta. " \
                         "Jeśli chcesz założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić przeszłych zleceń. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't display your past orders, because you don't have an account yet. If you " \
                         "want to create a best transport Poland account, select the option \"Sign up\" below."
    display_spoken_en = "You can't display your past orders. Create an account by selecting the option below \"Sign up\""

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
            current_orders = list()
            if Order.objects.filter(customer=profile, is_active=False).count() > 0:
                current_orders = Order.objects.filter(customer=profile, is_active=False)
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']

            if len(current_orders) > 1:
                with open('api/offers_list.json') as json_file:
                    response = json.load(json_file)
                part_to_modify = response['payload']['google']['systemIntent']["data"]["listSelect"]

                counter = 0
                orders_to_insert = []
                if language == 'pl':
                    part_to_modify["title"] = "Twoje zlecenia z historii zamówień"
                    for order in current_orders:
                        if counter < 30:
                            orders_to_insert.append({
                                "optionInfo": {
                                    "key": "Zlecenie numer {}".format(order.pk)
                                },
                                "description": "Załadunki: {} Rozładunki: {} cena: {}".format(
                                    get_loadings(order, language), get_unloadings(order, language), order.price),
                                "title": "Zlecenie numer {}".format(order.pk)
                            })
                            counter += 1
                        else:
                            break
                    speech_response = "Twoje zlecenia z historii zamówień"
                    display_response = "Twoje zlecenia z historii zamówień"
                    suggestions = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                   {"title": "Konto"}, {"title": "Inne"}]
                elif language == 'en':
                    part_to_modify["title"] = "Your orders from the order history"
                    for order in current_orders:
                        if counter < 30:
                            orders_to_insert.append({
                                "optionInfo": {
                                    "key": "Order number {}".format(order.pk)
                                },
                                "description": "Loadings: {}; Unloadings: {}; price: {}".format(
                                    get_loadings(order, language), get_unloadings(order, language), order.price),
                                "title": "Order number {}".format(order.pk)
                            })
                            counter += 1
                        else:
                            break
                    speech_response = "Your orders from the order history"
                    display_response = "Your orders from the order history"
                    suggestions = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                   {"title": "Account"}, {"title": "Others"}]

                part_to_modify["items"] = orders_to_insert
                response['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
                part_to_modify = response['payload']['google']["richResponse"]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_response
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_response
                part_to_modify['suggestions'] = suggestions

                response['payload']['google']["richResponse"] = part_to_modify
                return response
            elif len(current_orders) == 1:
                number_of_visited_places = get_number_of_visited_places(current_orders[0])
                if language == "pl":
                    if number_of_visited_places <= 4:
                        basic_card_pl = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(current_orders[0].pk),
                                "formattedText": "___Data złożenia zlecenia:___  {}  \n__Wykonawca:__  {}  \n__Usługobiorca:__  {}"
                                                 "  \n__Miejsca odjazdów:__  \n{}  \n__Miejsca docelowe:__  \n{}"
                                                 "  \n__Powiązane oferty:__  {}  \n__Kierowcy:__  {}  \n__Samochody:__  {}"
                                                 "  \n__Możliwość edycji zlecenia:__  {}  \n"
                                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                                    .format(current_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(current_orders[0], language),
                                            get_destinations(current_orders[0], language),
                                            get_related_offers(current_orders[0]), get_drivers(current_orders[0]),
                                            get_trucks(current_orders[0]), get_is_active(language, current_orders[0]),
                                            current_orders[0].remarks, current_orders[0].price)
                            }
                        }
                    elif number_of_visited_places > 4:
                        basic_card_pl = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(current_orders[0].pk),
                                "formattedText": "___Data złożenia zlecenia:___  {}  \n__Wykonawca:__  {}  \n__Usługobiorca:__  {}"
                                                 "  \n__Miejsca odjazdów:__  \n{}  \n__Miejsca docelowe:__  \n{}"
                                                 "  \n__Powiązane oferty:__  {}  \n__Możliwość edycji zlecenia:__  {}  \n"
                                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                                    .format(current_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(current_orders[0], language),
                                            get_destinations(current_orders[0], language),
                                            get_related_offers(current_orders[0]),
                                            get_is_active(language, current_orders[0]),
                                            current_orders[0].remarks, current_orders[0].price)
                            }
                        }

                    speech_text_pl = "Masz jedno zlecenie w historii zamówień"
                    display_text_pl = "Masz jedno zlecenie w historii zamówień"
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['items'].append(basic_card_pl)
                    part_to_modify['suggestions'] = suggestions_pl

                elif language == "en":
                    if number_of_visited_places <= 4:
                        basic_card_en = {
                            "basicCard": {
                                "title": "Order no. {}".format(current_orders[0].pk),
                                "formattedText": "___Date of placing the order:___  {}  \n__Performer:__  {}  \n__Recipient:__  {}"
                                                 "  \n__Departure places:__  \n{}  \n__Destinations:__  \n{}"
                                                 "  \n__Related offers:__  {}  \n__Drivers:__  {}  \n__Trucks:__  {}"
                                                 "  \n__The order can be edited:__  {}  \n"
                                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                                    .format(current_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(current_orders[0], language),
                                            get_destinations(current_orders[0], language),
                                            get_related_offers(current_orders[0]), get_drivers(current_orders[0]),
                                            get_trucks(current_orders[0]), get_is_active(language, current_orders[0]),
                                            current_orders[0].remarks, current_orders[0].price)
                            }
                        }
                    elif number_of_visited_places > 4:
                        basic_card_en = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(current_orders[0].pk),
                                "formattedText": "___Date of placing the order:___  {}  \n__Performer:__  {}  \n__Recipient:__  {}"
                                                 "  \n__Departure places:__  \n{}  \n__Destinations:__  \n{}"
                                                 "  \n__Related offers:__  {}  \n__The order can be edited:__  {}  \n"
                                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                                    .format(current_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(current_orders[0], language),
                                            get_destinations(current_orders[0], language),
                                            get_related_offers(current_orders[0]),
                                            get_is_active(language, current_orders[0]),
                                            current_orders[0].remarks, current_orders[0].price)
                            }
                        }

                    speech_text_en = "You have one order in the order history"
                    display_text_en = "You have one order in the order history"
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiry"},
                                      {"title": "Account"}, {"title": "Others"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                    part_to_modify['items'].append(basic_card_en)
                    part_to_modify['suggestions'] = suggestions_en

                response['payload']['google']['richResponse'] = part_to_modify
                return response
            elif len(current_orders) == 0:
                if language == "pl":
                    speech_text_pl = "Nie masz żadnych zleceń w historii zamówień"
                    display_text_pl = "Nie masz żadnych zleceń w historii zamówień"
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['suggestions'] = suggestions_pl
                elif language == "en":
                    speech_text_en = "You don't have any orders in the order history"
                    display_text_en = "You don't have any orders in the order history"
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                      {"title": "Account"}, {"title": "Others"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
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


def order_number(request):
    """
    Search details for order from request parameter. Create JSON with these details.
    :param request: POST request from "Order number" Dialogflow intent or from appropriate selected item in Dialogflow list
    :return: JSON with details of order
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyświetlić zlecenia, ponieważ nie posiadasz jeszcze konta. Jeśli chcesz założyć " \
                         "konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyświetlić zlecenia. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't display an order, because you don't have an account yet. If you " \
                         "want to create a best transport Poland account, select the option \"Sign up\" below."
    display_spoken_en = "You can't display an order. Create an account by selecting the option below \"Sign up\""

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
            title = request.data['originalDetectIntentRequest']['payload']['inputs'][0]['arguments'][0]['textValue']
            order_number = title.split()
            order_number = int(order_number[2])
            orders_amount = Order.objects.filter(pk=order_number).count()
            if orders_amount == 1:
                searched_order = Order.objects.get(pk=order_number)

            if orders_amount == 1 and profile.pk == searched_order.customer.pk:
                number_of_visited_places = get_number_of_visited_places(searched_order)
                if language == "pl":
                    if number_of_visited_places <= 4:
                        basic_card_pl = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(searched_order.pk),
                                "formattedText": "___Data złożenia zlecenia:___  {}  \n__Wykonawca:__  {}  \n__Usługobiorca:__  {}"
                                                 "  \n__Miejsca odjazdów:__  \n{}  \n__Miejsca docelowe:__  \n{}"
                                                 "  \n__Powiązane oferty:__  {}  \n__Kierowcy:__  {}  \n__Samochody:__  {}"
                                                 "  \n__Możliwość edycji zlecenia:__  {}  \n"
                                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                                    .format(searched_order.date, get_performer(language), get_order_client(profile),
                                            get_departure_places(searched_order, language),
                                            get_destinations(searched_order, language),
                                            get_related_offers(searched_order), get_drivers(searched_order),
                                            get_trucks(searched_order), get_is_active(language, searched_order),
                                            searched_order.remarks, searched_order.price)
                            }
                        }
                    elif number_of_visited_places > 4:
                        basic_card_pl = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(searched_order.pk),
                                "formattedText": "___Data złożenia zlecenia:___  {}  \n__Wykonawca:__  {}  \n__Usługobiorca:__  {}"
                                                 "  \n__Miejsca odjazdów:__  \n{}  \n__Miejsca docelowe:__  \n{}"
                                                 "  \n__Powiązane oferty:__  {}  \n__Możliwość edycji zlecenia:__  {}  \n"
                                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                                    .format(searched_order.date, get_performer(language), get_order_client(profile),
                                            get_departure_places(searched_order, language),
                                            get_destinations(searched_order, language),
                                            get_related_offers(searched_order),
                                            get_is_active(language, searched_order),
                                            searched_order.remarks, searched_order.price)
                            }
                        }

                    speech_text_pl = "Szczegóły wybranego zlecenia"
                    display_text_pl = "Szczegóły zlecenia"
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['items'].append(basic_card_pl)
                    part_to_modify['suggestions'] = suggestions_pl

                elif language == "en":
                    if number_of_visited_places <= 4:
                        basic_card_en = {
                            "basicCard": {
                                "title": "Order no. {}".format(searched_order.pk),
                                "formattedText": "___Date of placing the order:___  {}  \n__Performer:__  {}  \n__Recipient:__  {}"
                                                 "  \n__Departure places:__  \n{}  \n__Destinations:__  \n{}"
                                                 "  \n__Related offers:__  {}  \n__Drivers:__  {}  \n__Trucks:__  {}"
                                                 "  \n__The order can be edited:__  {}  \n"
                                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                                    .format(searched_order.date, get_performer(language), get_order_client(profile),
                                            get_departure_places(searched_order, language),
                                            get_destinations(searched_order, language),
                                            get_related_offers(searched_order), get_drivers(searched_order),
                                            get_trucks(searched_order), get_is_active(language, searched_order),
                                            searched_order.remarks, searched_order.price)
                            }
                        }
                    elif number_of_visited_places > 4:
                        basic_card_en = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(searched_order.pk),
                                "formattedText": "___Date of placing the order:___  {}  \n__Performer:__  {}  \n__Recipient:__  {}"
                                                 "  \n__Departure places:__  \n{}  \n__Destinations:__  \n{}"
                                                 "  \n__Related offers:__  {}  \n__The order can be edited:__  {}  \n"
                                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                                    .format(searched_order.date, get_performer(language), get_order_client(profile),
                                            get_departure_places(searched_order, language),
                                            get_destinations(searched_order, language),
                                            get_related_offers(searched_order),
                                            get_is_active(language, searched_order),
                                            searched_order.remarks, searched_order.price)
                            }
                        }

                    speech_text_en = "Details of selected order"
                    display_text_en = "Order details"
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiry"},
                                      {"title": "Account"}, {"title": "Others"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                    part_to_modify['items'].append(basic_card_en)
                    part_to_modify['suggestions'] = suggestions_en

                response['payload']['google']['richResponse'] = part_to_modify
                return response
            else:
                if language == "pl":
                    speech_text_pl = "Nie masz takiego zlecenia na swoim koncie"
                    display_text_pl = "Nie masz takiego zlecenia"
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['suggestions'] = suggestions_pl
                elif language == "en":
                    speech_text_en = "You don't have this order on your account"
                    display_text_en = "You don't have this order"
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                      {"title": "Account"}, {"title": "Others"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
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


def ask_search_orders(request):
    """
    Creates response with prompting user to give data to search order/orders
    :param request: request from "Ask creating inquiry for" Dialogflow intent or from appropriate selected item in Dialogflow list
    :return: string with prompting user to give data to search order/orders
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if access_token:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Aby wyszukać zlecenie podaj przynajmniej" \
                                                                                           " jedno miejsce załadunku i jedno miejsce " \
                                                                                           "rozładunku, ciężarówki lub samo id zlecenia." \
                                                                                           " Na przykład:"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Miejsca załadunku: Warszawa 15 listopada," \
                                                                                          " godzina 8:00, 7 palet. Dortmund 17 listopada" \
                                                                                          " godzina 9:00, 10 palet. Miejsca rozładunku: " \
                                                                                          "Bratysława 16 listopada godzina 11:00, 7 palet," \
                                                                                          " Sosnowiec 18 listopada, godzina 10:00, 10 palet." \
                                                                                          " 2 mercedesy, 6000 złotych"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                             {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "To search for an order, please provide" \
                                                                                           " at least one loading location and one " \
                                                                                           "unloading place, trucks or the order ID." \
                                                                                           " For example:"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Loading locations: Warsaw, November 15, 8:00, " \
                                                                                          "7 pallets. Dortmund November 17 at 9:00, 10 pallets." \
                                                                                          " Unloading places: Bratislava November 16 at 11:00, " \
                                                                                          "7 pallets, Sosnowiec November 18, 10:00. 10 pallets. " \
                                                                                          "2 Mercedes, 6000 PLN"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                             {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google'] = part_to_modify
        session_id = request.data["queryResult"]["outputContexts"][0]["name"]
        session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
        session_id = session_id.lstrip("sessions/").rstrip("/contexts")
        context = {
            "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/search_order".format(
                session_id),
            "lifespanCount": 5
        }
        list_with_context = list()
        list_with_context.append(context)
        response["outputContexts"] = list_with_context
        return response
    else:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "Musisz być zalogowany aby wyszukać" \
                                                                                           " zlecenie"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "Musisz być zalogowany aby wyszukać" \
                                                                                           " zlecenie"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                             {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "You must be logged in to search for" \
                                                                                           " the order"
            part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "You must be logged in to search for" \
                                                                                          " the order"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                             {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google'] = part_to_modify
        return response


def get_orders_loadings_geo_city(client_orders, value):
    """
    Searches OrdersLoadingPlaces objects linked with client orders and that contain value
    :param client_orders: orders of profile
    :param: value: value of geo-city for which OrdersLoadingPlaces objects are searching
    :return: List with OrdersLoadingPlaces objects or empty list
    """
    orders_loadings = list()

    for client_order in client_orders:
        orders_loading_temp = OrdersLoadingPlaces.objects.filter(order=client_order)
        for order_loading in orders_loading_temp:
            if order_loading.loading_place.place and order_loading.loading_place.place.post_place == value:
                orders_loadings.append(order_loading)

    return orders_loadings


def get_orders(orders_items):
    """
    Search orders that are linked with other objects from parameter
    :param orders_items: OrdersLoadingPlaces or OrdersDestinationPlaces or OrdersVehicles objects
    :return: found orders
    """
    orders = list()
    for order_item in orders_items:
        orders.append(order_item.order.pk)

    return orders


def get_orders_destinations_geo_city(client_orders, value):
    """
    Searches OrdersDestinationPlaces objects linked with client orders and that contain value
    :param client_orders: orders of profile
    :param: value: value of geo-city for which OrdersDestinationPlaces objects are searching
    :return: List with OrdersDestinationPlaces objects or empty list
    """
    orders_destinations = list()

    for client_order in client_orders:
        orders_destinations_temp = OrdersDestinationPlaces.objects.filter(order=client_order)
        for order_destination in orders_destinations_temp:
            if order_destination.destination_place.place and order_destination.destination_place.place.post_place == value:
                orders_destinations.append(order_destination)

    return orders_destinations


def get_orders_loadings_date(client_orders, value):
    """
    Searches OrdersLoadingPlaces objects linked with client orders and that contain value
    :param client_orders: orders of profile
    :param value: value of date for which OrdersLoadingPlaces objects are searching
    :return: List with OrdersLoadingPlaces objects or empty list
    """
    orders_loadings = list()
    date = value[:10]

    for client_order in client_orders:
        orders_loading_temp = OrdersLoadingPlaces.objects.filter(order=client_order)
        for order_loading in orders_loading_temp:
            if str(order_loading.loading_place.date)[0:10] == date:
                orders_loadings.append(order_loading)

    return orders_loadings


def get_orders_destinations_date(client_orders, value):
    """
    Searches OrdersDestinationPlaces objects linked with client orders and that contain value
    :param client_orders: orders of profile
    :param: value: value of date for which OrdersDestinationPlaces objects are searching
    :return: List with OrdersDestinationPlaces objects or empty list
    """
    orders_destinations = list()
    date = value[:10]

    for client_order in client_orders:
        orders_destinations_temp = OrdersDestinationPlaces.objects.filter(order=client_order)
        for order_destination in orders_destinations_temp:
            if str(order_destination.destination_place.date)[0:10] == date:
                orders_destinations.append(order_destination)

    return orders_destinations


def get_orders_loadings_time(client_orders, value):
    """
    Searches OrdersLoadingPlaces objects linked with client orders and that contain value
    :param client_orders: orders of profile
    :param value: value of time for which OrdersLoadingPlaces objects are searching
    :return: List with OrdersLoadingPlaces objects or empty list
    """
    orders_loadings = list()
    time = value[11:19]

    for client_order in client_orders:
        orders_loading_temp = OrdersLoadingPlaces.objects.filter(order=client_order)
        for order_loading in orders_loading_temp:
            if str(order_loading.loading_place.hour) == time:
                orders_loadings.append(order_loading)

    return orders_loadings


def get_orders_destinations_time(client_orders, value):
    """
    Searches OrdersDestinationPlaces objects linked with client orders and that contain value
    :param client_orders: orders of profile
    :param: value: value of time for which OrdersDestinationPlaces objects are searching
    :return: List with OrdersDestinationPlaces objects or empty list
    """
    orders_destinations = list()
    time = value[11:19]

    for client_order in client_orders:
        orders_destinations_temp = OrdersDestinationPlaces.objects.filter(order=client_order)
        for order_destination in orders_destinations_temp:
            if str(order_destination.destination_place.hour) == time:
                orders_destinations.append(order_destination)

    return orders_destinations


def get_orders_loadings_palette_number(client_orders, value):
    """
    Searches OrdersLoadingPlaces objects linked with client orders and that contain value
    :param client_orders: orders of profile
    :param value: value of palettes number for which OrdersLoadingPlaces objects are searching
    :return: List with OrdersLoadingPlaces objects or empty list
    """
    orders_loadings = list()

    for client_order in client_orders:
        orders_loading_temp = OrdersLoadingPlaces.objects.filter(order=client_order)
        for order_loading in orders_loading_temp:
            if order_loading.loading_place.palette_number and order_loading.loading_place.palette_number.pallets_number == value:
                orders_loadings.append(order_loading)

    return orders_loadings


def get_orders_destinations_palette_number(client_orders, value):
    """
    Searches OrdersDestinationPlaces objects linked with client orders and that contain value
    :param client_orders: orders of profile
    :param: value: value of number of palettes for which OrdersDestinationPlaces objects are searching
    :return: List with OrdersDestinationPlaces objects or empty list
    """
    orders_destinations = list()

    for client_order in client_orders:
        orders_destinations_temp = OrdersDestinationPlaces.objects.filter(order=client_order)
        for order_destination in orders_destinations_temp:
            if order_destination.destination_place.palette_number and order_destination.destination_place.palette_number.\
                    pallets_number == value:
                orders_destinations.append(order_destination)

    return orders_destinations


def get_orders_vehicles(client_orders, value):
    """
    Searches OrdersVehicles objects linked with client orders and that contain value
    :param client_orders: orders of profile
    :param: value: brands of trucks for which OrdersVehicles objects are searching
    :return: list with OrdersVehicles objects or empty list
    """
    orders_vehicles = list()

    for client_order in client_orders:
        orders_vehicles_temp = OrdersVehicles.objects.filter(order=client_order)
        for order_vehicle in orders_vehicles_temp:
            if value in order_vehicle.vehicle.brand:
                orders_vehicles.append(order_vehicle)

    return orders_vehicles


def get_orders_for_unit_currency(client_orders, value):
    """
    Search orders which price is lower than value + 300
    :param client_orders: orders of profile
    :param value: value from sending request to best transport service
    :return: found orders
    """
    amount = value["amount"]
    orders = list()

    for client_order in client_orders:
        if int(client_order.price) < amount + 300:
            orders.append(client_order.pk)

    return orders


def get_client_orders(orders_numbers):
    """
    Search Orders objects for orders numbers
    :param orders_number: list with orders numbers
    :return: list with Orders objects
    """
    orders = list()

    for order in orders_numbers:
        orders.append(Order.objects.get(pk=order))

    return orders


def find_key_position_in_text(queryText, key, parameters):
    """
    Search value position of key inside text entered by the user
    :param queryText: Text which user enter
    :param key: key from request parameters
    :param parameters: parameters of request
    :return: value position of key in queryText
    """
    if "unit-currency" in key:
        position = queryText.lower().find(str(parameters[key]["amount"]))
    elif "date" in key:
        value = parameters[key]
        value = value[8:10]
        if value[0] == '0':
            value = value[1]
        position = queryText.lower().find(value)
    elif "time" in key:
        value = parameters[key]
        value = value[11:16]
        if value[0] == '0':
            value = value[1:]
        position = queryText.lower().find(value)
    elif "number" in key:
        position = queryText.lower().find(str(parameters[key]) + " pal")
    else:
        position = queryText.lower().find(str(parameters[key]))

    return position


def find_orders(request, profile):
    """
    Search orders objects for parameters form request and for profile
    :param request: request from "Search order" Dialogflow intent
    :param profile: profile of user
    :return: list with orders objects or empty list
    """
    queryText = request.data["queryResult"]["queryText"]
    parameters  = request.data["queryResult"]["parameters"]
    parameters_list = list(parameters)
    language = request.data['queryResult']['languageCode']

    keys = list()
    parameters_names = ["geo-city", "date", "time", "number", "unit-currency", "trucks"]
    for name in parameters_names:
        for parameter in parameters_list:
            if name in parameter and parameters[parameter] != "":
                keys.append(parameter)

    if len(keys) == 1 and keys[0] == "number":
        order = Order.objects.get(pk=parameters["number"])
        orders = list()
        orders.append(order)
        return orders
        # with open('api/response.json') as json_file:
        #     response = json.load(json_file)
        #
        # part_to_modify = response['payload']['google']
        # part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "number"
        # part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "{}".format(orders)
        # part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
        #                                                          {"title": "Zapytania"},
        #                                                          {"title": "Konto"}, {"title": "Inne"}]
        # response['payload']['google'] = part_to_modify
        # return response

    keys_grouped = list()
    for name in parameters_names:
        keys_to_insert = list()
        for key in keys:
            if name in key:
                keys_to_insert.append(key)
        if len(keys_to_insert) > 0:
            keys_grouped.append(keys_to_insert)

    loading_locations_string_pl = "załadun"
    loading_locations_string_en = "loading"
    unloading_locations_string_pl = "rozładun"
    unloading_locations_string_en = "unloading"

    first_string_position = ""
    first_string = ""
    second_string_position = ""
    second_string = ""
    if language == 'pl':
        loading_string_position = queryText.lower().find(loading_locations_string_pl)
        unloading_string_position = queryText.lower().find(unloading_locations_string_pl)
        if loading_string_position < unloading_string_position:
            first_string_position = loading_string_position
            first_string = loading_locations_string_pl
            second_string_position = unloading_string_position
            second_string = unloading_locations_string_pl
        elif unloading_string_position < loading_string_position:
            first_string_position = unloading_string_position
            first_string = unloading_locations_string_pl
            second_string_position = loading_string_position
            second_string = loading_locations_string_pl
    elif language == 'en':
        loading_string_position = queryText.lower().find(loading_locations_string_en)
        unloading_string_position = queryText.lower().find(unloading_locations_string_en)
        if loading_string_position < unloading_string_position:
            first_string_position = loading_string_position
            first_string = loading_locations_string_en
            second_string_position = unloading_string_position
            second_string = unloading_locations_string_en
        elif unloading_string_position < loading_string_position:
            first_string_position = unloading_string_position
            first_string = unloading_locations_string_en
            second_string_position = loading_string_position
            second_string = loading_locations_string_en

    if Order.objects.filter(customer=profile.pk).count() > 0:
        client_orders = Order.objects.filter(customer=profile.pk)
    else:
        return list()

    orders_contain_request_parameters = list()
    counter = 0
    for keys in keys_grouped:
        if counter > 0:
            client_orders = get_client_orders(orders_contain_request_parameters)
            if len(client_orders) == 0:
                return client_orders
            orders_contain_request_parameters = list()
        for key in keys:
            key_position_in_text = find_key_position_in_text(queryText, key, parameters)
            if "geo-city" in key and key_position_in_text < first_string_position:
                if language == 'pl':
                    if first_string == 'załadun':
                        orders_loadings = get_orders_loadings_geo_city(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif first_string == 'rozładun':
                        orders_destinations = get_orders_destinations_geo_city(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                elif language == 'en':
                    if first_string == 'loading':
                        orders_loadings = get_orders_loadings_geo_city(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif first_string == 'unloading':
                        orders_destinations = get_orders_destinations_geo_city(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
            elif "geo-city" in key and key_position_in_text > first_string_position and key_position_in_text < second_string_position:
                if len(queryText) > second_string_position + 11:
                    if language =='pl':
                        if first_string == 'załadun':
                            orders_loadings = get_orders_loadings_geo_city(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif first_string == "rozładun":
                            orders_destinations = get_orders_destinations_geo_city(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                    elif language == 'en':
                        if first_string == 'loading':
                            orders_loadings = get_orders_loadings_geo_city(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif first_string == 'unloading':
                            orders_destinations = get_orders_destinations_geo_city(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                else:
                    if language =='pl':
                        if second_string == 'załadun':
                            orders_loadings = get_orders_loadings_geo_city(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif second_string == "rozładun":
                            orders_destinations = get_orders_destinations_geo_city(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                    elif language == 'en':
                        if second_string == 'loading':
                            orders_loadings = get_orders_loadings_geo_city(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif second_string == 'unloading':
                            orders_destinations = get_orders_destinations_geo_city(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
            elif "geo-city" in key and key_position_in_text > second_string_position:
                if language == 'pl':
                    if second_string == 'załadun':
                        orders_loadings = get_orders_loadings_geo_city(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif second_string == 'rozładun':
                        orders_destinations = get_orders_destinations_geo_city(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                elif language == 'en':
                    if second_string == 'loading':
                        orders_loadings = get_orders_loadings_geo_city(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif second_string == 'unloading':
                        orders_destinations = get_orders_destinations_geo_city(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
            elif "date" in key and key_position_in_text < first_string_position:
                if language =='pl':
                    if first_string == 'załadun':
                        orders_loadings = get_orders_loadings_date(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif first_string == 'rozładun':
                        orders_destinations = get_orders_destinations_date(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                elif language == 'en':
                    if first_string == 'loading':
                        orders_loadings = get_orders_loadings_date(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif first_string == 'unloading':
                        orders_destinations = get_orders_destinations_date(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
            elif "date" in key and key_position_in_text > first_string_position and key_position_in_text < second_string_position:
                if len(queryText) > second_string_position + 11:
                    if language == 'pl':
                        if first_string == 'załadun':
                            orders_loadings = get_orders_loadings_date(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif first_string == "rozładun":
                            orders_destinations = get_orders_destinations_date(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                    elif language == 'en':
                        if first_string == 'loading':
                            orders_loadings = get_orders_loadings_date(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif first_string == 'unloading':
                            orders_destinations = get_orders_destinations_date(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                else:
                    if language == 'pl':
                        if second_string == 'załadun':
                            orders_loadings = get_orders_loadings_date(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif second_string == "rozładun":
                            orders_destinations = get_orders_destinations_date(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                    elif language == 'en':
                        if second_string == 'loading':
                            orders_loadings = get_orders_loadings_date(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif second_string == 'unloading':
                            orders_destinations = get_orders_destinations_date(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
            elif "date" in key and key_position_in_text > second_string_position:
                if language == 'pl':
                    if second_string == 'załadun':
                        orders_loadings = get_orders_loadings_date(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif second_string == 'rozładun':
                        orders_destinations = get_orders_destinations_date(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                elif language == 'en':
                    if second_string == 'loading':
                        orders_loadings = get_orders_loadings_date(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif second_string == 'unloading':
                        orders_destinations = get_orders_destinations_date(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
            elif "time" in key and key_position_in_text < first_string_position:
                if language =='pl':
                    if first_string == 'załadun':
                        orders_loadings = get_orders_loadings_time(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif first_string == 'rozładun':
                        orders_destinations = get_orders_destinations_time(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                elif language == 'en':
                    if first_string == 'loading':
                        orders_loadings = get_orders_loadings_time(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif first_string == 'unloading':
                        orders_destinations = get_orders_destinations_time(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
            elif "time" in key and key_position_in_text > first_string_position and key_position_in_text < second_string_position:
                if len(queryText) > second_string_position + 11:
                    if language == 'pl':
                        if first_string == 'załadun':
                            orders_loadings = get_orders_loadings_time(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif first_string == "rozładun":
                            orders_destinations = get_orders_destinations_time(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                    elif language == 'en':
                        if first_string == 'loading':
                            orders_loadings = get_orders_loadings_time(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif first_string == 'unloading':
                            orders_destinations = get_orders_destinations_time(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                else:
                    if language == 'pl':
                        if second_string == 'załadun':
                            orders_loadings = get_orders_loadings_time(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif second_string == "rozładun":
                            orders_destinations = get_orders_destinations_time(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                    elif language == 'en':
                        if second_string == 'loading':
                            orders_loadings = get_orders_loadings_time(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif second_string == 'unloading':
                            orders_destinations = get_orders_destinations_time(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
            elif "time" in key and key_position_in_text > second_string_position:
                if language == 'pl':
                    if second_string == 'załadun':
                        orders_loadings = get_orders_loadings_time(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif second_string == 'rozładun':
                        orders_destinations = get_orders_destinations_time(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                elif language == 'en':
                    if second_string == 'loading':
                        orders_loadings = get_orders_loadings_time(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif second_string == 'unloading':
                        orders_destinations = get_orders_destinations_time(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
            elif "number" in key and key_position_in_text < first_string_position:
                if language =='pl':
                    if first_string == 'załadun':
                        orders_loadings = get_orders_loadings_palette_number(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif first_string == 'rozładun':
                        orders_destinations = get_orders_destinations_palette_number(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                elif language == 'en':
                    if first_string == 'loading':
                        orders_loadings = get_orders_loadings_palette_number(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif first_string == 'unloading':
                        orders_destinations = get_orders_destinations_palette_number(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
            elif "number" in key and key_position_in_text > first_string_position and key_position_in_text < second_string_position:
                if len(queryText) > second_string_position + 11:
                    if language == 'pl':
                        if first_string == 'załadun':
                            orders_loadings = get_orders_loadings_palette_number(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif first_string == "rozładun":
                            orders_destinations = get_orders_destinations_palette_number(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                    elif language == 'en':
                        if first_string == 'loading':
                            orders_loadings = get_orders_loadings_palette_number(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif first_string == 'unloading':
                            orders_destinations = get_orders_destinations_palette_number(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                else:
                    if language == 'pl':
                        if second_string == 'załadun':
                            orders_loadings = get_orders_loadings_palette_number(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif second_string == "rozładun":
                            orders_destinations = get_orders_destinations_palette_number(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                    elif language == 'en':
                        if second_string == 'loading':
                            orders_loadings = get_orders_loadings_palette_number(client_orders, parameters[key])
                            orders = get_orders(orders_loadings)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
                        elif second_string == 'unloading':
                            orders_destinations = get_orders_destinations_palette_number(client_orders, parameters[key])
                            orders = get_orders(orders_destinations)
                            if orders:
                                for order in orders:
                                    if order not in orders_contain_request_parameters:
                                        orders_contain_request_parameters.append(order)
            elif "number" in key and key_position_in_text > second_string_position:
                if language == 'pl':
                    if second_string == 'załadun':
                        orders_loadings = get_orders_loadings_palette_number(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif second_string == 'rozładun':
                        orders_destinations = get_orders_destinations_palette_number(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                elif language == 'en':
                    if second_string == 'loading':
                        orders_loadings = get_orders_loadings_palette_number(client_orders, parameters[key])
                        orders = get_orders(orders_loadings)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
                    elif second_string == 'unloading':
                        orders_destinations = get_orders_destinations_palette_number(client_orders, parameters[key])
                        orders = get_orders(orders_destinations)
                        if orders:
                            for order in orders:
                                if order not in orders_contain_request_parameters:
                                    orders_contain_request_parameters.append(order)
            elif "trucks" in key:
                orders_trucks = get_orders_vehicles(client_orders, parameters[key])
                orders = get_orders(orders_trucks)
                if orders:
                    for order in orders:
                        if order not in orders_contain_request_parameters:
                            orders_contain_request_parameters.append(order)
            elif "unit-currency" in key:
                orders = get_orders_for_unit_currency(client_orders, parameters[key])
                if orders:
                    for order in orders:
                        if order not in orders_contain_request_parameters:
                            orders_contain_request_parameters.append(order)

        # print("dupa{} {}".format(counter, len(orders_contain_request_parameters)))
        counter += 1
    return client_orders


    # with open('api/response.json') as json_file:
    #     response = json.load(json_file)
    #
    # part_to_modify = response['payload']['google']
    #
    # if request.data['queryResult']['languageCode'] == 'pl':
    #     part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "dupa"
    #     part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = "{}".format(keys_grouped)
    #     part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
    #                                                          {"title": "Zapytania"},
    #                                                          {"title": "Konto"}, {"title": "Inne"}]
    # elif request.data['queryResult']['languageCode'] == 'en':
    #     part_to_modify['richResponse']['items'][0]['simpleResponse']['textToSpeech'] = "to search"
    #     part_to_modify['richResponse']['items'][0]['simpleResponse']['displayText'] = " no"
    #     part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
    #                                                          {"title": "Inquiries"},
    #                                                          {"title": "Account"}, {"title": "Others"}]
    #
    # response['payload']['google'] = part_to_modify
    # return response


def search_orders(request):
    """
    Searches orders and display them
    :param request: request from "Search orders" Dialogflow intent
    :return: String with data of orders to display
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz wyszukiwać zleceń, ponieważ nie posiadasz jeszcze konta. " \
                         "Jeśli chcesz założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz wyszukiwać zleceń. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't search for orders, because you don't have an account yet. If you " \
                         "want to create a best transport Poland account, select the option \"Sign up\" below."
    display_spoken_en = "You can't search for orders. Create an account by selecting the option below \"Sign up\""

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
            found_orders = find_orders(request, profile)
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']

            if len(found_orders) > 1:
                with open('api/offers_list.json') as json_file:
                    response = json.load(json_file)
                part_to_modify = response['payload']['google']['systemIntent']["data"]["listSelect"]

                counter = 0
                orders_to_insert = []
                if language == 'pl':
                    part_to_modify["title"] = "Wyszukane zlecenia"
                    for order in found_orders:
                        if counter < 30:
                            orders_to_insert.append({
                                "optionInfo": {
                                    "key": "Zlecenie numer {}".format(order.pk)
                                },
                                "description": "Załadunki: {} Rozładunki: {} cena: {}".format(
                                    get_loadings(order, language), get_unloadings(order, language), order.price),
                                "title": "Zlecenie numer {}".format(order.pk)
                            })
                            counter += 1
                        else:
                            break
                    speech_response = "Szukane zlecenia"
                    display_response = "Szukane zlecenia"
                    suggestions = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                   {"title": "Konto"}, {"title": "Inne"}]
                elif language == 'en':
                    part_to_modify["title"] = "Searched orders"
                    for order in found_orders:
                        if counter < 30:
                            orders_to_insert.append({
                                "optionInfo": {
                                    "key": "Order number {}".format(order.pk)
                                },
                                "description": "Loadings: {}; Unloadings: {}; price: {}".format(
                                    get_loadings(order, language), get_unloadings(order, language), order.price),
                                "title": "Order number {}".format(order.pk)
                            })
                            counter += 1
                        else:
                            break
                    speech_response = "Your searched orders"
                    display_response = "Your searched orders"
                    suggestions = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                   {"title": "Account"}, {"title": "Others"}]

                part_to_modify["items"] = orders_to_insert
                response['payload']['google']["systemIntent"]["data"]["listSelect"] = part_to_modify
                part_to_modify = response['payload']['google']["richResponse"]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_response
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_response
                part_to_modify['suggestions'] = suggestions

                response['payload']['google']["richResponse"] = part_to_modify
                return response
            elif len(found_orders) == 1:
                number_of_visited_places = get_number_of_visited_places(found_orders[0])
                if language == "pl":
                    if number_of_visited_places <= 4:
                        basic_card_pl = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(found_orders[0].pk),
                                "formattedText": "___Data złożenia zlecenia:___  {}  \n__Wykonawca:__  {}  \n__Usługobiorca:__  {}"
                                                 "  \n__Miejsca odjazdów:__  \n{}  \n__Miejsca docelowe:__  \n{}"
                                                 "  \n__Powiązane oferty:__  {}  \n__Kierowcy:__  {}  \n__Samochody:__  {}"
                                                 "  \n__Możliwość edycji zlecenia:__  {}  \n"
                                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                                    .format(found_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(found_orders[0], language),
                                            get_destinations(found_orders[0], language),
                                            get_related_offers(found_orders[0]), get_drivers(found_orders[0]),
                                            get_trucks(found_orders[0][0:10]), get_is_active(language, found_orders[0]),
                                            found_orders[0].remarks, found_orders[0].price)
                            }
                        }
                    elif number_of_visited_places > 4:
                        basic_card_pl = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(found_orders[0].pk),
                                "formattedText": "___Data złożenia zlecenia:___  {}  \n__Wykonawca:__  {}  \n__Usługobiorca:__  {}"
                                                 "  \n__Miejsca odjazdów:__  \n{}  \n__Miejsca docelowe:__  \n{}"
                                                 "  \n__Powiązane oferty:__  {}  \n__Możliwość edycji zlecenia:__  {}  \n"
                                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                                    .format(found_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(found_orders[0], language),
                                            get_destinations(found_orders[0], language),
                                            get_related_offers(found_orders[0]),
                                            get_is_active(language, found_orders[0]),
                                            found_orders[0].remarks, found_orders[0].price)
                            }
                        }

                    speech_text_pl = "Oto szukane zlecenie"
                    display_text_pl = "Oto szukane zlecenie"
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['items'].append(basic_card_pl)
                    part_to_modify['suggestions'] = suggestions_pl

                elif language == "en":
                    if number_of_visited_places <= 4:
                        basic_card_en = {
                            "basicCard": {
                                "title": "Order no. {}".format(found_orders[0].pk),
                                "formattedText": "___Date of placing the order:___  {}  \n__Performer:__  {}  \n__Recipient:__  {}"
                                                 "  \n__Departure places:__  \n{}  \n__Destinations:__  \n{}"
                                                 "  \n__Related offers:__  {}  \n__Drivers:__  {}  \n__Trucks:__  {}"
                                                 "  \n__The order can be edited:__  {}  \n"
                                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                                    .format(found_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(found_orders[0], language),
                                            get_destinations(found_orders[0], language),
                                            get_related_offers(found_orders[0]), get_drivers(found_orders[0]),
                                            get_trucks(found_orders[0]), get_is_active(language, found_orders[0]),
                                            found_orders[0].remarks, found_orders[0].price)
                            }
                        }
                    elif number_of_visited_places > 4:
                        basic_card_en = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(found_orders[0].pk),
                                "formattedText": "___Date of placing the order:___  {}  \n__Performer:__  {}  \n__Recipient:__  {}"
                                                 "  \n__Departure places:__  \n{}  \n__Destinations:__  \n{}"
                                                 "  \n__Related offers:__  {}  \n__The order can be edited:__  {}  \n"
                                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                                    .format(found_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(found_orders[0], language),
                                            get_destinations(found_orders[0], language),
                                            get_related_offers(found_orders[0]),
                                            get_is_active(language, found_orders[0]),
                                            found_orders[0].remarks, found_orders[0].price)
                            }
                        }

                    speech_text_en = "Here's the order you're looking for."
                    display_text_en = "Here's the order you're looking for."
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiry"},
                                      {"title": "Account"}, {"title": "Others"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                    part_to_modify['items'].append(basic_card_en)
                    part_to_modify['suggestions'] = suggestions_en

                response['payload']['google']['richResponse'] = part_to_modify
                return response
            elif len(found_orders) == 0:
                if language == "pl":
                    speech_text_pl = "Nie ma żadnych zamówień o podanych parametrach"
                    display_text_pl = "Nie ma żadnych zamówień o podanych parametrach"
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['suggestions'] = suggestions_pl
                elif language == "en":
                    speech_text_en = "There are no orders with given parameters"
                    display_text_en = "There are no orders with given parameters"
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                      {"title": "Account"}, {"title": "Others"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
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


def ask_order_accepted(request):
    """
    Create response with prompting user to give data to search order
    :param request: request from "Ask order accepted for execution" Dialogflow intent
    :return: Json with response prompting user to give data to search order
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if access_token:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "Aby dowiedzieć się czy zlecenie zostało przyjete do realizacji, podaj przynajmniej" \
                                  " jedno miejsce załadunku i jedno miejsce " \
                                  "rozładunku, ciężarówki lub samo id zlecenia." \
                                  " Na przykład:"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "Miejsca załadunku: Warszawa 15 listopada," \
                                 " godzina 8:00, 7 palet. Dortmund 17 listopada" \
                                 " godzina 9:00, 10 palet. Miejsca rozładunku: " \
                                 "Bratysława 16 listopada godzina 11:00, 7 palet," \
                                 " Sosnowiec 18 listopada, godzina 10:00, 10 palet." \
                                 " 2 mercedesy, 6000 złotych"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                             {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "To find out whether the order was accepted for execution, please provide" \
                                  " at least one loading location and one " \
                                  "unloading place, trucks or the order ID." \
                                  " For example:"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "Loading locations: Warsaw, November 15, 8:00, " \
                                 "7 pallets. Dortmund November 17 at 9:00, 10 pallets." \
                                 " Unloading places: Bratislava November 16 at 11:00, " \
                                 "7 pallets, Sosnowiec November 18, 10:00. 10 pallets. " \
                                 "2 Mercedes, 6000 PLN"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                             {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google'] = part_to_modify
        session_id = request.data["queryResult"]["outputContexts"][0]["name"]
        session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
        session_id = session_id.lstrip("sessions/").rstrip("/contexts")
        context = {
            "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/is_order_accepted".format(
                session_id),
            "lifespanCount": 5
        }
        list_with_context = list()
        list_with_context.append(context)
        response["outputContexts"] = list_with_context
        return response
    else:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "Musisz być zalogowany aby wyszukać" \
                                  " zlecenie"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "Musisz być zalogowany aby wyszukać" \
                                 " zlecenie"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                             {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "You must be logged in to search for" \
                                  " the order"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "You must be logged in to search for" \
                                 " the order"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                             {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google'] = part_to_modify
        return response


def ask_order_realised(request):
    """
    Create response with prompting user to give data to search order
    :param request: request from "Ask order realised" Dialogflow intent
    :return: Json with response prompting user to give data to search order
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if access_token:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "Aby dowiedzieć się czy zlecenie zostało zrealizowane, podaj przynajmniej" \
                                  " jedno miejsce załadunku i jedno miejsce " \
                                  "rozładunku, ciężarówki lub samo id zlecenia." \
                                  " Na przykład:"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "Miejsca załadunku: Warszawa 15 listopada," \
                                 " godzina 8:00, 7 palet. Dortmund 17 listopada" \
                                 " godzina 9:00, 10 palet. Miejsca rozładunku: " \
                                 "Bratysława 16 listopada godzina 11:00, 7 palet," \
                                 " Sosnowiec 18 listopada, godzina 10:00, 10 palet." \
                                 " 2 mercedesy, 6000 złotych"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                             {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "To find out if the order has been completed, please provide" \
                                  " at least one loading location and one " \
                                  "unloading place, trucks or the order ID." \
                                  " For example:"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "Loading locations: Warsaw, November 15, 8:00, " \
                                 "7 pallets. Dortmund November 17 at 9:00, 10 pallets." \
                                 " Unloading places: Bratislava November 16 at 11:00, " \
                                 "7 pallets, Sosnowiec November 18, 10:00. 10 pallets. " \
                                 "2 Mercedes, 6000 PLN"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                             {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google'] = part_to_modify
        session_id = request.data["queryResult"]["outputContexts"][0]["name"]
        session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
        session_id = session_id.lstrip("sessions/").rstrip("/contexts")
        context = {
            "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/is_order_realised".format(
                session_id),
            "lifespanCount": 5
        }
        list_with_context = list()
        list_with_context.append(context)
        response["outputContexts"] = list_with_context
        return response
    else:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "Musisz być zalogowany aby wyszukać" \
                                  " zlecenie"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "Musisz być zalogowany aby wyszukać" \
                                 " zlecenie"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                             {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "You must be logged in to search for" \
                                  " the order"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "You must be logged in to search for" \
                                 " the order"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                             {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google'] = part_to_modify
        return response


def check_order_accepted_for_execution(request):
    """
    Check if order is accepted for execution
    :param request: request from "Check order accepted for execution" Dialogflow intent
    :return: Json with response if order is accepted for execution
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz sprawdzić czy zlecenie jest przyjęte do relizacji, ponieważ nie posiadasz jeszcze konta. " \
                         "Jeśli chcesz założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz tego sprawdzić. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't check if order is take for execution, because you don't have an account yet. If you " \
                         "want to create a best transport Poland account, select the option \"Sign up\" below."
    display_spoken_en = "You can't check this. Create an account by selecting the option below \"Sign up\""

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
            found_orders = find_orders(request, profile)
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']

            if len(found_orders) > 1:
                if language == 'pl':
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "Musisz podać dane tylko jednego zlecenia"
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = "Musisz podać dane tylko jednego zlecenia"
                    part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                     {"title": "Konto"}, {"title": "Inne"}]
                elif language == 'en':
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = "You have to enter data for only one order."
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = "You have to enter data for only one order."
                    part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                     {"title": "Account"},{"title": "Others"}]
                response['payload']['google']['richResponse'] = part_to_modify
                return response
            elif len(found_orders) == 1:
                if language == 'pl':
                    searched_text = "Zlecenie o numerze id {} zostało przyjęte do realizacji".format(found_orders[0].pk)
                    response_to_customer = False
                    if ResponseToCustomer.objects.filter(text=searched_text).count() == 1:
                        response_to_customer = ResponseToCustomer.objects.get(text=searched_text)
                    if response_to_customer:
                        part_to_modify['items'][0]['simpleResponse'][
                            'textToSpeech'] = "Zlecenie o numerze id {} zostało przyjęte do realizacji".format(
                            found_orders[0].pk)
                        part_to_modify['items'][0]['simpleResponse'][
                            'displayText'] = "Zlecenie o numerze id {} zostało przyjęte do realizacji".format(
                            found_orders[0].pk)
                        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                         {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
                    else:
                        part_to_modify['items'][0]['simpleResponse'][
                            'textToSpeech'] = "Zlecenie o numerze id {} nie zostało jeszcze przyjęte do realizacji".format(
                            found_orders[0].pk)
                        part_to_modify['items'][0]['simpleResponse'][
                            'displayText'] = "Zlecenie o numerze id {} nie zostało jeszcze przyjęte do realizacji".format(
                            found_orders[0].pk)
                        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
                elif language == 'en':
                    searched_text = "The order with ID number {} has been accepted for execution".format(found_orders[0].pk)
                    response_to_customer = False
                    if ResponseToCustomer.objects.filter(text=searched_text).count() == 1:
                        response_to_customer = ResponseToCustomer.objects.get(text=searched_text)
                    if response_to_customer:
                        part_to_modify['items'][0]['simpleResponse'][
                            'textToSpeech'] = "The order with ID number {} has been accepted for execution".format(
                            found_orders[0].pk)
                        part_to_modify['items'][0]['simpleResponse'][
                            'displayText'] = "The order with ID number {} has been accepted for execution".format(
                            found_orders[0].pk)
                        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                         {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]
                    else:
                        part_to_modify['items'][0]['simpleResponse'][
                            'textToSpeech'] = "The order with ID number {} hasn't been accepted yet".format(
                            found_orders[0].pk)
                        part_to_modify['items'][0]['simpleResponse'][
                            'displayText'] = "The order with ID number {} hasn't been accepted yet".format(
                            found_orders[0].pk)
                        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                         {"title": "Account"},{"title": "Others"}]

                response['payload']['google']['richResponse'] = part_to_modify
                return response
            elif len(found_orders) == 0:
                if language == "pl":
                    speech_text_pl = "Nie ma żadnych zamówień o podanych parametrach"
                    display_text_pl = "Nie ma żadnych zamówień o podanych parametrach"
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['suggestions'] = suggestions_pl
                elif language == "en":
                    speech_text_en = "There are no orders with given parameters"
                    display_text_en = "There are no orders with given parameters"
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                      {"title": "Account"}, {"title": "Others"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
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


def check_order_realised(request):
    """
    Check if order is realised
    :param request: request from "Check order realised" Dialogflow intent
    :return: Json with response if order is realised
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz sprawdzić czy zlecenie jest zrealizowane, ponieważ nie posiadasz jeszcze konta. " \
                         "Jeśli chcesz założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz sprawdzić czy zlecenie jest zrealizowane. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't check if order is realised, because you don't have an account yet. If you " \
                         "want to create a best transport Poland account, select the option \"Sign up\" below."
    display_spoken_en = "You can't check if order is realised. Create an account by selecting the option below \"Sign up\""

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
            found_orders = find_orders(request, profile)
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']

            if len(found_orders) > 1:
                if language == 'pl':
                    part_to_modify['items'][0]['simpleResponse'][
                        'textToSpeech'] = "Musisz podać dane tylko jednego zlecenia"
                    part_to_modify['items'][0]['simpleResponse'][
                        'displayText'] = "Musisz podać dane tylko jednego zlecenia"
                    part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                     {"title": "Konto"}, {"title": "Inne"}]
                elif language == 'en':
                    part_to_modify['items'][0]['simpleResponse'][
                        'textToSpeech'] = "You have to enter data for only one order."
                    part_to_modify['items'][0]['simpleResponse'][
                        'displayText'] = "You have to enter data for only one order."
                    part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                     {"title": "Account"}, {"title": "Others"}]
                response['payload']['google']['richResponse'] = part_to_modify
                return response
            elif len(found_orders) == 1:
                if language == 'pl':
                    searched_text = "Zlecenie numer {} zostało zrealizowane".format(found_orders[0].pk)
                    realised = False
                    all_orders = Order.objects.all()
                    for order in all_orders:
                        remarks = order.remarks
                        if searched_text in remarks:
                            realised = True
                    if realised:
                        part_to_modify['items'][0]['simpleResponse'][
                            'textToSpeech'] = "Zlecenie o numerze id {} zostało zrealizowane".format(
                            found_orders[0].pk)
                        part_to_modify['items'][0]['simpleResponse'][
                            'displayText'] = "Zlecenie o numerze id {} zostało zrealizowane".format(
                            found_orders[0].pk)
                        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                         {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
                    else:
                        part_to_modify['items'][0]['simpleResponse'][
                            'textToSpeech'] = "Zlecenie o numerze id {} nie zostało zrealizowane".format(
                            found_orders[0].pk)
                        part_to_modify['items'][0]['simpleResponse'][
                            'displayText'] = "Zlecenie o numerze id {} nie zostało zrealizowane".format(
                            found_orders[0].pk)
                        part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                         {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
                elif language == 'en':
                    searched_text = "Order number {} has been executed".format(found_orders[0].pk)
                    realised = False
                    all_orders = Order.objects.all()
                    for order in all_orders:
                        remarks = order.remarks
                        if searched_text in remarks:
                            realised = True
                    if realised:
                        part_to_modify['items'][0]['simpleResponse'][
                            'textToSpeech'] = "Order number {} has been executed".format(found_orders[0].pk)
                        part_to_modify['items'][0]['simpleResponse'][
                            'displayText'] = "Order number {} has been executed".format(found_orders[0].pk)
                        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                         {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]
                    else:
                        part_to_modify['items'][0]['simpleResponse'][
                            'textToSpeech'] = "Order number {} hasn't been executed".format(found_orders[0].pk)
                        part_to_modify['items'][0]['simpleResponse'][
                            'displayText'] = "Order number {} hasn't been executed".format(found_orders[0].pk)
                        part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                         {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

                response['payload']['google']['richResponse'] = part_to_modify
                return response
            elif len(found_orders) == 0:
                if language == "pl":
                    speech_text_pl = "Nie ma żadnych zamówień o podanych parametrach"
                    display_text_pl = "Nie ma żadnych zamówień o podanych parametrach"
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['suggestions'] = suggestions_pl
                elif language == "en":
                    speech_text_en = "There are no orders with given parameters"
                    display_text_en = "There are no orders with given parameters"
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                      {"title": "Account"}, {"title": "Others"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
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


def ask_remove_order(request):
    """
    Creates response prompting user to give order data
    :param request: request from "Ask remove order" Dialogflow intent
    :return: Json prompting user to give order data
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if access_token:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "Aby usunąć zlecenie, podaj przynajmniej" \
                                  " jedno miejsce załadunku i jedno miejsce " \
                                  "rozładunku, ciężarówki lub samo id zlecenia." \
                                  " Na przykład:"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "Miejsca załadunku: Warszawa 15 listopada," \
                                 " godzina 8:00, 7 palet. Dortmund 17 listopada" \
                                 " godzina 9:00, 10 palet. Miejsca rozładunku: " \
                                 "Bratysława 16 listopada godzina 11:00, 7 palet," \
                                 " Sosnowiec 18 listopada, godzina 10:00, 10 palet." \
                                 " 2 mercedesy, 6000 złotych"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                             {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "To remove order, please provide" \
                                  " at least one loading location and one " \
                                  "unloading place, trucks or the order ID." \
                                  " For example:"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "Loading locations: Warsaw, November 15, 8:00, " \
                                 "7 pallets. Dortmund November 17 at 9:00, 10 pallets." \
                                 " Unloading places: Bratislava November 16 at 11:00, " \
                                 "7 pallets, Sosnowiec November 18, 10:00. 10 pallets. " \
                                 "2 Mercedes, 6000 PLN"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                             {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google'] = part_to_modify
        session_id = request.data["queryResult"]["outputContexts"][0]["name"]
        session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
        session_id = session_id.lstrip("sessions/").rstrip("/contexts")
        context = {
            "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/remove_order".format(
                session_id),
            "lifespanCount": 5
        }
        list_with_context = list()
        list_with_context.append(context)
        response["outputContexts"] = list_with_context
        return response
    else:
        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "Musisz być zalogowany aby usunąć zlecenie"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "Musisz być zalogowany aby usunąć zlecenie"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                             {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "You must be logged in to remove the order"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "You must be logged in to remove the order"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                             {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google'] = part_to_modify
        return response


def remove_order(request):
    """
    Searches one order to remove. Asks user if he want to remove found order
    :param request: request from "Remove order" Dialogflow intent
    :return: Json with basic card that is Dialogflow item. This card contains order to delete
    """
    language = request.data['queryResult']['languageCode']
    response_spoken_pl = "Nie możesz usunąć zlecenia, ponieważ nie posiadasz jeszcze konta. " \
                         "Jeśli chcesz założyć konto w best transport Polska, wybierz poniższą opcję Zarejestruj się"
    display_spoken_pl = "Nie możesz usunąć zlecenia. Załóż konto przez wybranie poniższej opcji Zarejestruj się"
    response_spoken_en = "You can't delete order, because you don't have an account yet. If you " \
                         "want to create a best transport Poland account, select the option \"Sign up\" below."
    display_spoken_en = "You can't delete order. Create an account by selecting the option below \"Sign up\""

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
            found_orders = find_orders(request, profile)
            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']

            if len(found_orders) > 1:
                if language == 'pl':
                    part_to_modify['items'][0]['simpleResponse'][
                        'textToSpeech'] = "Musisz podać dane tylko jednego zlecenia"
                    part_to_modify['items'][0]['simpleResponse'][
                        'displayText'] = "Musisz podać dane tylko jednego zlecenia"
                    part_to_modify['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                     {"title": "Konto"}, {"title": "Inne"}]
                elif language == 'en':
                    part_to_modify['items'][0]['simpleResponse'][
                        'textToSpeech'] = "You have to enter data for only one order."
                    part_to_modify['items'][0]['simpleResponse'][
                        'displayText'] = "You have to enter data for only one order."
                    part_to_modify['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                     {"title": "Account"}, {"title": "Others"}]
                response['payload']['google']['richResponse'] = part_to_modify
                return response
            elif len(found_orders) == 1:
                number_of_visited_places = get_number_of_visited_places(found_orders[0])
                if language == "pl":
                    if number_of_visited_places <= 4:
                        basic_card_pl = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(found_orders[0].pk),
                                "formattedText": "___Data złożenia zlecenia:___  {}  \n__Wykonawca:__  {}  \n__Usługobiorca:__  {}"
                                                 "  \n__Miejsca odjazdów:__  \n{}  \n__Miejsca docelowe:__  \n{}"
                                                 "  \n__Powiązane oferty:__  {}  \n__Kierowcy:__  {}  \n__Samochody:__  {}"
                                                 "  \n__Możliwość edycji zlecenia:__  {}  \n"
                                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                                    .format(found_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(found_orders[0], language),
                                            get_destinations(found_orders[0], language),
                                            get_related_offers(found_orders[0]), get_drivers(found_orders[0]),
                                            get_trucks(found_orders[0]), get_is_active(language, found_orders[0]),
                                            found_orders[0].remarks, found_orders[0].price)
                            }
                        }
                    elif number_of_visited_places > 4:
                        basic_card_pl = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(found_orders[0].pk),
                                "formattedText": "___Data złożenia zlecenia:___  {}  \n__Wykonawca:__  {}  \n__Usługobiorca:__  {}"
                                                 "  \n__Miejsca odjazdów:__  \n{}  \n__Miejsca docelowe:__  \n{}"
                                                 "  \n__Powiązane oferty:__  {}  \n__Możliwość edycji zlecenia:__  {}  \n"
                                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                                    .format(found_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(found_orders[0], language),
                                            get_destinations(found_orders[0], language),
                                            get_related_offers(found_orders[0]),
                                            get_is_active(language, found_orders[0]),
                                            found_orders[0].remarks, found_orders[0].price)
                            }
                        }

                    speech_text_pl = "Czy na pewno chcesz usunąć to zlecenie?"
                    display_text_pl = "Czy na pewno chcesz usunąć to zlecenie?"
                    suggestions_pl = [{"title": "Tak"}, {"title": "Nie"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['items'].append(basic_card_pl)
                    part_to_modify['suggestions'] = suggestions_pl

                elif language == "en":
                    if number_of_visited_places <= 4:
                        basic_card_en = {
                            "basicCard": {
                                "title": "Order no. {}".format(found_orders[0].pk),
                                "formattedText": "___Date of placing the order:___  {}  \n__Performer:__  {}  \n__Recipient:__  {}"
                                                 "  \n__Departure places:__  \n{}  \n__Destinations:__  \n{}"
                                                 "  \n__Related offers:__  {}  \n__Drivers:__  {}  \n__Trucks:__  {}"
                                                 "  \n__The order can be edited:__  {}  \n"
                                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                                    .format(found_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(found_orders[0], language),
                                            get_destinations(found_orders[0], language),
                                            get_related_offers(found_orders[0]), get_drivers(found_orders[0]),
                                            get_trucks(found_orders[0]), get_is_active(language, found_orders[0]),
                                            found_orders[0].remarks, found_orders[0].price)
                            }
                        }
                    elif number_of_visited_places > 4:
                        basic_card_en = {
                            "basicCard": {
                                "title": "Zlecenie nr {}".format(found_orders[0].pk),
                                "formattedText": "___Date of placing the order:___  {}  \n__Performer:__  {}  \n__Recipient:__  {}"
                                                 "  \n__Departure places:__  \n{}  \n__Destinations:__  \n{}"
                                                 "  \n__Related offers:__  {}  \n__The order can be edited:__  {}  \n"
                                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                                    .format(found_orders[0].date, get_performer(language), get_order_client(profile),
                                            get_departure_places(found_orders[0], language),
                                            get_destinations(found_orders[0], language),
                                            get_related_offers(found_orders[0]),
                                            get_is_active(language, found_orders[0]),
                                            found_orders[0].remarks, found_orders[0].price)
                            }
                        }

                    speech_text_en = "Are you sure you want to delete this order?"
                    display_text_en = "Are you sure you want to delete this order?"
                    suggestions_en = [{"title": "Yes"}, {"title": "No"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
                    part_to_modify['items'].append(basic_card_en)
                    part_to_modify['suggestions'] = suggestions_en

                response['payload']['google']['richResponse'] = part_to_modify
                session_id = request.data["queryResult"]["outputContexts"][0]["name"]
                session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
                session_id = session_id.lstrip("sessions/").rstrip("/contexts")
                context = {
                    "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/order_to_remove".format(
                        session_id),
                    "lifespanCount": 2,
                    "parameters": {
                        "order_to_remove": found_orders[0].pk
                    }
                }
                list_with_context = list()
                list_with_context.append(context)
                response["outputContexts"] = list_with_context
                return response
            elif len(found_orders) == 0:
                if language == "pl":
                    speech_text_pl = "Nie ma żadnych zamówień o podanych parametrach"
                    display_text_pl = "Nie ma żadnych zamówień o podanych parametrach"
                    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                      {"title": "Konto"}, {"title": "Inne"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
                    part_to_modify['suggestions'] = suggestions_pl
                elif language == "en":
                    speech_text_en = "There are no orders with given parameters"
                    display_text_en = "There are no orders with given parameters"
                    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                      {"title": "Account"}, {"title": "Others"}]
                    part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
                    part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
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


def remove_order_no(request):
    """
    Creates response about no remove order
    :param request: POST request from "Remove order - no" Dialogflow intent
    :return: JSON with info about order hasn't been deleted
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
                response_spoken_pl = "Nie ma sprawy, Twoje zlecenie nie zostanie usunięte. Wybierz co chcesz jeszcze zrobić"
                display_spoken_pl = "Nie ma sprawy, Twoje zlecenie nie zostanie usunięte. Wybierz co chcesz jeszcze zrobić"
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "No problem, your order will not be deleted. Choose what you want to do next"
                display_spoken_en = "No problem, your order will not be deleted. Choose what you want to do next"
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


def remove_order_related_objects(order_to_remove):
    """
    Removes related objects to order
    :param order_to_remove: order for which related objects are deleting
    :return: No
    """
    if OrdersVehicles.objects.filter(order=order_to_remove).count() > 0:
        orders_vehicles = OrdersVehicles.objects.filter(order=order_to_remove)
        for order_vehicle in orders_vehicles:
            order_vehicle.delete()
    if OrdersDrivers.objects.filter(order=order_to_remove).count() > 0:
        orders_drivers = OrdersDrivers.objects.filter(order=order_to_remove)
        for order_driver in orders_drivers:
            order_driver.delete()
    if OrdersLoadingPlaces.objects.filter(order=order_to_remove).count() > 0:
        orders_loadings = OrdersLoadingPlaces.objects.filter(order=order_to_remove)
        for order_loading in orders_loadings:
            order_loading.delete()
    if OrdersDestinationPlaces.objects.filter(order=order_to_remove).count() > 0:
        orders_destinations = OrdersDestinationPlaces.objects.filter(order=order_to_remove)
        for order_destination in orders_destinations:
            order_destination.delete()


def remove_order_yes(request):
    """
    Removes order
    :param request: POST request from "Remove order - yes" Dialogflow intent
    :return: JSON with info about order has been deleted
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
            contexts = request.data["queryResult"]["outputContexts"]
            order_to_remove = ""
            for context in contexts:
                if "order_to_remove" in context["name"]:
                    order_to_remove = context["parameters"]["order_to_remove"]
            remove_order_related_objects(order_to_remove)
            order = Order.objects.get(pk=order_to_remove)
            order.delete()

            with open('api/response.json') as json_file:
                response = json.load(json_file)
            part_to_modify = response['payload']['google']['richResponse']
            if language == "pl":
                response_spoken_pl = "Twoje zlecenie o id równym {} zostało usunięte. Wybierz co chcesz jeszcze zrobić".format(order_to_remove)
                display_spoken_pl = "Twoje zlecenie o id równym {} zostało usunięte. Wybierz co chcesz jeszcze zrobić".format(order_to_remove)
                suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                                  {"title": "Inne"}]
                part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = response_spoken_pl
                part_to_modify['items'][0]['simpleResponse']['displayText'] = display_spoken_pl
                part_to_modify['suggestions'] = suggestions_pl
            elif language == "en":
                response_spoken_en = "Your order with id equal {} has been deleted. Choose what you want to do next".format(order_to_remove)
                display_spoken_en = "Your order with id equal {} has been deleted. Choose what you want to do next".format(order_to_remove)
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


def ask_create_order(request):
    """
    Creates response prompting user to give loadings data for creating order
    :param request: request from "Ask create order" Dialogflow intent
    :return: Json with response prompting user to give loadings data for creating order
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']
    
    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Aby złożyć zlecenie podaj najpierw miejsca załadunku. Na przykład: "
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Warszawa ulica Józefa Poniatowskiego 10 kod pocztowy 01 007 Warszawa, Warszawa ulica " \
                             "Henryka Dąbrowskiego 12 kod pocztowy 05 0100 Warszawa, Amsterdam ulica Maxwellstraat 3, " \
                             "kod pocztowy 1097 Amsterdam"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "To place an order, first enter the places of loadings. For example:"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Warsaw street of Józef Poniatowski 10 postal code 01 007 Warsaw, Warsaw street of " \
                             "Henryk Dąbrowski 12 postcode 05 0100 Warsaw, Amsterdam street Maxwellstraat 3, " \
                             "postal code 1097 Amsterdam"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                        {"title": "Account"}, {"title": "Others"}]

    response['payload']['google'] = part_to_modify
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/ask_creating_order".format(
            session_id),
        "lifespanCount": 3
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context
    return response


def extract_order_places(request, my_data):
    """
    Extracts order parameters from text
    :param request: request from "Create order loadings places" Dialogflow intent
    :return: dictionary with parameters extracted from text
    """
    language = request.data['queryResult']['languageCode']
    text = request.data["queryResult"]["queryText"]
    text_array = text.split()
    array_length = len(text_array)
    parameters_from_text = dict()
    post_code_index = 0
    counter = 0

    if language == 'pl':
        street_language = "ulica"
        code_language = "kod"
        post_language = "pocztowy"
    elif language == 'en':
        street_language = "street"
        code_language = "postcode"
        post_language = "postcode"

    if my_data == 'loadings':
        my_street = "my_loading_street"
        my_post_code = "my_loading_post_code"
        my_post_place = "my_loading_post_place"
    elif my_data == 'destinations':
        my_street = "my_destination_street"
        my_post_code = "my_destination_post_code"
        my_post_place = "my_destination_post_place"

    while array_length > post_code_index + 1:
        text_array = text_array[post_code_index:]
        street_index = text_array.index(street_language)
        code_index = text_array.index(code_language)
        street = ""
        for i in range(street_index + 1, code_index):
            street += text_array[i]
            street += " "
        street = street[:-1]
        parameters_from_text["{}{}".format(my_street, counter)] = street

        post_code = ""
        post_code_index = text_array.index(post_language) + 1
        while text_array[post_code_index].isdigit():
            post_code += text_array[post_code_index]
            post_code += " "
            post_code_index += 1

        post_code = post_code[:-1]
        parameters_from_text["{}{}".format(my_post_code, counter)] = post_code

        post_place = text_array[post_code_index]
        parameters_from_text["{}{}".format(my_post_place, counter)] = post_place

        counter += 1
        array_length = len(text_array)

    return parameters_from_text


def create_order_loadings_places_dates(request):
    """
    Handles input data with loadings places. Creates response with prompting user to give info about loadings dates
    :param request: request from "Create order loadings places" Dialogflow intent
    :return: Json with prompting user to give data of loadings dates
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']
    text = request.data["queryResult"]["queryText"]

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Podaj teraz datę, godzinę i liczbę palet dla każdego załadunku. Podaj w takiej kolejności w jakiej " \
                              "wprowadziłeś miejsca załadunków"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "{}".format(text)
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Enter the date, time and number of pallets for each load now. Enter in the order in which " \
                              "you entered the loadings"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "{}".format(text)
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

    response['payload']['google'] = part_to_modify
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")

    parameters_from_text = extract_order_places(request, "loadings")
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_order_places".format(
            session_id),
        "lifespanCount": 3,
        "parameters": parameters_from_text
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context
    return response


def add_parameters_to_context(request, previous_context_name, current_parameters="", loadings_or_destinations=""):
    """
    Create new dictionary with previous and current parameters
    :param request: request from "Creating order loadings dates" Dialogflow intent
    :param previous_context_name: name of searched context
    :param current_parameters: dictionary with current parameters
    :param: loadings_or_destinations: index of current parameters
    :return: dictionary with previous and current parameters
    """
    contexts = request.data["queryResult"]["outputContexts"]
    previous_parameters = ""
    for context in contexts:
        if re.search(r"{}$".format(previous_context_name), context["name"]):
            previous_parameters = context["parameters"]
            break

    output_parameters = dict()
    for key, value in previous_parameters.items():
        if "my_" in key:
            output_parameters[key] = previous_parameters[key]

    if current_parameters == "":
        current_parameters = request.data["queryResult"]["parameters"]
        searched_keys = {"date": 0, "time": 0, "number": 0}
        for key, value in current_parameters.items():
            if current_parameters[key] != "":
                if "date" in key:
                    output_parameters["my_date_{}{}".format(loadings_or_destinations, searched_keys["date"])] = current_parameters[key]
                    searched_keys["date"] += 1
                elif "time" in key:
                    output_parameters["my_time_{}{}".format(loadings_or_destinations, searched_keys["time"])] = current_parameters[key]
                    searched_keys["time"] += 1
                elif "number" in key:
                    output_parameters["my_number_{}{}".format(loadings_or_destinations, searched_keys["number"])] = current_parameters[key]
                    searched_keys["number"] += 1
    else:
        for key, value in current_parameters.items():
            output_parameters[key] = current_parameters[key]

    return output_parameters


# def get_orders_dates_from_text(parameters):
#     """
#     Takes from request parameters dates and number of pallets and place it second dictionary
#     :param parameters: dictionary of parameters from request
#     :return: dictionary contains dates and numbers of pallets in parameters
#     """
#     parameters_from_text = dict()
#     for key, value in parameters.items():
#         if parameters[key] != "":
#             parameters_from_text["my_{}".format(key)] = parameters[key]
#
#     return parameters_from_text


def create_order_loadings_dates(request):
    """
    Take dates parameters from text and place in custom context
    :param request: request from "Creating order loadings dates" Dialogflow intent
    :return: Json with prompting user to give destination places and with custom context
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Podaj miejsca rozładunków w taki sam sposób jak podałeś miejsca załadunków"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Warszawa ulica Przemysłowa 9 kod pocztowy 07 001 Warszawa, Warszawa ulica " \
                             "Techniczna 13 kod pocztowy 05 0105 Warszawa, Rotterdam ulica Maxwellstraat 3, " \
                             "kod pocztowy 9710 Rotterdam"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Give the places of unloading in the same way as you provided the places of loading"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Warsaw street Przemysłowa 9 postcode 07 001 Warsaw, Warsaw street Technical 13 postcode 05 0105 Warsaw," \
                             " Rotterdam street Maxwellstraat 3 postcode 9710 Rotterdam"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

    response['payload']['google'] = part_to_modify
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")

    #request_parameters = request.data["queryResult"]["parameters"]
    #parameters_from_text = get_orders_dates_from_text(request_parameters)
    parameters_from_text = add_parameters_to_context(request, "creating_order_places", loadings_or_destinations="loading")
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_order_dates".format(
            session_id),
        "lifespanCount": 3,
        "parameters": parameters_from_text
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context
    return response


def create_order_destinations_places_dates(request):
    """
    Handles input data with destination places. Creates response with prompting user to give info about destination dates
    :param request: request from "Create order destination places" Dialogflow intent
    :return: Json with prompting user to give data of destination dates
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']
    text = request.data["queryResult"]["queryText"]

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Podaj teraz datę, godzinę i liczbę palet dla każdego rozładunku. Podaj w takiej kolejności w jakiej " \
                              "wprowadziłeś miejsca rozładunków"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "{}".format(text)
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Enter the date, time and number of pallets for each unload now. Enter in the order in which " \
                              "you entered the destinations"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "{}".format(text)
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

    response['payload']['google'] = part_to_modify
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")

    parameters_from_text = extract_order_places(request, "destinations")
    parameters_from_text = add_parameters_to_context(request, "creating_order_dates", parameters_from_text)
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_order_places_destinations".format(
            session_id),
        "lifespanCount": 3,
        "parameters": parameters_from_text
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context
    return response


def create_order_destinations_dates(request):
    """
    Take dates parameters from text and place in custom context
    :param request: request from "Creating order destinations dates" Dialogflow intent
    :return: Json with prompting user to give destination places and with custom context
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Czy chcesz wprowadzić do zamówienia dodatkowe uwagi?"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Czy chcesz wprowadzić do zamówienia dodatkowe uwagi?"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Tak"}, {"title": "Nie"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Do you want to add additional comments to your order?"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Do you want to add additional comments to your order?"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Yes"}, {"title": "No"}]

    response['payload']['google'] = part_to_modify
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")

    parameters_from_text = add_parameters_to_context(request, "creating_order_places_destinations", loadings_or_destinations="destination")
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_order_dates_destinations".format(
            session_id),
        "lifespanCount": 3,
        "parameters": parameters_from_text
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context
    return response


def create_order_destinations_dates_yes(request):
    """
    Take parameters from previous context and prompts user to give additional notes to creating order
    :param request: request from "Creating order destinations dates - yes" Dialogflow intent
    :return: Json with prompting user to give additional notes to the creating order and with custom context
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Wprowadź teraz dodatkowe uwagi do tworzonego zlecenia"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Wprowadź teraz dodatkowe uwagi do tworzonego zlecenia"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Now add additional notes to the created order"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Now add additional notes to the created order"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

    response['payload']['google'] = part_to_modify
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")

    parameters_from_text = add_parameters_to_context(request, "creating_order_dates_destinations")
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_order_dates_destinations_plus".format(
            session_id),
        "lifespanCount": 3,
        "parameters": parameters_from_text
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context
    return response


def create_order_destinations_dates_no(request):
    """
    Takes parameters from previous context and prompts user to give price order
    :param request: request from "Creating order destinations dates - no" Dialogflow intent
    :return: Json with prompting user to give price order and with custom context
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Wprowadź teraz twoją cenę zlecenia"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Wprowadź teraz twoją cenę zlecenia"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                         {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Now enter your order price"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Now enter your order price"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                         {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

    response['payload']['google'] = part_to_modify
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")

    parameters_from_text = add_parameters_to_context(request, "creating_order_dates_destinations")
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_order_dates_destinations_plus".format(
            session_id),
        "lifespanCount": 3,
        "parameters": parameters_from_text
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context
    return response


def create_order_additional_notes(request):
    """
    Create response with prompting user to give price of creating order and with custom context
    :param request: request from "Create order additional notes" Dialogflow intent
    :return: Json with prompting user to give price of creating order and with custom context
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Wprowadź teraz twoją cenę zlecenia"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Wprowadź teraz twoją cenę zlecenia"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Now enter your order price"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Now enter your order price"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

    response['payload']['google'] = part_to_modify
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")

    remarks = dict()
    remarks["my_remarks"] = request.data["queryResult"]["queryText"]
    parameters_from_text = add_parameters_to_context(request, "creating_order_dates_destinations_plus", remarks)
    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_order_additional_notes".format(
            session_id),
        "lifespanCount": 3,
        "parameters": parameters_from_text
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context
    return response


def find_previous_context(request):
    """
    Founded previous context and return its in string
    :param request: request from "Create order price" Dialogflow intent
    :return: String with previous context
    """
    contexts = request.data["queryResult"]["outputContexts"]
    possible_previous_contexts = {"creating_order_additional_notes": False, "creating_order_dates_destinations_plus": False}
    for context in contexts:
        for key, value in possible_previous_contexts.items():
            if key in context["name"]:
                possible_previous_contexts[key] = True

    if possible_previous_contexts["creating_order_additional_notes"] == True:
        searched_previous_context = "creating_order_additional_notes"
    else:
        searched_previous_context = "creating_order_dates_destinations_plus"

    return searched_previous_context


def create_order_price(request):
    """
    Creates response with event triggering "Create order" Dialogflow intent or with prompting user to give his
    telephone number and email
    :param request: request from "Create order price" Dialogflow intent
    :return: Json with event triggering "Create order" Dialogflow intent or Json with prompting user to give his
    telephone number and email
    """
    price = dict()
    price["my_price"] = request.data["queryResult"]["queryText"]
    previous_context = find_previous_context(request)
    parameters_from_text = add_parameters_to_context(request, previous_context, price)
    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
    else:
        access_token = None

    if access_token:
        language = request.data['queryResult']['languageCode']
        if language == "pl":
            response = {
                "followupEventInput": {
                    "name": "create_order_event",
                    "parameters": parameters_from_text,
                    "languageCode": "pl"
                }
            }
        elif language == "en":
            response = {
                "followupEventInput": {
                    "name": "create_order_event",
                    "parameters": parameters_from_text,
                    "languageCode": "en"
                }
            }
        return response
    else:
        with open('api/response.json') as json_file:
            response = json.load(json_file)

        part_to_modify = response['payload']['google']

        if request.data['queryResult']['languageCode'] == 'pl':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "Podaj jeszcze swój numer telefonu i adres e-mail"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "Podaj jeszcze swój numer telefonu i adres e-mail"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                             {"title": "Zapytania"},
                                                             {"title": "Konto"}, {"title": "Inne"}]
        elif request.data['queryResult']['languageCode'] == 'en':
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'textToSpeech'] = "Enter your phone number and e-mail address"
            part_to_modify['richResponse']['items'][0]['simpleResponse'][
                'displayText'] = "Enter your phone number and e-mail address"
            part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                             {"title": "Inquiries"},
                                                             {"title": "Account"}, {"title": "Others"}]

        response['payload']['google'] = part_to_modify
        session_id = request.data["queryResult"]["outputContexts"][0]["name"]
        session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
        session_id = session_id.lstrip("sessions/").rstrip("/contexts")

        context = {
            "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_order_telephone_email".format(
                session_id),
            "lifespanCount": 3,
            "parameters": parameters_from_text
        }
        list_with_context = list()
        list_with_context.append(context)
        response["outputContexts"] = list_with_context
        return response


def create_order_email_phone_number(request):
    """
    Creates event triggering "Create order" Dialogflow intent
    :param request: request from "Create order telephone email" Dialogflow intent
    :return: Json with event triggering "Create order" Dialogflow intent
    """
    parameters_from_text = add_parameters_to_context(request, "creating_order_telephone_email")
    language = request.data['queryResult']['languageCode']
    if language == "pl":
        response = {
            "followupEventInput": {
                "name": "create_order_event",
                "parameters": parameters_from_text,
                "languageCode": "pl"
            }
        }
    elif language == "en":
        response = {
            "followupEventInput": {
                "name": "create_order_event",
                "parameters": parameters_from_text,
                "languageCode": "en"
            }
        }
    return response


def get_loadings_for_created_order(language, parameters_from_text):
    """
    Creates string with loadings information
    :param language: language from request
    :param parameters_from_text: order parameters gathering from previous contexts
    :return: string with loadings information
    """
    loadings_keys = list()
    keys = list(parameters_from_text)
    for item in keys:
        if "loading" in item:
            loadings_keys.append(item)

    number_of_dates = 0
    for item in loadings_keys:
        if "date" in item:
            number_of_dates += 1

    dicts_list = list()
    for i in range(0, number_of_dates):
        temp_dict = dict()
        for item in loadings_keys:
            if str(i) in item:
                temp_dict[item] = parameters_from_text[item]
        dicts_list.append(temp_dict)

    output_string = ""
    counter = 1
    parameter_index = 0
    for dictionary in dicts_list:
        if language == 'pl':
            output_string += "{}. {} godz. {}, ulica: {} {} {}, liczba palet: {}\n".format(
                counter, dictionary["my_date_loading{}".format(parameter_index)][0:10],
                dictionary["my_time_loading{}".format(parameter_index)][11:16],
                dictionary["my_loading_street{}".format(parameter_index)],
                dictionary["my_loading_post_code{}".format(parameter_index)],
                dictionary["my_loading_post_place{}".format(parameter_index)],
                dictionary["my_number_loading{}".format(parameter_index)])
        elif language == 'en':
            output_string += "{}. {} at {}, {} street, {} {}, pallets: {}\n".format(
                counter, dictionary["my_date_loading{}".format(parameter_index)][0:10],
                dictionary["my_time_loading{}".format(parameter_index)][11:16],
                dictionary["my_loading_street{}".format(parameter_index)],
                dictionary["my_loading_post_code{}".format(parameter_index)],
                dictionary["my_loading_post_place{}".format(parameter_index)],
                dictionary["my_number_loading{}".format(parameter_index)])
        counter += 1
        parameter_index += 1

    return output_string


def get_destinations_for_created_order(language, parameters_from_text):
    """
    Creates string with destinations information
    :param language: language from request
    :param parameters_from_text: order parameters gathering from previous contexts
    :return: string with destinations information
    """
    destinations_keys = list()
    keys = list(parameters_from_text)
    for item in keys:
        if "destination" in item:
            destinations_keys.append(item)

    number_of_dates = 0
    for item in destinations_keys:
        if "date" in item:
            number_of_dates += 1

    dicts_list = list()
    for i in range(0, number_of_dates):
        temp_dict = dict()
        for item in destinations_keys:
            if str(i) in item:
                temp_dict[item] = parameters_from_text[item]
        dicts_list.append(temp_dict)

    output_string = ""
    counter = 1
    parameter_index = 0
    for dictionary in dicts_list:
        if language == 'pl':
            output_string += "{}. {} godz. {}, ulica: {} {} {}, liczba palet: {}\n".format(
                counter, dictionary["my_date_destination{}".format(parameter_index)][0:10],
                dictionary["my_time_destination{}".format(parameter_index)][11:16],
                dictionary["my_destination_street{}".format(parameter_index)],
                dictionary["my_destination_post_code{}".format(parameter_index)],
                dictionary["my_destination_post_place{}".format(parameter_index)],
                dictionary["my_number_destination{}".format(parameter_index)])
        elif language == 'en':
            output_string += "{}. {} at {}, {} street, {} {}, pallets: {}\n".format(
                counter, dictionary["my_date_destination{}".format(parameter_index)][0:10],
                dictionary["my_time_destination{}".format(parameter_index)][11:16],
                dictionary["my_destination_street{}".format(parameter_index)],
                dictionary["my_destination_post_code{}".format(parameter_index)],
                dictionary["my_destination_post_place{}".format(parameter_index)],
                dictionary["my_number_destination{}".format(parameter_index)])
        counter += 1
        parameter_index += 1

    return output_string


def create_order(request):
    """
    Creates question if user want to create order and creates basic card contains data of order
    :param request: request from "Create order" Dialogflow intent
    :return: Json with question if user want to create order and with basic card contains data of order
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Czy na pewno chcesz stworzyć to zamówienie?"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Czy na pewno chcesz stworzyć to zamówienie?"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Tak"}, {"title": "Nie"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Are you sure you want to create this order?"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Are you sure you want to create this order?"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Yes"}, {"title": "No"}]

    language = request.data['queryResult']['languageCode']
    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
        profile_token = Token.objects.get(key=access_token)
        user = profile_token.user
        profile = Profile.objects.get(user=user)
    else:
        access_token = None
    parameters_from_text = add_parameters_to_context(request, "create_order_event")

    if "my_remarks" in parameters_from_text:
        remarks = parameters_from_text["my_remarks"]
    else:
        remarks = ""

    if access_token and language == 'pl':
        basic_card = {
            "basicCard": {
                "title": "Dane Twojego zlecenia",
                "formattedText": "__Wykonawca:__  {}  \n__Usługobiorca:__  {}  \n"
                                 "  \n__Miejsca odjazdów:__  {}  \n__Miejsca docelowe:__  {}  \n"
                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                    .format(get_performer(language), get_order_client(profile),
                            get_loadings_for_created_order(language, parameters_from_text),
                            get_destinations_for_created_order(language, parameters_from_text),
                            remarks, parameters_from_text["my_price"])
            }
        }
    elif access_token and language == 'en':
        basic_card = {
            "basicCard": {
                "title": "Data of your order",
                "formattedText": "__Performer:__  {}  \n__Client:__  {}  \n"
                                 "  \n__Departures:__  {}  \n__Destinations:__  {}  \n"
                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                    .format(get_performer(language), get_order_client(profile),
                            get_loadings_for_created_order(language, parameters_from_text),
                            get_destinations_for_created_order(language, parameters_from_text),
                            remarks, parameters_from_text["my_price"])
            }
        }
    elif language == 'pl':
        basic_card = {
            "basicCard": {
                "title": "Dane Twojego zlecenia",
                "formattedText": "__Wykonawca:__  {}  \n__Email klienta:__  {}  \n__Numer telefonu klienta:__  {}"
                                 "  \n__Miejsca odjazdów:__  {}  \n__Miejsca docelowe:__  {}  \n"
                                 "__Uwagi:__  {}  \n__Cena:__  {} pln"
                    .format(get_performer(language), parameters_from_text["Email"], parameters_from_text["telephone-number"],
                            get_loadings_for_created_order(language, parameters_from_text),
                            get_destinations_for_created_order(language, parameters_from_text),
                            remarks, parameters_from_text["my_price"])
            }
        }
    elif language == 'en':
        basic_card = {
            "basicCard": {
                "title": "Data of your order",
                "formattedText": "__Performer:__  {}  \n__Customer email:__  {}  \n__Customer_telephone_number:__  {}"
                                 "  \n__Departures:__  {}  \n__Destinations:__  {}  \n"
                                 "__Remarks:__  {}  \n__Price:__  {} pln"
                    .format(get_performer(language), parameters_from_text["Email"], parameters_from_text["telephone-number"],
                            get_loadings_for_created_order(language, parameters_from_text),
                            get_destinations_for_created_order(language, parameters_from_text),
                            remarks, parameters_from_text["my_price"])
            }
        }

    response['payload']['google'] = part_to_modify
    response['payload']['google']['richResponse']["items"].append(basic_card)
    session_id = request.data["queryResult"]["outputContexts"][0]["name"]
    session_id = re.search(r"sessions\/.*\/contexts", session_id).group()
    session_id = session_id.lstrip("sessions/").rstrip("/contexts")

    context = {
        "name": "projects/best-trans-968c8/agent/sessions/{}/contexts/creating_order_final".format(
            session_id),
        "lifespanCount": 3,
        "parameters": parameters_from_text
    }
    list_with_context = list()
    list_with_context.append(context)
    response["outputContexts"] = list_with_context
    return response


def create_order_no(request):
    """
    Creates Json with question to user what he want to do
    :param request: request from "Create order - no" Dialogflow intent
    :return: Json with question to user what he want to do
    """
    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Nie ma sprawy, wybierz co chcesz jeszcze zrobić"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Nie ma sprawy, wybierz co chcesz jeszcze zrobić"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                         {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "No problem, choose what you want to do"
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "No problem, choose what you want to do"
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                         {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

    response['payload']['google'] = part_to_modify
    return response


def creating_order(request, parameters):
    """

    :param request:
    :param parameters:
    :return:
    """
    access_token = request.data['originalDetectIntentRequest']['payload']['user']
    if 'accessToken' in access_token:
        access_token = access_token['accessToken']
        profile_token = Token.objects.get(key=access_token)
        user = profile_token.user
        profile = Profile.objects.get(user=user)
    else:
        access_token = None
    best_transport = BestTransData.objects.get(email="kontakt@besttransport.com.pl")

    if access_token:
        order = Order.objects.create(customer=profile, email=profile.email, phone_number=profile.phone_number,
                                     performer=best_transport, price=parameters["my_price"])
        if "my_remarks" in parameters:
            order.remarks = parameters["my_remarks"]
            order.save()
    else:
        price = re.search(r"\d+", parameters["my_price"]).group()
        order = Order.objects.create(email=parameters["Email"], phone_number=parameters["telephone-number"],
                                     performer=best_transport, price=parameters["my_price"])
        if "my_remarks" in parameters:
            order.remarks = parameters["my_remarks"]
            order.save()

    loadings_keys = list()
    keys = list(parameters)
    for item in keys:
        if "loading" in item:
            loadings_keys.append(item)

    number_of_loading_dates = 0
    for item in loadings_keys:
        if "date" in item:
            number_of_loading_dates += 1

    for i in range(0, number_of_loading_dates):
        loading_place = SimpleAddress.objects.create(street=parameters["my_loading_street{}".format(i)],
                                                     post_code=parameters["my_loading_post_code{}".format(i)],
                                                     post_place=parameters["my_loading_post_place{}".format(i)])

        year = parameters["my_date_loading{}".format(i)][0:4]
        month = parameters["my_date_loading{}".format(i)][5:7]
        day = parameters["my_date_loading{}".format(i)][8:10]
        load_date = datetime.datetime(int(year), int(month), int(day))
        cargo = Cargo.objects.create(pallets_number=int(parameters["my_number_loading{}".format(i)]))

        loading_place_date = ExtendAddress.objects.create(date=load_date,
                                                          hour=parameters["my_time_loading{}".format(i)],
                                                          place=loading_place,
                                                          palette_number=cargo)
        OrdersLoadingPlaces.objects.create(order=order, loading_place=loading_place_date)

    destinations_keys = list()
    keys = list(parameters)
    for item in keys:
        if "destination" in item:
            destinations_keys.append(item)

    number_of_destination_dates = 0
    for item in destinations_keys:
        if "date" in item:
            number_of_destination_dates += 1

    for i in range(0, number_of_destination_dates):
        destination_place = SimpleAddress.objects.create(street=parameters["my_destination_street{}".format(i)],
                                                         post_code=parameters["my_destination_post_code{}".format(i)],
                                                         post_place=parameters["my_destination_post_place{}".format(i)])

        year = parameters["my_date_destination{}".format(i)][0:4]
        month = parameters["my_date_destination{}".format(i)][5:7]
        day = parameters["my_date_destination{}".format(i)][8:10]
        destination_date = datetime.datetime(int(year), int(month), int(day))
        cargo = Cargo.objects.create(pallets_number=int(parameters["my_number_loading{}".format(i)]))

        destination_place_date = ExtendAddress.objects.create(date=destination_date,
                                                              hour=parameters["my_time_destination{}".format(i)],
                                                              place=destination_place,
                                                              palette_number=cargo)
        OrdersDestinationPlaces.objects.create(order=order, destination_place=destination_place_date)

    return order.pk


def create_order_yes(request):
    """
    Creates new order from data from context
    :param request: request from "Create order - yes" Dialogflow intent
    :return: Json with information about created order and question what user want to do next
    """
    parameters_from_text = add_parameters_to_context(request, "creating_order_final")
    order_id = creating_order(request, parameters_from_text)

    with open('api/response.json') as json_file:
        response = json.load(json_file)

    part_to_modify = response['payload']['google']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Twoje zlecenie zostało zapisane. Id utworzonego zlecenia to {}".format(order_id)
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Twoje zlecenie zostało zapisane. Id utworzonego zlecenia to {}".format(order_id)
        part_to_modify['richResponse']['suggestions'] = [{"title": "Oferty"}, {"title": "Zlecenia"},
                                                         {"title": "Zapytania"},
                                                         {"title": "Konto"}, {"title": "Inne"}]
    elif request.data['queryResult']['languageCode'] == 'en':
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'textToSpeech'] = "Your order has been saved. The created order's id is {}".format(order_id)
        part_to_modify['richResponse']['items'][0]['simpleResponse'][
            'displayText'] = "Your order has been saved. The created order's id is {}".format(order_id)
        part_to_modify['richResponse']['suggestions'] = [{"title": "Offers"}, {"title": "Orders"},
                                                         {"title": "Inquiries"},
                                                         {"title": "Account"}, {"title": "Others"}]

    response['payload']['google'] = part_to_modify
    return response

