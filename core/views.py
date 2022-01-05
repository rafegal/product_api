from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Company, ProductCompany
from django.contrib.auth.models import User
import json

import base64
from django.contrib.auth import authenticate


def header_auth_view(request):
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if not auth_header:
        return False, None
    encoded_credentials = auth_header.split(" ")[
        1
    ]  # Removes "Basic " to isolate credentials
    decoded_credentials = (
        base64.b64decode(encoded_credentials).decode("utf-8").split(":")
    )
    username = decoded_credentials[0]
    password = decoded_credentials[1]
    user = User.objects.filter(username=username).first()
    return authenticate(username=username, password=password), user


@csrf_exempt
def product(request):
    auth, user = header_auth_view(request)
    if not auth:
        return JsonResponse(
            {"status": "error", "message": "Invalid credentials"}, status=401
        )
    print("######")
    if request.method == "POST":
        data = json.loads(request.body)
        if Product.objects.filter(name=data["name"]):
            return JsonResponse(
                {"status": "error", "message": "Product already exists"}, status=400
            )
        product = Product.objects.create(
            name=data["name"],
            price=data["price"],
            description=data.get("description"),
            created_by=user,
            updated_by=user,
        )
        return JsonResponse(
            {
                "status": "ok",
                "message": f"Successfully created '{product.name}' product",
                "id": product.id,
            },
            status=200,
        )
    if request.method == "GET":
        product_name = request.GET.get("name")
        product = Product.objects.filter(name=product_name).first()
        if product:
            return JsonResponse(
                {
                    "status": "ok",
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    # "add_date": product.description,
                    "description": product.description,
                    "created_by": product.created_by.get_full_name(),
                },
                status=200,
            )
        else:
            return JsonResponse(
                {"status": "error", "message": "Product '{product_name}' not found"},
                status=404,
            )


@csrf_exempt
def company(request):
    auth, user = header_auth_view(request)
    if not auth:
        return JsonResponse(
            {"status": "error", "message": "Invalid credentials"}, status=401
        )
    if request.method == "POST":
        data = json.loads(request.body)
        if Company.objects.filter(name=data["name"]):
            return JsonResponse(
                {"status": "error", "message": "Company already exists"}, status=400
            )
        company = Company.objects.create(
            name=data["name"],
            created_by=user,
            updated_by=user,
        )
        return JsonResponse(
            {
                "status": "ok",
                "message": f"Successfully created '{company.name}' company",
                "id": company.id,
            },
            status=200,
        )
    if request.method == "GET":
        print("######")
        company_name = request.GET.get("name")
        company = Company.objects.filter(name=company_name).first()
        if company:
            print("######")
            return JsonResponse(
                {
                    "status": "ok",
                    "id": company.id,
                    "name": company.name,
                    "created_by": company.created_by.get_full_name(),
                },
                status=200,
            )
        else:
            return JsonResponse(
                {"status": "error", "message": f"Company '{company_name}' not found"},
                status=404,
            )


@csrf_exempt
def company_product(request):
    auth, user = header_auth_view(request)
    if not auth:
        return JsonResponse(
            {"status": "error", "message": "Invalid credentials"}, status=401
        )
    if request.method == "POST":
        data = json.loads(request.body)
        if not Product.objects.filter(
            id=data["product_id"]
        ) or not Company.objects.filter(id=data["company_id"]):
            return JsonResponse(
                {"status": "error", "message": "Company or Product does not exist"},
                status=400,
            )
        product = Product.objects.get(id=data["product_id"])
        company = Company.objects.get(id=data["company_id"])

        # product = Product.objects.get(name=data["product_name"])
        # company = Company.objects.get(name=data["company_name"])
        product_company = ProductCompany.objects.filter(
            product=product,
            company=company,
        ).first()
        if product_company:
            product_company.quantity = data["quantity"]
            product_company.save()
        else:
            product_company = ProductCompany.objects.create(
                product=product,
                company=company,
                quantity=data["quantity"],
                created_by=user,
                updated_by=user,
            )
        return JsonResponse(
            {
                "status": "ok",
                "message": f"Success",
                "id": product_company.id,
            },
            status=200,
        )
    else:
        # company_name = request.GET.get("company_name")
        # product_name = request.GET.get("product_name")

        company_id = request.GET.get("company_id")
        product_id = request.GET.get("product_id")

        product_company = ProductCompany.objects.filter(
            company__id=company_id, product__id=product_id
        ).first()

        # product_company = ProductCompany.objects.filter(
        #     company__name=company_name, product__name=product_name
        # ).first()
        if product_company:
            return JsonResponse(
                {
                    "status": "ok",
                    "id": product_company.id,
                    "company": product_company.company.name,
                    "product": product_company.product.name,
                    "quantity": product_company.quantity,
                    "created_by": product_company.created_by.get_full_name(),
                },
                status=200,
            )
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Company or Product does not exist",
                },
                status=404,
            )


def company_product_all(request):
    auth, user = header_auth_view(request)
    if not auth:
        return JsonResponse(
            {"status": "error", "message": "Invalid credentials"}, status=401
        )
    if request.method == "GET":
        product_company = ProductCompany.objects.all()
        list_product_company = []
        for pc in product_company:
            list_product_company.append(
                {
                    "product_id": pc.product.id,
                    "product_name": pc.product.name,
                    "company_id": pc.company.id,
                    "company_name": pc.company.name,
                    "quantity": pc.quantity,
                }
            )
        return JsonResponse({"all_product_company": list_product_company})
