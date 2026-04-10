from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.contrib import admin
from django.contrib.auth import views as auth_views
import Software.views as views


urlpatterns = [
	path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
	path('logout/', views.logout_view, name="logout"),
	path('admin/logout/', views.logout_view, name="admin_logout"),
	path('', views.homepage, name="homepage"),
	
	## Display Entries
	path('agents/', views.agents, name="agents"),
	path('clients/', views.clients, name="clients"),
	path('invoices/', views.invoices, name="invoices"),
	path('products/', views.products, name="products"),
	path('payments/', views.payments, name="payments"),
	path('sizes/', views.sizes, name="sizes"),
	path('firm-settings/', views.firm_settings, name="firm_settings"),
	path('reports/', views.reports, name="reports"),
	path('reports/export/<str:export_type>/', views.reports_export, name="reports_export"),
	path('maintenance/', views.maintenance, name="maintenance"),
	path('maintenance/backup/', views.download_backup, name="download_backup"),

	## Add Entries
	path('agents/new', views.new_agent, name="new_agent"),
	path('invoices/new', views.new_invoice, name="new_invoice"),
	path('clients/new', views.new_client, name="new_client"),
	path('products/new', views.new_product, name="new_product"),
	path('payments/new', views.new_payment, name="new_payment"),

	## Display n Edit 
	re_path(r'^invoices/(?P<id>\d+)$', views.single_invoice, name="single_invoice"),
	re_path(r'^invoices/(?P<id>\d+)/print$', views.print_invoice, name="print_invoice"),
	re_path(r'^invoices/(?P<id>\d+)/delete$', views.delete_invoice, name="delete_invoice"),
	re_path(r'^products/(?P<id>\d+)$', views.single_product, name="single_product"),
	re_path(r'^products/(?P<id>\d+)/delete$', views.delete_product, name="delete_product"),
	re_path(r'^agents/(?P<id>\d+)$', views.single_agent, name="single_agent"),
	re_path(r'^agents/(?P<id>\d+)/delete$', views.delete_agent, name="delete_agent"),
	re_path(r'^clients/(?P<id>\d+)$', views.single_client, name="single_client"),
	re_path(r'^clients/(?P<id>\d+)/delete$', views.delete_client, name="delete_client"),
	re_path(r'^sizes/(?P<id>\d+)/delete$', views.delete_size, name="delete_size"),
	re_path(r'^payments/(?P<id>\d+)$', views.single_payment, name="single_payment"),
	re_path(r'^payments/(?P<id>\d+)/edit$', views.edit_payment, name="edit_payment"),
	re_path(r'^payments/(?P<id>\d+)/delete$', views.delete_payment, name="delete_payment"),

	re_path(r'^clients/(?P<id>\d+)/edit$', views.edit_client, name="edit_client"),
	re_path(r'^invoices/(?P<id>\d+)/edit$', views.edit_invoice, name="edit_invoice"),

	## Admin Site
	path('admin/', admin.site.urls),
	
	## Search API
	re_path(r'^api/(?P<model>product)/(?P<id>\w+)$', views.api, name="data_api"),
	re_path(r'^api/(?P<model>size)/(?P<id>\w+)$', views.api, name="data_api"),
	re_path(r'^api/(?P<model>[a-z]+)/(?P<id>\d+)$', views.api, name="data_api"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
