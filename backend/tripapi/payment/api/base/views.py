from uuid import uuid4

from account.api.base.permissions import AuthUserIsPartner, BasicPerm
from cargo.models import Order
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from payment.models import BankAccount, Transaction, UserAuthorizationCode
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.base.errors import PaymentClientError
from utils.base.general import url_with_params
from utils.base.logger import err_logger, logger  # noqa
from utils.base.mixins import ListMixinUtils, UpdateRetrieveViewSet
from utils.base.flutterwave import payment_client
from django.db import transaction

from . import serializers


class SavedUserAuthorizationList(generics.ListAPIView):
    serializer_class = serializers.UASerializer
    permission_classes = (AuthUserIsPartner,)

    # Filter the queryset to only authorizations for this user
    def get_queryset(self):
        return UserAuthorizationCode.objects.filter(
            user__id=self.request.user.id
        ).order_by('account_name')


class CreateOrderTransaction(generics.GenericAPIView):
    """
    Create new transaction for a connector (order or booking). \
When you visit the checkout url, you will be redirected to the \
payment gateway to complete the payment. When payment is completed, \
you will be redirected to the callback url you provided with the \
status of the transaction and the tracking code of the transaction.
    """
    serializer_class = serializers.CreateOrderTxSerializer
    permission_classes = (BasicPerm,)

    def create_payment_link(self, order: Order, reference: str) -> str:
        """
        Create the payment link for the order
        """
        # Create the callback api url
        site = get_current_site(self.request).domain
        link = str(reverse('payment:callback_payment_client'))
        callback = f'{self.request.scheme}://' + site + link

        try:
            link = payment_client.create_init_transaction(
                email=order.package.user.email,
                amount=order.price,
                callback_url=callback,
                reference=reference
            )
        except PaymentClientError as e:
            err_logger.exception(e)
            raise ValidationError({'message': str(e)})
        except Exception as e:
            err_logger.exception(e)
            raise ValidationError({'message': 'Unable to create payment link'})
        return link

    @swagger_auto_schema(
        responses={200: serializers.CreateTxResponse}
    )
    def post(self, request, format=None, *args, **kwargs):
        # Validate the request data
        serializer = serializers.CreateOrderTxSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order: Order = serializer.validated_data.get('tracking_code')
        reference = uuid4().hex
        link = self.create_payment_link(order, reference)

        callback = request.data.get('callback')
        Transaction.objects.create(
            amount=order.price,
            status='pending',
            reference=reference,
            redirect_url=callback,
            order=order
        )

        data = {
            'authorization_url': link
        }
        return Response(data=data)


class CallbackTransaction(APIView):
    """
    Process the callback from payment gateway,
    and update the transaction status
    """
    permission_classes = []

    def redirect_response(self, tx_obj: Transaction, params: dict[str, str]):
        redirect_url = tx_obj.redirect_url
        if not redirect_url:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=params)
        redirect_url = url_with_params(redirect_url, params)
        return redirect(redirect_url)

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        params = {
            "message": "",
            "status": "error",
        }

        reference = request.GET.get('tx_ref')

        trans_obj = get_object_or_404(Transaction, reference=reference)
        params["tracking_code"] = trans_obj.get_tx_tracking_code()

        # Verification transaction status on payment client
        try:
            payment_client.verify_transaction(
                reference,
                trans_obj.amount
            )
            trans_obj.status = 'success'
            trans_obj.paidAt = timezone.now()
            trans_obj.save()
            trans_obj.update_success()
            params['status'] = 'success'
        except PaymentClientError as e:
            err_logger.exception(e)
            params['message'] = str(e)
            trans_obj.status = 'failed'
            trans_obj.save()
        except Exception as e:
            err_logger.exception(e)
            params['message'] = 'Error verifying transaction'

        return self.redirect_response(trans_obj, params)


class BankAccountViewSet(UpdateRetrieveViewSet):
    """
    Views for update and retrieving user account details
    """
    serializer_class = serializers.BankAccountSerializer
    permission_classes = (AuthUserIsPartner,)

    def get_queryset(self):
        return BankAccount.objects.all()

    def get_object(self):
        return self.request.user.bankaccount


class PaymentViewSet(ListMixinUtils, viewsets.ReadOnlyModelViewSet):
    """
    Views for listing and retrieving payments
    """
    serializer_class = serializers.PaymentSerializer
    permission_classes = (AuthUserIsPartner,)
    lookup_field = 'tracking_code'

    def get_queryset(self):
        return Transaction.objects.filter(
            bank_account=self.request.user.bankaccount)

    def get_transaction_filter(self, status: str) -> QuerySet:
        """Filter partner transactions by their status"""
        return self.filter_queryset(
            self.get_queryset()).filter(status=status)

    @action(detail=False, methods=['get'], url_path='status/pending')
    def pending_payments(self, request, *args, **kwargs):
        """Get all pending payments for partner"""
        queryset = self.get_transaction_filter('pending')
        return self.get_with_queryset(queryset)

    @action(detail=False, methods=['get'], url_path='status/success')
    def successful_payments(self, request, *args, **kwargs):
        """Get all success payments for partner"""
        queryset = self.get_transaction_filter('success')
        return self.get_with_queryset(queryset)

    @action(detail=False, methods=['get'], url_path='status/failed')
    def failed_payments(self, request, *args, **kwargs):
        """Get all failed payments for partner"""
        queryset = self.get_transaction_filter('failed')
        return self.get_with_queryset(queryset)
