from django.contrib import admin
from .models import *

admin.site.register(Agent)
admin.site.register(Bill)
admin.site.register(Client)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(Payment)