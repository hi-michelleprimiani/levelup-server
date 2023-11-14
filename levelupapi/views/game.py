from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, GameType
from django.contrib.auth.models import User


class GameView(ViewSet):

    def retrieve(self, request, pk):
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):
        game = Game.objects.all()
        serializer = GameSerializer(game, many=True)
        return Response(serializer.data)


class GameUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ['full_name', 'username']


class GameGameTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = GameType
        fields = ['description']


class GameSerializer(serializers.ModelSerializer):

    user = GameUserSerializer(many=False)
    gametype = GameGameTypeSerializer(many=False)

    class Meta:
        model = Game
        fields = ['id', 'name', 'user', 'gametype', 'description',
                  'difficulty', 'duration', 'num_of_players']
