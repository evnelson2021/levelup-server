"""View module for handling requests about games"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Game, Gamer, GameType


class GameView(ViewSet):
    """Level up games view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game
        """
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all games

        Returns:
            Response -- JSON serialized list of games
        """
        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        gamer = Gamer.objects.get(user=request.auth.user)
        type = GameType.objects.get(pk=request.data["type"])

        game = Game.objects.create(
            # type=request.data["type"],
            # gamer=request.data["gamer"],
            name=request.data["name"],
            length=request.data["length"],
            min_age=request.data["min_age"],
            min_players=request.data["min_players"],
            max_players=request.data["max_players"],
            gamer=gamer,
            type=type
        )
        serializer = GameSerializer(game)
        return Response(serializer.data)

class GameCreatorSerializer(serializers.ModelSerializer):
    """JSON serializer for attendees
    """
    class Meta:
        model = Gamer
        fields = ('full_name',)

class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for attendees
    """
    class Meta:
        model = GameType
        fields = ('label',)

class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    gamer = GameCreatorSerializer()
    type = GameTypeSerializer()
    class Meta:
        model = Game
        fields = ('id', 'type', 'gamer', 'name', 'length', 'min_age', 'min_players', 'max_players', )
