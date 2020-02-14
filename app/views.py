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

class FillResponseView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowMeetCreatorandMembers)
    serializer_class = FillResponseSerializer
    lookup_field = 'pk'
    queryset = Meetup.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'meetup':self.get_object()
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.fill_response()
        return API_RESPONSE(status=status.HTTP_200_OK)

class AddMembersView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowMeetCreator)
    serializer_class = AddMembersSerializer
    lookup_field = 'pk'
    queryset = Meetup.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'meetup':self.get_object()
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.add_members()
        return API_RESPONSE(status=status.HTTP_200_OK)

class CheckResponseView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowMeetCreatorandMembers)
    serializer_class = CheckResponseSerializer
    lookup_field = 'pk'
    queryset = Meetup.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'meetup':self.get_object()
        }

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        response = serializer.check_response()
        return API_RESPONSE(response.data, status=status.HTTP_200_OK)

class FinalizeMeetView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, AllowMeetCreator)
    serializer_class = FinalizeMeetSerializer
    lookup_field = 'pk'
    queryset = Meetup.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'meetup':self.get_object()
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.finalize_response()
        return API_RESPONSE(response.data, status=status.HTTP_200_OK)

class AddTaskView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = AddTaskSerializer
    lookup_field = 'pk'
    queryset = Meetup.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'meetup':self.get_object()
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.add_task()
        return API_RESPONSE(status=status.HTTP_200_OK)

class CompleteTaskView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = CompleteTaskSerializer
    lookup_field = 'pk'
    queryset = Task.objects.all()

    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            return None
        return super().get_object()

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'task':self.get_object()
        }

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.complete_task()
        return API_RESPONSE(status=status.HTTP_200_OK)