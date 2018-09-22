import django_filters
from .models import College


class CollegeFilter(django_filters.FilterSet):
	class Meta:
		model = College
		fields = ['average_cost',]