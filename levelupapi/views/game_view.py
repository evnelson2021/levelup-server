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
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Game.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.name = request.data["name"]
        game.length=request.data["length"]
        game.min_age=request.data["min_age"]
        game.min_players=request.data["min_players"]
        game.max_players=request.data["max_players"]

        type = GameType.objects.get(pk=request.data["type"])
        game.type = type
        game.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


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
        fields = ('id', 'label',)


class GameSerializer(serializers.ModelSerializer):
    """JSON serializer for games"""
    gamer = GameCreatorSerializer()
    type = GameTypeSerializer()

    class Meta:
        model = Game
        fields = ('id', 'type', 'gamer', 'name', 'length',
                  'min_age', 'min_players', 'max_players', )
