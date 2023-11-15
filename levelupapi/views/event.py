from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Game
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

    def create(self, request):

        game = Game.objects.get(pk=request.data["game"])

        events = Event()

        events.organizer = request.auth.user
        events.game = game
        events.name = request.data.get('name')
        events.location = request.data.get('location')
        events.date = request.data.get('date')
        events.time = request.data.get('time')
        events.save()

        try:
            serializer = EventSerializer(events, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception:
            return Response(None, status=status.HTTP_404_NOT_FOUND)


class EventOrganizer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class EventSerializer(serializers.ModelSerializer):

    organizer = EventOrganizer(many=False)
    attendees = EventOrganizer(many=True)
    game = GameSerializer(many=False)
    time = serializers.SerializerMethodField()

    # def get_time(self, obj):
    #     # Use the 'time' field from the Event model
    #     return obj.time.strftime("%I:%M %p")

    class Meta:
        model = Event
        fields = ['id', 'organizer', 'game', 'name',
                  'location', 'date', 'time', 'attendees']


# class Developer:
#     def __init__(self, name):
#         self.name = name
#         self.languages = ["Javascript", "React",
#                           "Python", "Django", "Tailwind"]
#         self.loves = [
#             "exploring jazz music",
#             "getting vertical on rocks",
#             "devoting time to others"
#         ]
#         self.traits = ["laid-back", "compassionate", "silly-goose"]


# paolo = Developer("Paolo Medel")
