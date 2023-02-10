"""View module for handling requests about attendees"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Attendee


class AttendeeView(ViewSet):
    """Level up attendees view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single attendee

        Returns:
            Response -- JSON serialized attendee
        """
        attendee = Attendee.objects.get(pk=pk)
        serializer = AttendeeSerializer(attendee)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all attendees

        Returns:
            Response -- JSON serialized list of attendees
        """
        attendees = Attendee.objects.all()
        serializer = AttendeeSerializer(attendees, many=True)
        return Response(serializer.data)

class AttendeeSerializer(serializers.ModelSerializer):
    """JSON serializer for attendees
    """
    class Meta:
        model = Attendee
        fields = ('id', 'event_id', 'gamer_id')