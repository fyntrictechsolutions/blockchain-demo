
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import Company
from catalog.models import Product


class Command(BaseCommand):

    help = "Insert sample companies and products"

    @transaction.atomic
    def handle(self, *args, **kwargs):

        # 1. Create sample companies

        manufacturer, created = Company.objects.get_or_create(
            company_name="Kerala Steel Ltd",
            defaults={
                "company_type": Company.CompanyType.MANUFACTURER,
                "company_email": "info@keralasteel.com",
                "company_is_active": True,
            }
        )

        buyer, created = Company.objects.get_or_create(
            company_name="ABC Builders",
            defaults={
                "company_type": Company.CompanyType.BUYER,
                "company_email": "info@abcbuilders.com",
                "company_is_active": True,
            }
        )

        # 2. Create sample products

        products = [
            {
                "product_name": "TMT Steel Bars",
                "product_grade": "Fe500",
                "product_price_per_tonne": Decimal("55000.00"),
            },
            {
                "product_name": "TMT Steel Bars",
                "product_grade": "Fe500D",
                "product_price_per_tonne": Decimal("56000.00"),
            },
            {
                "product_name": "TMT Steel Bars",
                "product_grade": "Fe550",
                "product_price_per_tonne": Decimal("57000.00"),
            },
        ]

        for product_data in products:

            Product.objects.get_or_create(
                product_company=manufacturer,
                product_name=product_data["product_name"],
                product_grade=product_data["product_grade"],
                defaults={
                    "product_price_per_tonne":
                        product_data["product_price_per_tonne"],
                    "product_is_active": True,
                }
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Sample companies and products created successfully!"
            )
        )
