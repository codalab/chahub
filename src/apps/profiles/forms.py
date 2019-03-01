from django.contrib.auth.forms import UserCreationForm, UsernameField

from django.contrib.auth import get_user_model
from django.forms import EmailField

User = get_user_model()


class ChahubCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {
            'username': UsernameField,
            'email': EmailField
        }
