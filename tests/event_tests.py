import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Gamer, Event, Attendee, Game
from rest_framework.authtoken.models import Token


class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events', 'attendees']

    def setUp(self):
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_event(self):
        """
        Ensure we can create a new event.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/events"

        # Define the request body
        data = {
            "game": 1,
            "location": "123 Somewhere Way",
            "date": "2023-02-12",
            "start_time": "09:00",
            "end_time": "11:00",
            "details": "We will be meeting at my house to play Sequence at the end of the month. I have 3 boards and can host up to 18 people."
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["location"], "123 Somewhere Way")
        self.assertEqual(json_response["date"], "2023-02-12")
        self.assertEqual(json_response["start_time"], "09:00")
        self.assertEqual(json_response["end_time"], "11:00")
        self.assertEqual(json_response["details"], "We will be meeting at my house to play Sequence at the end of the month. I have 3 boards and can host up to 18 people.")



    def test_get_event(self):
        """
        Ensure we can get an existing event.
        """

        # Seed the database with a game
        event = Event()
        event.game = Game(pk=2)
        event.location = "123 Front Street"
        event.date = "2024-01-01"
        event.start_time = "16:00"
        event.end_time = "20:00"
        event.details = "Let's kick off 2024 with some fun"
        event.organizing_gamer = Gamer(pk=1)

        event.save()

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the event was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["location"], "123 Front Street")
        self.assertEqual(json_response["date"], "2024-01-01")
        self.assertEqual(json_response["start_time"], "16:00:00")
        self.assertEqual(json_response["end_time"], "20:00:00")
        self.assertEqual(json_response["details"], "Let's kick off 2024 with some fun")



    def test_change_event(self):
        """
        Ensure we can change an existing event.
        """
        event = Event()
        event.game = Game(pk=2)
        event.location = "123 Front Street"
        event.date = "2024-01-01"
        event.start_time = "16:00"
        event.end_time = "20:00"
        event.details = "Let's kick off 2024 with some fun"
        event.organizing_gamer = Gamer(pk=1)
        event.save()

        # DEFINE NEW PROPERTIES FOR EVENT
        data = {
            "game": 3,
            "location": "456 Back Street",
            "date": "2023-12-31",
            "start_time": "22:00",
            "end_time": "01:00",
            "details": "New Year's Eve games! Let's go!"
        }

        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET event again to verify changes were made
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["location"], "456 Back Street")
        self.assertEqual(json_response["date"], "2023-12-31")
        self.assertEqual(json_response["start_time"], "22:00:00")
        self.assertEqual(json_response["end_time"], "01:00:00")
        self.assertEqual(json_response["details"], "New Year's Eve games! Let's go!")



    def test_delete_event(self):
        """
        Ensure we can delete an existing event.
        """
        event = Event()
        event.game = Game(pk=3)
        event.location = "456 Back Street"
        event.date = "2023-12-31"
        event.start_time = "22:00"
        event.end_time = "01:00"
        event.details = "New Year's Eve games! Let's go!"
        event.organizing_gamer = Gamer(pk=1)
        event.save()

        # DELETE the event you just created
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the event again to verify you get a 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_delete_event_attendee(self):
        """
        Ensure we can delete an existing attendee from an event (leave).
        """
        event = Event()
        event.game = Game(pk=3)
        event.location = "456 Back Street"
        event.date = "2023-12-31"
        event.start_time = "22:00"
        event.end_time = "01:00"
        event.details = "New Year's Eve games! Let's go!"
        event.organizing_gamer = Gamer(pk=1)
        event.save()

        # DELETE the event you just created
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the event again to verify you get a 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_add_event_attendee(self):
        """
        Ensure we can add an existing attendee from an event (join).
        """
        event = Event()
        event.game = Game(pk=3)
        event.location = "456 Back Street"
        event.date = "2023-12-31"
        event.start_time = "22:00"
        event.end_time = "01:00"
        event.details = "New Year's Eve games! Let's go!"
        event.organizing_gamer = Gamer(pk=1)
        event.save()

        # DELETE the event you just created
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the event again to verify you get a 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)