from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Profile(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	name = models.CharField(max_length = 100)
	gre = models.IntegerField(validators = [MinValueValidator(0), MaxValueValidator(340)])
	cgpa = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(10)])


	def __str__(self):
		return self.name