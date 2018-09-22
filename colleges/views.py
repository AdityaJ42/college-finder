from django.shortcuts import render, redirect
from os import listdir
from os.path import isfile, join
import pickle
from sign_in.models import Profile
from django.http import HttpResponse
from .models import College
from .forms import CollegeForm


def predictor(student):
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


def checker(user):	
	profile = Profile.objects.get(user = user)
	possible_colleges = predictor([[profile.gre, profile.cgpa]])

	college_list = []

	for college in possible_colleges:
		college_details = College.objects.get(name = college)
		college_list.append(college_details)

	return college_list


def add_college(request):
	if request.user.is_authenticated and request.user.is_superuser:
		if request.method == "POST":
			college_form = CollegeForm(request.POST)

			if college_form.is_valid():
				college_form.save()
				return redirect('colleges:add')
		else:
			college_form = CollegeForm()
		return render(request, 'colleges/add.html', {'college_form': college_form})

def search(request):
	if request.user.is_authenticated:
		user = request.user
		colleges = checker(user)
		colleges_copy = []
		# print(len(colleges_copy))
		maxCost = request.POST.get('maxRange')
		# print(colleges_copy)
		if maxCost is not None:
			maxCost = (int)(maxCost)

			for college in colleges:
				# print(college.average_cost, maxCost, college)
				if college.average_cost <= maxCost:
					colleges_copy.append(college)
		else:
			colleges_copy = colleges
		print(colleges_copy)
		return render(request, 'colleges/college_list.html', {'colleges_copy': colleges_copy})