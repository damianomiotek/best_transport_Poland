import json


def default_welcome_intent(request):
    """
    Display welcome with activities to choose
    :param request: POST request from "Default Welcome Intent" dialogflow intent
    :return: Json with welcome text and welcome menu
    """
    speech_text_pl = "Witaj!!! Jestem Twoim asystentem best transport Polska. Pomogę Ci załatwić różne sprawy w naszej " \
                     "firmie. W czym mogę Ci pomóc?"
    display_text_pl = "Witaj!!! Jestem asystentem best transport Polska. W czym mogę Ci pomóc?"
    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                      {"title": "Inne"}]
    speech_text_en = "Welcome!!! I am your best transport Poland assistant. I will help you get things done in our company. " \
                     "What can I help you now?"
    display_text_en = "Welcome!!! I am best transport Poland assistant. What can I help you?"
    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                      {"title": "Others"}]

    with open('api/response.json') as json_file:
        welcome = json.load(json_file)

    part_to_modify = welcome['payload']['google']['richResponse']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
        part_to_modify['suggestions'] = suggestions_pl
    else:
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
        part_to_modify['suggestions'] = suggestions_en

    welcome['payload']['google']['richResponse'] = part_to_modify
    return welcome


def others(request):
    """
    Display others menu with activities to choose
    :param request: POST request from "Others" dialogflow intent
    :return: Json with others menu
    """
    speech_text_pl = "Wybierz jedną z poniższych opcji, która Cię interesuje"
    display_text_pl = "Która z poniższych opcji Cię interesuje?"
    suggestions_pl = [{"title": "Kontakt"}, {"title": "O firmie"}, {"title": "Adres"}, {"title": "Tabor samochodowy"}]

    speech_text_en = "Choose one of the options below that interest you"
    display_text_en = "Choose one of the options below that interest you"
    suggestions_en = [{"title": "Contact"}, {"title": "About us"}, {"title": "Address"}, {"title": "Car fleet"}]

    with open('api/response.json') as json_file:
        menu_others = json.load(json_file)

    part_to_modify = menu_others['payload']['google']['richResponse']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
        part_to_modify['suggestions'] = suggestions_pl
    else:
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
        part_to_modify['suggestions'] = suggestions_en

    menu_others['payload']['google']['richResponse'] = part_to_modify
    return menu_others


def contact(request):
    """
    Create Json response about the contact to the company.
    :param request: POST request from "Contact" dialogflow intent
    :return: Json response that contains spoken and display prompt and also basic card about contact to company
    """
    speech_text_pl = "Dane adresowe Best Transport Polska S.A. W Czym mogę Ci jeszcze pomóc?"
    display_text_pl = "Dane adresowe Best Transport Polska S.A. W Czym mogę Ci jeszcze pomóc?"
    basic_card_pl = {
        "basicCard": {
            "title": "Kontakt",
            "formattedText": "___ul.___ Piotrkowska 1 90-000 Łódź  \n___tel.___ 111222333  \n___e-mail___ kontakt.besttransport@com.pl  \n"
                             "___Otwarte:___  \npon.- pt. 7.00 - 19.00  \nsob. 7.00 - 16.00",
            "image": {
                "url": "https://polskazachwyca.pl/wp-content/uploads/2017/10/%C5%82%C3%B3d%C5%BA-piotrkowska-shutterstock_441654322.jpg",
                "accessibilityText": "Kontakt"
              },
            "imageDisplayOptions": "CROPPED"
            }
          }
    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                      {"title": "Inne"}]

    speech_text_en = "Address details of Best Transport Poland S.A. How can I help you?"
    display_text_en = "Address details of Best Transport Poland S.A. How can I help you?"
    basic_card_en = {
        "basicCard": {
            "title": "Contact",
            "formattedText": "__st.__ Piotrkowska 1 90-000 Lodz  \n__tel.no.__ +48 111222333  \n__e-mail__ kontakt.besttransport@com.pl  \n"
                             "__Open:__  \nmon.- fri. 7.00 - 19.00  \nsat. 7.00 - 16.00",
            "image": {
                "url": "https://polskazachwyca.pl/wp-content/uploads/2017/10/%C5%82%C3%B3d%C5%BA-piotrkowska-shutterstock_441654322.jpg",
                "accessibilityText": "Contact"
            },
            "imageDisplayOptions": "CROPPED"
        }
    }
    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                      {"title": "Others"}]

    with open('api/response.json') as json_file:
        contact = json.load(json_file)

    part_to_modify = contact['payload']['google']['richResponse']

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

    contact['payload']['google']['richResponse'] = part_to_modify
    return contact


