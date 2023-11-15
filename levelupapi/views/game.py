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

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        game_type = GameType.objects.get(pk=request.data["gametype"])

        game = Game()

        game.user = request.auth.user
        game.name = request.data.get('name')
        game.gametype = game_type
        game.description = request.data.get('description')
        game.difficulty = request.data.get('difficulty')
        game.duration = request.data.get('duration')
        game.num_of_players = request.data.get('num_of_players')

        game.save()

        try:
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data and send it back to the client


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
