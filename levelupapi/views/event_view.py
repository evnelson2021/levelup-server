"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game, GameType


class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all events

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        organizing_gamer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])
        # type = GameType.objects.get(pk=request.data["type"])

        event = Event.objects.create(
            # game=request.data["game"],
            location=request.data["location"],
            date=request.data["date"],
            start_time=request.data["start_time"],
            end_time=request.data["end_time"],
            details=request.data["details"],
            # attendees=request.data["attendees"],
            organizing_gamer=organizing_gamer,
            game=game
            # type=type
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)


class EventGameSerializer(serializers.ModelSerializer):
    """JSON serializer for organizers
    """
    class Meta:
        model = Game
        fields = ('name',)

class OrganizerSerializer(serializers.ModelSerializer):
    """JSON serializer for organizers
    """
    class Meta:
        model = Gamer
        fields = ('full_name',)

class AttendeeSerializer(serializers.ModelSerializer):
    """JSON serializer for attendees
    """
    class Meta:
        model = Gamer
        fields = ('full_name',)


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    game = EventGameSerializer(many=False)
    organizing_gamer = OrganizerSerializer(many=False)
    attendees = AttendeeSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'organizing_gamer', 'game', 'location',
                'date', 'start_time', 'end_time', 'details', 'attendees')