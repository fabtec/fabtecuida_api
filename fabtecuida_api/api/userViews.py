from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt import authentication

class GetUserViewSet(APIView):

	def post(self, request):
		response = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }
		return Response(response, status=status.HTTP_200_OK)

	