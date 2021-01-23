from rest_framework import serializers

from sample_api import models


class AtmSerializer(serializers.Serializer):
    card_num = serializers.CharField(max_length=20)


class BalanceSerializer(serializers.Serializer):
    account_num = serializers.CharField(max_length=20)
    amount = serializers.IntegerField()


class AtmLoginSerializer(serializers.Serializer):
    card_num = serializers.CharField(max_length=20)
    pin_num = serializers.CharField(max_length=6)


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Account
        fields = ('account_num', 'user', 'balance')
        extra_kwargs = {'user': {'read_only': True}}
