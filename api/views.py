from rest_framework.decorators import api_view
from api.dialogflow_intents import *
from django.http import JsonResponse
from api.forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse


@api_view(['POST'])
def google_actions(request):
    if request.data['queryResult']['intent']['displayName']:
        output = intents[request.data['queryResult']['intent']['displayName']](request)
    return JsonResponse(output)


def sign_in(request):
    """
    Endpoint for sign in
    :param request: POST request with data to log
    :return: website for sign in or redirect to google assistant
    """
    form = LoginForm(request.POST or None)
    state = request.GET.get('state', " ")
    sign_up_url = "https://best-transport.herokuapp.com/api/sign_up/?state={}".format(state)

    if form.is_valid():
        id = request.GET.get('client_id', "")
        url = request.GET.get('redirect_uri', "")
        if id == 'GoogleInc' and url == 'https://oauth-redirect.googleusercontent.com/r/best-trans-968c8':
            if User.objects.filter(username=form.cleaned_data['username']).count() > 0:
                user = User.objects.get(username=form.cleaned_data['username'])
                matchcheck = check_password(form.cleaned_data['password'], user.password)
                if matchcheck:
                    token = Token.objects.get(user=user)
                    return_path = 'https://oauth-redirect.googleusercontent.com/r/best-trans-968c8#access_token=' \
                                  '{}&token_type=bearer&state={}'.format(str(token), state)
                    return redirect(return_path)
    return render(request, 'login.html', {'form': form, 'sign_up_url': sign_up_url})


def sign_up(request):
    """
    Endpoint for sign up. Create new account
    :param request: POST request with data to create new account
    :return: website for sign up or redirect to google assistant
    """
    form = SingUpForm(request.POST or None)
    state = request.GET.get('state', " ")

    if form.is_valid():
        user = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        token = Token.objects.create(user=user)
        if form.cleaned_data.get("residence_place", None) and form.cleaned_data.get("street", None) and form.cleaned_data.get("post_code", "") and \
                form.cleaned_data.get("post_place", None) and form.cleaned_data.get("country", None):
            profile = Profile.objects.create(user=user, name=form.cleaned_data["name"], surname=form.cleaned_data["surname"],
                                             email=form.cleaned_data["email"], phone_number=form.cleaned_data["phone_number"],
                                             tax_number=form.cleaned_data.get('profile_tax_number', None),
                                             address=SimpleAddress.objects.create(place_name=form.cleaned_data["residence_place"],
                                                                                  street=form.cleaned_data["street"],
                                                                                  post_code=form.cleaned_data["post_code"],
                                                                                  post_place=form.cleaned_data["post_place"],
                                                                                  country=form.cleaned_data["country"]))
        else:
            profile = Profile.objects.create(user=user, name=form.cleaned_data["name"],
                                             surname=form.cleaned_data["surname"],
                                             email=form.cleaned_data["email"],
                                             phone_number=form.cleaned_data["phone_number"],
                                             tax_number=form.cleaned_data.get('profile_tax_number', None))

        if form.cleaned_data.get("company_tax_number", None) and form.cleaned_data.get("company_email", None) and \
                form.cleaned_data.get("company_phone_number", None) and form.cleaned_data.get("company_name", None) and \
                form.cleaned_data.get("company_street", None) and form.cleaned_data.get("company_post_code_", None) and \
                form.cleaned_data.get("company_post_place", None) and form.cleaned_data.get("company_country", None):
            company = Company.objects.create(tax_number=form.cleaned_data["company_tax_number"], email=
                                             form.cleaned_data["company_email"], phone_number=form.cleaned_data["company_phone_number"],
                                             address=SimpleAddress.objects.create(place_name=form.cleaned_data["company_name"],
                                                                          street=form.cleaned_data["company_street"],
                                                                          post_code=form.cleaned_data["company_post_code_"],
                                                                          post_place=form.cleaned_data["company_post_place"],
                                                                          country=form.cleaned_data["company_country"]))
            profile.company = company

        elif form.cleaned_data.get("company_tax_number", None) and form.cleaned_data.get("company_email", None) and \
                form.cleaned_data.get("company_phone_number", None):
            company = Company.objects.create(tax_number=form.cleaned_data["company_tax_number"], email=form.cleaned_data["company_email"],
                                             phone_number=form.cleaned_data["company_phone_number"])
            profile.company = company

        return_path = 'https://oauth-redirect.googleusercontent.com/r/best-trans-968c8#access_token={}&token_type=' \
                      'bearer&state={}'.format(str(token), state)
        return redirect(return_path)

    return render(request, 'sign_up.html', {'form': form})


def token(request):
    pass
