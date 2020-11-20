# Create your views here.
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render

from .forms import SignUpForm


def signup_view(request):
    """
    This view generates view for sign up form.
    """
    form = SignUpForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = BaseUserManager().make_random_password()

        send_mail(
            f"Registration Electronic library",
            f"Hello!\nYour login: {username}, password: {password}\nUse it to registrate in platform\n",
            settings.EMAIL_HOST_USER,
            [email, ]
        )

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        print("User:", username, ", email:", email, ", password:", password)
        # confirmation page redirect
        # return home_view(request)
        return render(request, 'registration/signup_successful.html')
    return render(request, 'registration/signup.html', {'form': form})
