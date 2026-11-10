
from django.db import models
from accounts.models import Company
from catalog.models import Batch
from orders.models import Order


class ChainTx(models.Model):

    class TransactionType(models.TextChoices):
        REGISTER_BATCH = 'REGISTER_BATCH', 'Register Batch'
        TRANSFER_CUSTODY = 'TRANSFER_CUSTODY', 'Transfer Custody'

    class TransactionStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        FAILED = 'FAILED', 'Failed'

    chain_tx_id = models.AutoField(primary_key=True)

    chain_tx_kind = models.CharField(
        max_length=30,
        choices=TransactionType.choices
    )

    chain_tx_batch = models.ForeignKey(
        Batch,
        on_delete=models.PROTECT,
        related_name='chain_transactions'
    )

    chain_tx_order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='chain_transactions'
    )

    chain_tx_from_company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='outgoing_chain_transactions'
    )

    chain_tx_to_company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='incoming_chain_transactions'
    )

    chain_tx_hash = models.CharField(
        max_length=66,
        unique=True,
        null=True,
        blank=True
    )

    chain_tx_status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING
    )

    chain_tx_block_number = models.BigIntegerField(
        null=True,
        blank=True
    )

    chain_tx_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.chain_tx_kind} - {self.chain_tx_batch.batch_code}"
