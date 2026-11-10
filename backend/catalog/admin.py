from django.contrib import admin
from .models import Product, Batch, Document

admin.site.register(Product)
admin.site.register(Batch)
admin.site.register(Document)

# Register your models here.
