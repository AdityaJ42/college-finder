from django.conf.urls import url
from . import views


urlpatterns = [
				url(r'^possibles/$', views.checker, name = 'check'),
				url(r'^add/$', views.add_college, name = 'add'),]