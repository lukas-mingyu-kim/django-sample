from rest_framework import serializers

from sample_api import models


class AtmSerializer(serializers.Serializer):
    card_num = serializers.CharField(max_length=10)


class BalanceSerializer(serializers.Serializer):
    account_num = serializers.CharField(max_length=20)
    amount = serializers.IntegerField()


class AtmLoginSerializer(serializers.Serializer):
    card_num = serializers.CharField(max_length=20)
    pin_num = serializers.CharField(max_length=6)






class AtmUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AtmUser
        fields = ('id', 'card_num', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        user = models.AtmUser.objects.create_user(
            card_num=validated_data['card_num'],
            password=validated_data['password'],
        )
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class ProfileFeedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProfileFeedItem
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        extra_kwargs = {'user_profile': {'read_only': True}}


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Account
        fields = ('account_num', 'user', 'balance')
        extra_kwargs = {'user': {'read_only': True}}
