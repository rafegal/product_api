from django.contrib import admin
from .models import Company, Product, ProductCompany
# Register your models here.

admin.site.register(Company)
admin.site.register(Product)
admin.site.register(ProductCompany)