
from django.db import models
from django.conf import settings
from accounts.models import Company
from catalog.models import Batch


class Order(models.Model):

    class OrderStatus(models.TextChoices):
        PLACED = 'PLACED', 'Placed'
        DELIVERED = 'DELIVERED', 'Delivered'

    order_id = models.AutoField(primary_key=True)

    order_buyer_company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    order_placed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='placed_orders'
    )

    order_status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PLACED
    )

    order_created_at = models.DateTimeField(auto_now_add=True)
    order_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id}"


class OrderItem(models.Model):

    order_item_id = models.AutoField(primary_key=True)

    order_item_order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    order_item_batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        related_name='order_items'
    )

    order_item_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"Order {self.order_item_order_id} - {self.order_item_batch.batch_code}"
