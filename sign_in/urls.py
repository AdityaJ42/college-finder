from django.conf.urls import url
from . import views


urlpatterns = [
				url(r'^register/$', views.register, name = 'register'),
				url(r'^profile/$', views.profile, name = 'profile'),
				url(r'^update/$', views.update, name = 'update'),]