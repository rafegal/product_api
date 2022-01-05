from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.CharField(max_length=500, blank=True, null=True)
    add_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="product_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="product_updated_by")

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=100)
    add_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="company_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="company_updated_by")

    def __str__(self):
        return self.name


class ProductCompany(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="product_company_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="product_company_updated_by")

    def __str__(self):
        return f"{self.product.name} - {self.company.name}"
    