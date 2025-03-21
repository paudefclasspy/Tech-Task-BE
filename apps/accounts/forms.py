from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    # extending the basic user form
    # porque siempre necesitamos más campos 😅
    
    # making email required - no more fake emails!
    # marketing team will love this 📧
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        # these are the fields we actually care about
        # keep it simple, nobody reads the profile anyway 🤷‍♂️
        fields = ('username', 'email', 'password1', 'password2')
