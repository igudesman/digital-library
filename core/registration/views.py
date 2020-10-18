from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from django.conf import settings
from search.views import get_material_queryset
from search.models import Material
from operator import attrgetter


def home_view(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)

    if query == "":
        print("Empty request")
        material_list = sorted(Material.objects.all(), key=attrgetter('date_publication'), reverse=True)
    else:
        material_list = sorted(get_material_queryset(query), key=attrgetter('date_publication'), reverse=True)
    context['material_list'] = material_list
    return render(request, 'material_list.html', context)


def signup_view(request):
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

        return home_view(request)
    return render(request, 'signup.html', {'form': form})
