from rest_framework.response import Response as API_RESPONSE
from .serializers import *
from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from .permissions import *

class MeetsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MeetsSerializer

    def get(self, request):
        queryset = request.user
        response = self.get_serializer(queryset)
        return API_RESPONSE(response.data, status.HTTP_200_OK)

class ProposeMeetView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProposeMeetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.propose_meet(request.user)
        return API_RESPONSE(response.data, status.HTTP_200_OK)

class MeetView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowMeetCreatorandMembers)
    serializer_class = MeetSerializer
    queryset = Meetup.objects.all()


