import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Gamer, Event, Attendee, Game
from rest_framework.authtoken.models import Token


class GameTypeTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events', 'attendees']

    def setUp(self):
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


    def test_get_GameType(self):
        """
        Ensure we can get an existing GameType.
        """

        # Seed the database with a game
        game_type = GameType()
        game_type.label = "Card Game"

        game_type.save()

        # Initiate request and store response
        response = self.client.get(f"/gametypes/{game_type.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game_type was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["label"], "Card Game")