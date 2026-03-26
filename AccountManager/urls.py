from django.urls import path, re_path
from django.contrib import admin
import Software.views as views


urlpatterns = [
	path('', views.homepage, name="homepage"),
	
	## Display Entries
	path('agents/', views.agents, name="agents"),
	path('clients/', views.clients, name="clients"),
	path('invoices/', views.invoices, name="invoices"),
	path('products/', views.products, name="products"),
	path('payments/', views.payments, name="payments"),
	path('sizes/', views.sizes, name="sizes"),

	## Add Entries
	path('agents/new', views.new_agent, name="new_agent"),
	path('invoices/new', views.new_invoice, name="new_invoice"),
	path('clients/new', views.new_client, name="new_client"),
	path('products/new', views.new_product, name="new_product"),
	path('payments/new', views.new_payment, name="new_payment"),

	## Display n Edit 
	re_path(r'^invoices/(?P<id>\d+)$', views.single_invoice, name="single_invoice"),
	re_path(r'^products/(?P<id>\d+)$', views.single_product, name="single_product"),
	re_path(r'^agents/(?P<id>\d+)$', views.single_agent, name="single_agent"),
	re_path(r'^clients/(?P<id>\d+)$', views.single_client, name="single_client"),
	re_path(r'^payments/(?P<id>\d+)$', views.single_payment, name="single_payment"),
	re_path(r'^payments/(?P<id>\d+)/edit$', views.edit_payment, name="edit_payment"),

	re_path(r'^clients/(?P<id>\d+)/edit$', views.edit_client, name="edit_client"),
	re_path(r'^invoices/(?P<id>\d+)/edit$', views.edit_invoice, name="edit_invoice"),

	## Admin Site
	path('admin/', admin.site.urls),
	
	## Search API
	re_path(r'^api/(?P<model>product)/(?P<id>\w+)$', views.api, name="data_api"),
	re_path(r'^api/(?P<model>size)/(?P<id>\w+)$', views.api, name="data_api"),
	re_path(r'^api/(?P<model>[a-z]+)/(?P<id>\d+)$', views.api, name="data_api"),
]
