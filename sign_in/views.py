from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Profile
from .forms import ProfileForm, RegistrationForm


def register(request):
	if request.method == "POST":

		user_form = RegistrationForm(request.POST)
		profile_form = ProfileForm(request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			profile = profile_form.save()

			user.set_password(user.password)
			user.save()

			username = user_form.cleaned_data.get('username')
			raw_password = user_form.cleaned_data.get('password')

			profile.user = user
			login(request, authenticate(username = username, password = raw_password))
			return redirect('/')
	else:
		user_form = RegistrationForm()
		profile_form = ProfileForm()
	return redirect('/')