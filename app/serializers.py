from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

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