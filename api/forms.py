from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class SingUpForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password')
    name = forms.CharField(label='Name')
    surname = forms.CharField(label='Surname')
    email = forms.EmailField(label='email')
    phone_number = forms.CharField(label='Phone number')
    profile_tax_number = forms.CharField(label='Your tax number', required=False)
    residence_place = forms.CharField(label='Residence place', required=False)
    street = forms.CharField(label='Street', required=False)
    post_code = forms.CharField(label='Post code', required=False)
    post_place = forms.CharField(label='Post place', required=False)
    country = forms.CharField(label='Country', required=False)
    company_tax_number = forms.CharField(label='Company tax number', required=False)
    company_email = forms.EmailField(label='Company email', required=False)
    company_phone_number = forms.CharField(label='Company phone number', required=False)
    company_name = forms.CharField(label='Company name', required=False)
    company_street = forms.CharField(label='Company street', required=False)
    company_post_code_ = forms.CharField(label='Company post code', required=False)
    company_post_place = forms.CharField(label='Post place ', required=False)
    company_country = forms.CharField(label='Company country', required=False)
