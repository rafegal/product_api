from django.urls import path

from .views import product, company, company_product, company_product_all
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("product/", product, name="product"),
    path("company/", company, name="company"),
    path("company/product/all", company_product_all, name="company_product_all"),
    path("company/product/", company_product, name="company_product"),
]