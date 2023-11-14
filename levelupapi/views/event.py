from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from django.contrib.auth.models import User
from levelupapi.views.game import GameSerializer


class EventView(ViewSet):

    def retrieve(self, request, pk):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        # Get the 'game' parameter from the URL query parameters
        game_id = request.query_params.get('game')

        # Check if 'game' parameter is provided
        if game_id is not None:
            # Filter events based on the provided 'game_id'
            events = Event.objects.filter(game_id=game_id)
        else:
            # If 'game' parameter is not provided, return all events
            events = Event.objects.all()

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventOrganizer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ['full_name']


class EventSerializer(serializers.ModelSerializer):

    organizer = EventOrganizer(many=False)
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ['organizer', 'game', 'name',
                  'location', 'date', 'time', 'attendees']
