from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import model_info, model_requests, model_assign

class form_user(forms.ModelForm):
    class Meta():
        model = User
        fields = ('first_name','last_name','email','password')
        widgets = {
        'first_name' : forms.TextInput(attrs={'class':'form-control'}),
        'last_name' : forms.TextInput(attrs={'class':'form-control'}),
        'email' : forms.TextInput(attrs={'class':'form-control'}),
        'password' : forms.PasswordInput(attrs={'class':'form-control'}),
        }
class form_info(forms.ModelForm):
    # request_type = forms.ChoiceField(label='Request Type',choices=model_requests, widget=forms.RadioSelect())
    request_type = forms.ModelChoiceField(queryset= model_requests.objects, widget=forms.RadioSelect)
    request_desc = forms.SlugField(label='Description')
    request_ccode = forms.IntegerField(label='Country Code')
    request_number = forms.IntegerField(label='Mobile Number')
    class Meta():
        model = model_info
        fields = ['request_type','request_desc','request_city','request_states','request_pincode','request_ccode','request_number']

class form_details(forms.ModelForm):
    class Meta():
        model = model_assign
        fields = ['request_status','request_remark']
