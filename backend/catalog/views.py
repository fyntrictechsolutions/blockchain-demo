from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction

from .models import Product, Batch, Document
from .serializers import ProductSerializer, BatchSerializer
from chain.models import ChainTx
from chain.services import hash_file, register_batch_on_chain


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer

    def create(self, request, *args, **kwargs):
        # 1. Validate batch fields using our existing BatchSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 2. Check if a certificate file was uploaded in the form
        pdf_file = request.FILES.get('certificate') or request.FILES.get('document_file')

        # 3. Perform database operations safely together (like @Transactional in Java)
        with transaction.atomic():
            # Save the Batch in the database
            batch = serializer.save()

            doc_hash = None
            # If a certificate PDF was provided, hash it and save in Document table
            if pdf_file:
                doc_hash = hash_file(pdf_file)
                Document.objects.create(
                    document_batch=batch,
                    document_file=pdf_file,
                    document_sha256=doc_hash
                )

            # Call our chain service to get the transaction hash
            tx_hash = register_batch_on_chain(
                batch_code=batch.batch_code,
                doc_hash=doc_hash if doc_hash else "0x0"
            )

            # Record the transaction in the ChainTx table
            ChainTx.objects.create(
                chain_tx_batch=batch,
                chain_tx_kind=ChainTx.TransactionType.REGISTER_BATCH,
                chain_tx_from_company=batch.batch_current_holder,
                chain_tx_hash=tx_hash,
                chain_tx_status=ChainTx.TransactionStatus.PENDING
            )

        # Return the created batch data PLUS the transaction hash to the frontend
        response_data = serializer.data
        response_data['tx_hash'] = tx_hash
        return Response(response_data, status=status.HTTP_201_CREATED)