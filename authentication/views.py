from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView

from .serializers import ProfileUpdateSerializer


class ProfileUpdateView(UpdateAPIView):
    """
        This defines an API view to update a user's profile. It only accepts PUT-Requests
    """
    # A user must be authenticated to update a user
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileUpdateSerializer

    def update(self, request, *args, **kwargs):
        # serialize, validate, save pattern
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class TestProtectedView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response({'token_valid': True})

