from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings as jwt_settings
from django.conf import settings

from django.db import transaction


from sample_api import serializers
from sample_api import models
from sample_api import permissions
from sample_api.authentication import ExpiringTokenAuthentication

#
# @api_view(['GET'])
# # @permission_classes((IsAuthenticated,))
# @authentication_classes((JSONWebTokenAuthentication,))
# def accounts(requests):
#
#
# def login(requests):


class AtmApiView(APIView):
    """ATM API View"""
    serializer_class = serializers.AtmSerializer

    def get(self, request, format=None):
        """Returns balance"""
        return Response({
            'message': 'balance GET API!!',
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class AtmUserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AtmUserSerializer
    queryset = models.AtmUser.objects.all()
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('card_num',)








class UserProfileFeedViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        IsAuthenticated
    )

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)






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
