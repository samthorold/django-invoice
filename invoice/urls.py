from django.conf.urls import url

from . import views


app_name = 'invoice'

urlpatterns = [
	url(r'^$', views.invoice_list, name='invoice_list'),
	url(r'^new/$', views.invoice_new, name='invoice_new'),
	url(r'^search/$', views.invoice_search, name='invoice_search'),
	url(r'^(?P<pk>[0-9]+)/$', views.invoice_detail, name='invoice_detail'),
	url(r'^(?P<pk>[0-9]+)/edit/$', views.invoice_edit, name='invoice_edit'),
	url(r'^(?P<pk>[0-9]+)/delete/$', views.invoice_delete, name='invoice_delete'),

	url(r'^(?P<invoice_pk>[0-9]+)/invoice_line_new/$', views.invoice_line_new, name='invoice_line_new'),
	url(r'^lines/(?P<pk>[0-9]+)/send/$', views.invoice_line_send_invoice_now, name='invoice_line_send_invoice_now'),
	url(r'^lines/(?P<pk>[0-9]+)/edit/$', views.invoice_line_edit, name='invoice_line_edit'),
	url(r'^lines/(?P<pk>[0-9]+)/delete/$', views.invoice_line_delete, name='invoice_line_delete'),

	url(r'^worktypes/$', views.worktype_list, name='worktype_list'),
	url(r'^worktypes/new/$', views.worktype_new, name='worktype_new'),
	url(r'^worktypes/search/$', views.worktype_search, name='worktype_search'),
	url(r'^worktypes/(?P<pk>[0-9]+)/$', views.worktype_detail, name='worktype_detail'),
	url(r'^worktypes/(?P<pk>[0-9]+)/edit/$', views.worktype_edit, name='worktype_edit'),
	url(r'^worktypes/(?P<pk>[0-9]+)/delete/$', views.worktype_delete, name='worktype_delete'),

	url(r'^payments/$', views.payment_list, name='payment_list'),
	url(r'^(?P<invoice_pk>[0-9]+)/payment_new/$', views.payment_new, name='payment_new'),
	url(r'^payments/search/$', views.payment_search, name='payment_search'),
	url(r'^payments/(?P<pk>[0-9]+)/edit/$', views.payment_edit, name='payment_edit'),
	url(r'^payments/(?P<pk>[0-9]+)/delete/$', views.payment_delete, name='payment_delete'),
]