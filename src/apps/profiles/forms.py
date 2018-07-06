from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.http import HttpResponse
# from django.shortcuts import render
from django.shortcuts import render

from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


class ChahubCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}