def about_us(request):
    """
    Create general informations about company
    :param request: POST request from "About us" dialogflow intent
    :return: Json with general info about company
    """
    speech_text_pl = "Jesteśmy w Polsce liderem wśród firm transportowych średniej wielkości. Rozwijamy się niezwykle szybko" \
                     " i stale zwiększamy ilość naszych klientów. Oferujemy usługi transportu międzynarodowego ciągnikami siodłowymi. " \
                     "Nasz tabor samochodowy liczy obecnie ponad 80 samochodów ciężarowych. Posiadamy uprawnienia do przewozu" \
                     " materiałów spożywczych i niebezpiecznych. Jeśli chcesz dowiedzieć się więcej o naszej flocie, wybierz poniższą opcję" \
                     " Tabor samochodowy"
    display_text_pl = "Jesteśmy w Polsce liderem wśród firm transportowych średniej wielkości. Rozwijamy się niezwykle szybko" \
                     " i stale zwiększamy ilość naszych klientów. Oferujemy usługi transportu międzynarodowego ciągnikami siodłowymi. " \
                     "Nasz tabor samochodowy liczy obecnie 80 samochodów ciężarowych. Posiadamy uprawnienia do przewozu" \
                     " materiałów spożywczych i niebezpiecznych. Jeśli chcesz dowiedzieć się więcej o naszej flocie, wybierz poniższą opcję" \
                     " Tabor samochodowy"
    suggestions_pl = [{"title": "Tabor samochodowy"}, {"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"},
                      {"title": "Konto"}, {"title": "Inne"}]

    speech_text_en = "We are a leader among medium-sized transport companies in Poland. We are developing extremely fast" \
                     " and we are constantly increasing the number of our clients. We offer international transport " \
                     "services our truck tractors. Our fleet currently has over 80 trucks. We have the authority to transport " \
                     "food and dangerous materials. If you want to learn more about our fleet, choose the following " \
                     "option Car fleet"
    display_text_en = "We are a leader among medium-sized transport companies in Poland. We are developing extremely fast" \
                     " and we are constantly increasing the number of our clients. We offer international transport " \
                     "services our truck tractors. Our fleet currently has 80 trucks. We have the authority to transport " \
                     "food and dangerous materials. If you want to learn more about our fleet, choose the following " \
                     "option Car fleet"
    suggestions_en = [{"title": "Car fleet"}, {"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"},
                      {"title": "Account"}, {"title": "Others"}]

    with open('api/response.json') as json_file:
        about_us = json.load(json_file)

    part_to_modify = about_us['payload']['google']['richResponse']

    if request.data['queryResult']['languageCode'] == 'pl':
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_pl
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_pl
        part_to_modify['suggestions'] = suggestions_pl
    else:
        part_to_modify['items'][0]['simpleResponse']['textToSpeech'] = speech_text_en
        part_to_modify['items'][0]['simpleResponse']['displayText'] = display_text_en
        part_to_modify['suggestions'] = suggestions_en

    about_us['payload']['google']['richResponse'] = part_to_modify
    return about_us


