from django.contrib import admin

from .models import Agent, AuditLog, Bill, Client, FirmSettings, InvoiceSequence, Payment, Product, Size


@admin.register(FirmSettings)
class FirmSettingsAdmin(admin.ModelAdmin):
	list_display = ("firm_name", "invoice_template", "gstin", "contact_number", "alternate_contact_number", "third_contact_number", "updated_at")
	search_fields = ("firm_name", "gstin", "contact_number", "alternate_contact_number", "third_contact_number")


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
	list_display = ("display_invoice_number", "invoice_date", "client", "total_after_tax", "is_cleared", "is_deleted")
	list_filter = ("is_cleared", "is_deleted")
	search_fields = ("invoice_number", "client__name")

	def display_invoice_number(self, obj):
		return obj.display_invoice_number()
	display_invoice_number.short_description = "invoice_number"


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
	list_display = ("payment_date", "client", "paid_amount", "method_of_payment", "is_cleared", "is_deleted")
	list_filter = ("is_cleared", "is_deleted", "method_of_payment")
	search_fields = ("client__name", "method_of_payment", "description")


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
	list_display = ("created_at", "action", "model_name", "object_id", "actor")
	list_filter = ("action", "model_name")
	search_fields = ("object_id", "object_repr", "model_name")
	readonly_fields = ("action", "model_name", "object_id", "object_repr", "before_data", "after_data", "created_at", "actor")


admin.site.register(Agent)
admin.site.register(Client)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(InvoiceSequence)
