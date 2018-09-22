from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .models import Profile
from django.http import HttpResponse
from .forms import ProfileForm, RegistrationForm
from django.contrib.auth.decorators import login_required

def home(request):
	if request.user.is_authenticated:
		return redirect('colleges:search')
	return redirect('login/')

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


def profile(request):
	if request.user.is_authenticated:
		user = request.user
		profile = Profile.objects.get(user = user)
		return render(request, 'sign_in/profile.html', {'profile': profile})
	return redirect('login/')


@login_required(login_url = 'login/')
def update(request):
	profile = Profile.objects.get(user = request.user)
	if request.method == 'POST':

		new_score = request.POST.get('score')
		new_cgpa = request.POST.get('cgpa')

		if (int)(new_score) > 340 or (int)(new_cgpa) > 10:
			return render(request, 'sign_in/update.html')

		profile.gre = new_score
		profile.cgpa = new_cgpa
		profile.save()
		return redirect('sign_in:profile')
	return render(request, 'sign_in/update.html')