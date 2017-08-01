from django.contrib import messages
from django.db import transaction
from django.shortcuts import *
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import *
from .models import *


@csrf_exempt
def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():

                if User.objects.filter(username=form.cleaned_data['username']).exists():
                    raise ValidationError("Username already used choose other")
                form_data = form.cleaned_data
                if form_data['password'] != form_data['password_repeat']:
                    form._errors["password"] = ["Password do not match"]
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],

                )
                authenticate(username=user.username, password=user.password)
                login(request, user)
                return HttpResponseRedirect('/update_profile')
            else:
                raise Exception
        else:
            form = SignupForm()
            variables = {'form': form}

            return render_to_response(
                'signup.html',
                variables
            )
    else:
        return HttpResponseRedirect('/update_profile')


@login_required(login_url="login/")
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            profile_form.save()
            messages.success(request, ('Your profile was successfully updated! Press Home on navbar to proceed'))
            return redirect('update_profile')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form}
                  )


@login_required(login_url="login/")
def home(request):
    players = User.objects.filter(profile__type__exact='P')
    return render(request, "dashboard.html", {'user': players})


@login_required(login_url="login/")
def transact_money(request):
    if request.user.profile.type == 'A':
        if request.method == 'POST':
            form = TransactionForm(request.POST)
            if form.is_valid():
                user_money = request.user.profile.money
                giving_money = form.cleaned_data['money']
                player = form.cleaned_data['send_to']
                print(player)
                if user_money >= giving_money and giving_money >= 0:
                    request.user.profile.money -= giving_money
                    print(user_money, request.user.profile.money)
                    request.user.profile.save()

                    player.profile.money += giving_money
                    player.profile.save()
                    return HttpResponseRedirect('/scoreboard')
                else:
                    messages.error(request, ('Please enter a valid amount above.'))
                    transaction_form = TransactionForm
                    return render(request, 'transaction.html', {'transaction_form': transaction_form})
            else:
                raise Exception
        else:
            transaction_form = TransactionForm
            return render(request, 'transaction.html', {'transaction_form': transaction_form})
    else:
        messages.error(request, ('You are not allowed please re-register as audience'))
        transaction_form = TransactionForm
        return render(request, 'transaction.html', {'transaction_form': transaction_form})


def scoreboard(request):
    players = User.objects.filter(profile__type__exact='P')
    return render(request, 'scoreboard.html', {'players': players})


@login_required(login_url="login/")
def logout_view(request):
    logout(request)
    return render(request, "logout.html")
