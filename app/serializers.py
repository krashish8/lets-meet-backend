from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
import textwrap

class MeetSerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField(read_only=True)
    members = serializers.SerializerMethodField(read_only=True)

    def get_creator(self, obj):
        return obj.creator.email

    def get_members(self, obj):
        return obj.members.all().values_list('email', flat=True)

    class Meta:
        model = Meetup
        fields = '__all__'
        read_only_fields = ('zoom_link', 'is_accepted', 'is_slack')

class MeetsSerializer(serializers.ModelSerializer):
    created_meets = serializers.SerializerMethodField()
    participating_meets = serializers.SerializerMethodField()

    def get_created_meets(self, obj):
        created_meets_queryset = obj.created_meetups
        return MeetSerializer(created_meets_queryset, many=True).data

    def get_participating_meets(self, obj):
        participating_meets_queryset = obj.participating_meetups
        return MeetSerializer(participating_meets_queryset, many=True).data

    class Meta:
        model = User
        fields = ('created_meets', 'participating_meets')

class ProposeMeetSerializer(serializers.ModelSerializer):
    def propose_meet(self, user):
        data = self.validated_data
        meetup = Meetup.objects.create(
            title = data['title'],
            description = data['description'],
            is_slack = data['is_slack'],
            creator = user
        )
        return MeetSerializer(meetup)

    class Meta:
        model = Meetup
        fields = ('title', 'description', 'is_slack')

class FillResponseSerializer(serializers.Serializer):
    response = serializers.CharField(max_length=255)

    def fill_response(self):
        meetup = self.context['meetup']
        response = self.validated_data['response']
        user = self.context['request'].user

        if Response.objects.filter(member=user, meetup=meetup):
            raise serializers.ValidationError("Already Responded")

        Response.objects.create(
            member=user,
            meetup=meetup,
            response=response
        )

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

class AddMembersSerializer(serializers.Serializer):
    members = MemberSerializer(many=True)

    def add_members(self):
        meetup = self.context['meetup']
        members = self.validated_data['members']
        for member in members:
            user = User.objects.filter(username=member['email'])
            if not user:
                raise serializers.ValidationError("No such member")
            user = user[0]

            meetup.members.add(user)
            meetup.save()

class CommonTimeSerializer(serializers.Serializer):
    response = serializers.CharField(max_length=255)

class CheckResponseSerializer(serializers.Serializer):
    def bitwise_or(self, string1, string2):
        strring = ''
        for i in range(len(string1)):
            if string1[i] == '1' and string2[i] == '1':
                strring += '1'
            else:
                strring += '0'
        return strring

    def check_response(self):
        meetup = self.context['meetup']

        responses = list()

        for user in meetup.members.all():
            response = Response.objects.filter(meetup=meetup, user=user)
            if not response:
                raise serializers.ValidationError("All members have not responded yet")
            responses.append(response[0].response)

        day_wise_responses = list()

        for response in responses:
            day_wise_responses.append(textwrap.wrap(response, 24))

        day_responses = ''

        for i in range(7):
            final_string = '1' * 24
            for j in range(len(day_wise_responses)):
                final_string = self.bitwise_or(final_string, day_wise_responses[j][i])

            day_responses += final_string

        return CommonTimeSerializer({
            'response': day_responses
        })        

class ZoomLinkSerializer(serializers.Serializer):
    zoom_link = serializers.URLField()

class FinalizeMeetSerializer(serializers.Serializer):
    date_time = serializers.DateTimeField()
    duration = serializers.IntegerField()

    def finalize_response(self):
        meetup = self.context['meetup']
        date_time = self.validated_data['date_time']
        duration = self.validated_data['duration']
        meetup.date_and_time = date_time
        meetup.duration = duration
        meetup.is_accepted = True
        meetup.zoom_link = 'https://www.zoom.us/j/da6546das46das4s'
        meetup.save()

        return ZoomLinkSerializer({
            'zoom_link': meetup.zoom_link
        })

class AddTaskSerializer(serializers.ModelSerializer):
    member = MemberSerializer()

    def add_task(self):
        meetup = self.context['meetup']
        data = self.validated_data
        user = User.objects.filter(username=data['member']['email'])
        if not user:
            raise serializers.ValidationError("No such member")
        user = user[0]
        Task.objects.create(
            meetup = meetup,
            title = data['title'],
            description = data['description'],
            assigned_to = user
        )

    class Meta:
        model = Task
        fields = ('title', 'description', 'member')

class CompleteTaskSerializer(serializers.Serializer):
    def complete_task(self):
        task = self.context['task']
        task.completed = True
        task.save()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'