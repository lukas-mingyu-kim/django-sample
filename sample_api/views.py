from rest_framework.views import APIView
from rest_framework.response import Response


class AtmApiView(APIView):
    """ATM API View"""

    def get(self, request, format=None):
        """Returns balance"""

        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'Is similar to a traditional Django View'
        ]

        return Response({
            'message': 'balance GET API!!',
        })