def address(request):
    """
    Create Json response with address data
    :param request: POST request from "Address" dialogflow intent
    :return: Json response that contains spoken and display prompt and also basic card about company address
    """
    speech_text_pl = "Oto adres Best Transport Polska S.A. W Czym mogę Ci jeszcze pomóc"
    display_text_pl = "Oto adres Best Transport Polska S.A. W Czym mogę Ci jeszcze pomóc"
    basic_card_pl = {
        "basicCard": {
            "title": "Adres",
            "formattedText": "___ul.___ Piotrkowska 1  \n90-000 Łódź  \n"
                             "___Otwarte:___  \npon.- pt. 7.00 - 19.00  \nsob. 7.00 - 16.00",
            "image": {
                "url": "https://s23.flog.pl/media/foto/11989150_magiczna-ul-piotrkowska-w-lodzi-.jpg",
                "accessibilityText": "Adres"
            },
            "imageDisplayOptions": "CROPPED"
        }
    }
    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                      {"title": "Inne"}]

    speech_text_en = "Here is the address of Best Transport Poland S.A. What can I help you with?"
    display_text_en = "Here is the address of Best Transport Poland S.A. What can I help you with?"
    basic_card_en = {
        "basicCard": {
            "title": "Address",
            "formattedText": "__st.__ Piotrkowska 1  \n90-000 Lodz  \n"
                             "__Open:__  \nmon.- fri. 7.00 - 19.00  \nsat. 7.00 - 16.00",
            "image": {
                "url": "https://s23.flog.pl/media/foto/11989150_magiczna-ul-piotrkowska-w-lodzi-.jpg",
                "accessibilityText": "Address"
            },
            "imageDisplayOptions": "CROPPED"
        }
    }
    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                      {"title": "Others"}]

    with open('api/response.json') as json_file:
        address = json.load(json_file)

    part_to_modify = address['payload']['google']['richResponse']

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

    address['payload']['google']['richResponse'] = part_to_modify
    return address


def car_fleet(request):
    """
    Create Json response with the car fleet of company
    :param request: POST request from "Car flat" dialogflow intent about car fleet
    :return: Json response that contains spoken and display prompt and also basic card about car fleet
    """
    speech_text_pl = "Oto nasz tabor samochodowy. Powiedz mi w czym mogę Ci jeszcze pomóc?"
    display_text_pl = "Tabor samochodowy. Powiedz mi w czym mogę Ci jeszcze pomóc?"
    basic_card_pl = {
        "basicCard": {
            "title": "Nasz sprzęt",
            "formattedText": "__Samochody ciężarowe:__  \nScania - 72 szt.  \nMercedes - 8 szt.  \nVolvo - 5 szt.  \n"
                             "__Naczepy:__  \nNaczepy uniwersalne - 54 szt.  \nCysterny - 12 szt.  \nChłodnie - 9 szt.  \n"
                             "Naczepy podkontenerowe - 10 szt.",
            "image": {
                "url": "https://bi.im-g.pl/im/0b/f5/12/z19878923Q,Europejskie-koncerny-motoryzacyjne-od-wielu-lat-pr.jpg",
                "accessibilityText": "Tabot samochodowy"
            },
            "imageDisplayOptions": "CROPPED"
        }
    }
    suggestions_pl = [{"title": "Oferty"}, {"title": "Zlecenia"}, {"title": "Zapytania"}, {"title": "Konto"},
                      {"title": "Inne"}]

    speech_text_en = "Here's our car fleet. Tell me how can I help you?"
    display_text_en = "Car fleet. Tell me how can I help you?"
    basic_card_en = {
        "basicCard": {
            "title": "Our equipment",
            "formattedText": "__Trucks:__  \nScania - 72 pcs.  \nMercedes - 8 pcs.  \nVolvo - 5 pcs.  \n"
                             "__Semitrailers:__  \nUniversal semitrailers - 54 pcs.  \nTankers - 12 pcs.  \n"
                             "Coolings - 9 pcs.  \nContainer semitrailers - 10 pcs.",
            "image": {
                "url": "https://bi.im-g.pl/im/0b/f5/12/z19878923Q,Europejskie-koncerny-motoryzacyjne-od-wielu-lat-pr.jpg",
                "accessibilityText": "Car fleet"
            },
            "imageDisplayOptions": "CROPPED"
        }
    }
    suggestions_en = [{"title": "Offers"}, {"title": "Orders"}, {"title": "Inquiries"}, {"title": "Account"},
                      {"title": "Others"}]

    with open('api/response.json') as json_file:
        car_fleet = json.load(json_file)

    part_to_modify = car_fleet['payload']['google']['richResponse']

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

    car_fleet['payload']['google']['richResponse'] = part_to_modify
    return car_fleet
