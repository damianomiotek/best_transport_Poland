from api.account import *
from api.inquiries import *
from api.orders import *


def values_of_lists(request):
    """
    Call function according to selected list item
    :param request: POST request from "Values of lists" dialogflow intent
    :return: Json returned by called function
    """
    title_from_lists = request.data['originalDetectIntentRequest']['payload']['inputs'][0]['arguments'][0]['textValue']
    language = request.data['queryResult']['languageCode']

    if language == 'pl':
        for key, value in titles_from_lists_pl.items():
            response = re.search(key, title_from_lists)
            if response:
                return titles_from_lists_pl[key](request)
        return titles_from_lists_pl[title_from_lists](request)
    else:
        for key, value in titles_from_lists_en.items():
            response = re.search(key, title_from_lists)
            if response:
                return titles_from_lists_en[key](request)
        return titles_from_lists_en[title_from_lists](request)


titles_from_lists_pl = {
    "Zaloguj": access_google_account,
    "Zarejestruj się": access_google_account,
    "Usuń konto": delete_account,
    "Wyświetl jedną konkretną informację o użytkowniku": one_user_information,
    "Imie": tell_name,
    "Nazwisko": tell_surname,
    "Nazwa użytkownika": tell_username,
    "Email": tell_email,
    "Numer telefonu": tell_phone_number,
    "Numer podatnika": tell_tax_number,
    "Miejsce zamieszkania": tell_place_name,
    "Ulica": tell_street,
    "Kod pocztowy": tell_post_code,
    "Poczta": tell_post_place,
    "Kraj": tell_country,
    "Numer podatnika dla firmy": tell_company_tax_number,
    "Email firmy": tell_company_email,
    "Numer telefonu do firmy": tell_company_phone_number,
    "Nazwa firmy": tell_company_name,
    "Ulica firmy": tell_company_street,
    "Kod pocztowy firmy": tell_company_post_code,
    "Poczta firmy": tell_company_post_place,
    "Kraj firmy": tell_company_country,
    "Wyświetl wszystkie dane konta": tell_all_account_information,
    "Zmień dane konta": ask_change_account_settings,
    "Zmień jedno ustawienie konta": change_one_account_information,
    "Zmien imie": change_user_name_list,
    "Zmien nazwisko": change_user_surname_list,
    "Zmien nazwa użytkownika": change_user_username_list,
    "Przeglądaj oferty": browse_offers,
    "Wyszukaj oferty": ask_search_offers,
    "Wyszukaj ofertę po id": ask_search_offer_id,
    "Do kiedy jest ważna oferta": ask_until_when_offer_valid,
    "Wyszukaj zapytanie/odpowiedź": search_inquiry_response,
    "Tworzenie zapytania": create_inquiry,
    "Tworzenie zapytania do oferty/zamówienia": ask_creating_inquiry_for,
    "Czy są nieprzeczytane odpowiedzi": are_there_unread_responses,
    "Nieprzeczytane odpowiedzi": unread_responses,
    "Odpowiedzi do zapytania": ask_responses_for_inquiry,
    "Odpowiedzi do oferty/zamówienia": ask_search_response_for,
    "Odpowiedz": ask_create_response_to_admnin,
    "Przeglądaj aktualne zlecenia": browse_current_orders,
    "Historia zleceń": orders_history,
    "Zlecenie numer ": order_number,
    "Wyszukaj zlecenie": ask_search_orders,
    "Czy zlecenie zostało przyjęte do realizacji": ask_order_accepted,
    "Czy zlecenie zostało zrealizowane": ask_order_realised,
    "Usuń zlecenie": ask_remove_order,
    "Stwórz zlecenie": ask_create_order
}

titles_from_lists_en = {
    "Sign in": access_google_account,
    "Sign up": access_google_account,
    "Delete account": delete_account,
    "View one specific user information": one_user_information,
    "Name": tell_name,
    "Surname": tell_surname,
    "Username": tell_username,
    "Email": tell_email,
    "Phone number": tell_phone_number,
    "Tax number": tell_tax_number,
    "Place of residence": tell_place_name,
    "Street": tell_street,
    "Post code": tell_post_code,
    "Post Place": tell_post_place,
    "Country": tell_country,
    "Company tax number": tell_company_tax_number,
    "Email for company": tell_company_email,
    "Company phone number": tell_company_phone_number,
    "Company name": tell_company_name,
    "Company street": tell_company_street,
    "Company post code": tell_company_post_code,
    "Post city for company": tell_company_post_place,
    "Company country": tell_company_country,
    "View all account details": tell_all_account_information,
    "Change account details": ask_change_account_settings,
    "Change one account detail": change_one_account_information,
    "Change name": change_user_name_list,
    "Change surname": change_user_surname_list,
    "Change username": change_user_username_list,
    "Browse offers": browse_offers,
    "Search offers": ask_search_offers,
    "Search offer after id": ask_search_offer_id,
    "Until when is the offer valid": ask_until_when_offer_valid,
    "Search inquiry/answer": search_inquiry_response,
    "Create a inquiry": create_inquiry,
    "Creating a inquiry for an offer/order": ask_creating_inquiry_for,
    "Are there unread responses": are_there_unread_responses,
    "Unread responses": unread_responses,
    "Answers to the inquiry": ask_responses_for_inquiry,
    "Answers to the offer/order": ask_search_response_for,
    "Reply to admin": ask_create_response_to_admnin,
    "Browse current orders": browse_current_orders,
    "The history of orders": orders_history,
    "Order number ": order_number,
    "Search for the order": ask_search_orders,
    "Is the order accepted for execution": ask_order_accepted,
    "Has the order been executed": ask_order_realised,
    "Delete an order": ask_remove_order,
    "Create an order": ask_create_order
}