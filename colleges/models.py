from django.db import models


class College(models.Model):
	name = models.CharField(max_length = 200)
	average_cost = models.IntegerField()
	location = models.CharField(max_length = 70)
	website = models.CharField(max_length = 1000)

	def __str__(self):
		return self.name