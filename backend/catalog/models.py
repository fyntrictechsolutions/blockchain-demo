
from django.db import models
from accounts.models import Company


# 1. Product Model
class Product(models.Model):

    product_id = models.AutoField(primary_key=True)

    product_company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name='products'
    )

    product_name = models.CharField(max_length=255)
    product_grade = models.CharField(max_length=50)

    product_price_per_tonne = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    product_description = models.TextField(blank=True)
    product_is_active = models.BooleanField(default=True)

    product_created_at = models.DateTimeField(auto_now_add=True)
    product_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} - {self.product_grade}"


# 2. Batch Model
class Batch(models.Model):

    batch_id = models.AutoField(primary_key=True)

    batch_code = models.CharField(
        max_length=100,
        unique=True
    )

    batch_product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='batches'
    )

    batch_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    batch_current_holder = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name='held_batches'
    )

    batch_manufacturing_date = models.DateField(
        null=True,
        blank=True
    )

    batch_created_at = models.DateTimeField(auto_now_add=True)
    batch_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.batch_code


# 3. Document Model
class Document(models.Model):

    class DocumentType(models.TextChoices):
        TEST_CERTIFICATE = 'TEST_CERTIFICATE', 'Test Certificate'

    document_id = models.AutoField(primary_key=True)

    document_batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        related_name='documents'
    )

    document_file = models.FileField(
        upload_to='batch_certificates/'
    )

    document_sha256 = models.CharField(
        max_length=64,
        blank=True
    )

    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
        default=DocumentType.TEST_CERTIFICATE
    )

    document_uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} - {self.document_batch.batch_code}"
