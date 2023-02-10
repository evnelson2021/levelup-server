"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event, Gamer, Game


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


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Event
        fields = ('id', 'organizing_gamer', 'game', 'location',
                  'date', 'start_time', 'end_time', 'details', 'attendees')

# class EventGameSerializer(serializers.ModelSerializer):
#     """JSON serializer for organizers
#     """
#     class Meta:
#         model = Game
#         fields = ('name',)

# class OrganizerSerializer(serializers.ModelSerializer):
#     """JSON serializer for organizers
#     """
#     class Meta:
#         model = Gamer
#         fields = ('full_name',)

# class AttendeeSerializer(serializers.ModelSerializer):
#     """JSON serializer for attendees
#     """
#     class Meta:
#         model = Gamer
#         fields = ('full_name',)

# class EventSerializer(serializers.ModelSerializer):
#     """JSON serializer for events
#     """

#     game = EventGameSerializer(many=False)
#     organizer = OrganizerSerializer(many=False)
#     attendees = AttendeeSerializer(many=True)
