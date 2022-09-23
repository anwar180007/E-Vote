from dataclasses import fields
from django import forms
from django.contrib.auth.forms import UsernameField, AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _ 
from . models import Voter_Registration, Nomination_list, Vote_Shedule

class VoterRegForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Voter_Registration
        fields = ['username', 'first_name', 'last_name', 'email', 'father_name', 'mother_name', 'gender', 'dob', 'village', 'post_office', 'upazilla', 'zilla', 'profile_pic']
        labels = {
            'username': 'Voter_ID',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'password1': 'Password',
            'password2': 'Password Confirm',
            'email': 'Email',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
            'village': forms.TextInput(attrs={'class': 'form-control'}),
            'post_office': forms.TextInput(attrs={'class': 'form-control'}),
            'upazilla': forms.TextInput(attrs={'class': 'form-control'}),
            'zilla': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    Voter_Id = forms.CharField(widget= forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip= False, widget= forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))

class Nomination_list_Form(forms.ModelForm):
    class Meta:
        model = Nomination_list
        fields = '__all__'
        widgets = {
            'candidate_name': forms.TextInput(attrs={'class': 'form-control'}),
            'icon_name': forms.TextInput(attrs={'class': 'form-control'}),
            'ballot_paper_img': forms.FileInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VoteSheduleForm(forms.ModelForm):
    class Meta:
        model = Vote_Shedule
        fields = '__all__'
        widgets = {
            'vote_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'datepicker'}),
        }