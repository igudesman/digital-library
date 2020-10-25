from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from validate_email import validate_email

class SignUpForm(forms.Form):
    """
    From for signing up (registrating) with checks username and email
    """
    username = forms.CharField(max_length=100, help_text='Nickname')
    email = forms.EmailField(max_length=150, help_text='Email')

    # class Meta:
    #     model = User
    #     fields = ('name', 'email',)

    def clean_username(self):
        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"Username: {username} is already in use.")

        else:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        # TODO(допилить проверку на сущ. почты)
        # if not validate_email(email):
        #     raise forms.ValidationError(f"{email} is not exist.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"{email} is already in use.")

        elif '@innopolis.ru' not in email and '@innopolis.university' not in email:
            raise forms.ValidationError(f"{email} is not an innopolis univesity email.")

        else:
            return email
