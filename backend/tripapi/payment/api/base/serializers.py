from payment.models import (BankAccount, Transaction,
                            UserAuthorizationCode)
from rest_framework import serializers

from cargo.models import Order


class CreateOrderTxSerializer(serializers.Serializer):
    callback = serializers.URLField(
        help_text='Callback url for the payment link')
    tracking_code = serializers.CharField(
        help_text='Tracking code of the order to create transaction for')

    def validate_tracking_code(self, tracking_code: str) -> str:
        """
        Validate the tracking code
        """
        try:
            return Order.objects.get(tracking_code=tracking_code)
        except Order.DoesNotExist:
            raise serializers.ValidationError(
                {'tracking_code': 'Order not found'}
            )


class UASerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAuthorizationCode
        exclude = ('user', 'authorization_code')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class CreateTxResponse(serializers.Serializer):
    authorization_url = serializers.CharField()


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        exclude = ('user', 'id',)


class PaymentSerializer(serializers.ModelSerializer):
    amount = serializers.FloatField(
        help_text='Date when booking was placed', read_only=True)
    date = serializers.CharField(
        help_text='Date when payment was completed', read_only=True)
    time = serializers.CharField(
        help_text='Time when payment was completed', read_only=True)
    status = serializers.CharField(
        help_text='Transaction status', read_only=True)

    class Meta:
        model = Transaction
        exclude = ('bank_account', 'id')
        read_only_fields = ('tracking_code', 'created', 'trip')

    def to_representation(self, instance: Transaction):
        rep = super().to_representation(instance)

        paidAt = instance.paidAt
        date, time = None, None
        if paidAt is not None:
            date, time = str(instance.created).split()
        rep['date'] = date
        rep['time'] = time

        return rep
