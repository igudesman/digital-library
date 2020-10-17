from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import  User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.conf import settings

def home_view(request):
    return render(request, 'index.html')


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = BaseUserManager().make_random_password()

        try:
            send_mail(
                f"Registration Electronic library",
                f"Hello!\nYour login: {username}, password: {password}\nUse it to registrate in platform\n",
                settings.EMAIL_HOST_USER,
                [email,]
            )
        except BaseException:
            print("Упс, почту мою залочил майл!")

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        print("User:", username, ", email:", email, ", password:", password)

        return home_view(request)
    return render(request, 'signup.html', {'form': form})
