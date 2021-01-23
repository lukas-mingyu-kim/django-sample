from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.db import transaction

from sample_api import serializers
from sample_api import models
from sample_api import permissions
from sample_api.authentication import ExpiringTokenAuthentication


class UserLoginApiView(ObtainAuthToken):

    serializer_class = serializers.AtmLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            card_num = serializer.validated_data.get('card_num')
            pin_num = serializer.validated_data.get('pin_num')
            if not self._is_pin_valid():
                return Response(status=status.HTTP_401_UNAUTHORIZED)

            if not models.AtmUser.objects.filter(card_num=card_num).exists():
                user = models.AtmUser.objects.create_user(card_num=card_num, password=pin_num)
                user.save()
            else:
                user = models.AtmUser.objects.get(card_num=card_num)

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user_id': user.id,
                'token': token.key
            })

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def _is_pin_valid(self):
        # TODO: call bank API to check the PIN
        return True


class AccountApiView(APIView):

    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (permissions.OwnAccount,)
    serializer_class = serializers.AtmSerializer

    def get(self, request, user_id):
        user = models.AtmUser.objects.get(id=user_id)
        user_accounts = user.account_set.all()
        serializer = serializers.AccountSerializer(user_accounts, many=True)
        return Response({'accounts': serializer.data})


class DepositWithdrawApiView(APIView):

    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (permissions.OwnAccount,)
    serializer_class = serializers.BalanceSerializer

    def post(self, request, user_id):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            url = request.get_full_path()
            account_num = serializer.validated_data.get('account_num')
            amount = serializer.validated_data.get('amount')

            account = models.Account.objects.filter(user__id=user_id, account_num=account_num).first()
            if not account:
                return Response(
                    "No such account",
                    status=status.HTTP_400_BAD_REQUEST
                )

            with transaction.atomic():
                if url.endswith('deposit'):
                    self._deposit_bin(amount)
                    account.balance += amount
                    account.save()
                else:
                    if account.balance - amount < 0:
                        return Response(
                            "Balance not sufficient",
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    self._withdraw_bin(amount)
                    account.balance -= amount
                    account.save()

            serializer = serializers.AccountSerializer(account)
            return Response({'account': serializer.data})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def _can_withdraw_from_bin(self, amount):
        # TODO: check cash bin for enough cash to withdraw
        return True

    def _deposit_bin(self, amount):
        # TODO: send call to cash bin to deposit
        return

    def _withdraw_bin(self, amount):
        # TODO: send call to cash bin to deposit
        return
