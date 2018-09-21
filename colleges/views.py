from django.shortcuts import render, redirect
from os import listdir
from os.path import isfile, join
import pickle
from sign_in.models import Profile
from django.http import HttpResponse
from .models import College
from .forms import CollegeForm


def predictor(student):
	print(student)
	to_test = student
	mypath = '/home/aditya/Desktop/django/college_finder/colleges/ml/'
	all_files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
	colleges = []

	for file in all_files:
		loaded_model = pickle.load(open(mypath + file, 'rb'))
		result = loaded_model.predict(to_test)

		if (int)(0.5 * result[0] + 0.5) >= 1:
			name = ''
			i = 0
			while file[i] != '.':
				name += file[i]
				i += 1
			colleges.append(name)
	return colleges


def checker(request):
	if request.user.is_authenticated:
		user = request.user
		profile = Profile.objects.get(user = user)
		possible_colleges = predictor([[profile.gre, profile.cgpa]])
		college_list = []
		for college in possible_colleges:
			print(college)
			college_details = College.objects.get(name = college)
			college_list.append(college_details)
		return render(request, 'colleges/college_list.html', {'college_list': college_list})
	else:
		return redirect('/login/')


def add_college(request):
	if request.user.is_authenticated and request.user.is_superuser:
		if request.method == "POST":
			college_form = CollegeForm(request.POST)

			if college_form.is_valid():
				college_form.save()
				return redirect('/')
		else:
			college_form = CollegeForm()
		return render(request, 'colleges/add.html', {'college_form': college_form})
