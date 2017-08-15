from django.conf.urls import url

from . import views


app_name = 'contacts'

urlpatterns = [
	url(r'^$', views.list_contacts, name='list_contacts'),
	url(r'^new/$', views.new_contact, name='new_contact'),
	url(r'^(?P<id>[0-9]+)/$', views.view_contact, name='view_contact'),
	url(r'^(?P<id>[0-9]+)/edit/$', views.edit_contact, name='edit_contact'),
	url(r'^(?P<id>[0-9]+)/delete/$', views.delete_contact, name='delete_contact'),
]