from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Profile
from django.http import HttpResponse
from .forms import ProfileForm, RegistrationForm

def home(request):
	return HttpResponse('<h1>Home</h1>')

def register(request):
	if request.method == "POST":

		user_form = RegistrationForm(request.POST)
		profile_form = ProfileForm(request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			username = user_form.cleaned_data.get('username')
			raw_password = user_form.cleaned_data.get('password')

			profile = profile_form.save(commit = False)
			profile.user = user
			profile.save()

			login(request, authenticate(username = username, password = raw_password))
			return redirect('/')
	else:
		user_form = RegistrationForm()
		profile_form = ProfileForm()
	return render(request, 'sign_in/register.html', {'user_form': user_form, 'profile_form': profile_form})