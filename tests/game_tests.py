import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Gamer, Game
from rest_framework.authtoken.models import Token


class GameTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events', 'attendees']

    def setUp(self):
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/games"

        # Define the request body
        data = {
            "type": 1,
            "name": "Clue",
            "length": 3.5,
            "min_age": 6,
            "min_players": 1,
            "max_players": 10,
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["name"], "Clue")
        self.assertEqual(json_response["length"], "3.5")
        self.assertEqual(json_response["min_age"], 6)
        self.assertEqual(json_response["min_players"], 1)
        self.assertEqual(json_response["max_players"], 10)



    def test_get_game(self):
        """
        Ensure we can get an existing game.
        """

        # Seed the database with a game
        game = Game()
        gamer = Gamer(pk=1)
        game.gamer = gamer
        type = GameType(pk=1)
        game.type = type
        game.name = "Monopoly"
        game.length = 5.0
        game.min_age = 8
        game.min_players = 2
        game.max_players = 8

        game.save()

        # Initiate request and store response
        response = self.client.get(f"/games/{game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["name"], "Monopoly")
        self.assertEqual(json_response["length"], "5.0")
        self.assertEqual(json_response["min_age"], 8)
        self.assertEqual(json_response["min_players"], 2)
        self.assertEqual(json_response["max_players"], 8)



    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        game = Game()
        type = GameType(pk=1)
        game.type = type
        game.name = "Monopoly"
        game.length = 5.0
        game.min_age = 8
        game.min_players = 2
        game.max_players = 8
        gamer = Gamer(pk=1)
        game.gamer = gamer
        game.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "type": 1,
            "name": "Monopoly 2",
            "length": 6.5,
            "min_age": 12,
            "min_players": 2,
            "max_players": 8,
        }

        response = self.client.put(f"/games/{game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET game again to verify changes were made
        response = self.client.get(f"/games/{game.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "Monopoly 2")
        self.assertEqual(json_response["length"], "6.5")
        self.assertEqual(json_response["min_age"], 12)
        self.assertEqual(json_response["min_players"], 2)
        self.assertEqual(json_response["max_players"], 8)



    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """
        game = Game()
        game.type = GameType(pk=1)
        game.name = "Monopoly 2"
        game.length = 6.5
        game.min_age = 12
        game.min_players = 2
        game.max_players = 8
        game.gamer = Gamer(pk=1)
        game.save()

        # DELETE the game you just created
        response = self.client.delete(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the game again to verify you get a 404 response
        response = self.client.get(f"/games/{game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)