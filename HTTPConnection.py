import random
from flask import Flask, request, jsonify
from GameObjects.GameObjects import Player, Game, Question

class HTTPConnection:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.externIpaddress = ""
        self.game = None
        self.games = []
        self.questions = []
        self.init_question_stack()

        # self.resetAllPlayerAnswers()
        # self.get_next_question()

    def run_server(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)

    def setup_routes(self):
        self.app.add_url_rule('/game/create', view_func=self.create_new_game, methods=['POST'])
        self.app.add_url_rule('/game/join', view_func=self.join_existing_game, methods=['POST'])
        self.app.add_url_rule('/game/getQuestion', view_func=self.get_question, methods=['GET'])
        self.app.add_url_rule('/game/sendAnswer', view_func=self.recieve_answer, methods=['POST'])
        self.app.add_url_rule('/game/getGameStatus', view_func=self.returnGameReslts, methods=['GET'])

    def create_new_game(self):

        try:
            data = request.get_json()
            if data:
                player_obj = Player(data.get('playerName'), data.get('playerId'))
                # Example: Print player's name and ID
                print(f"Player Name: {player_obj.playerName}")
                print(f"Player ID: {player_obj.playerId}")
                self.game = Game(player_obj)
                print(self.game.game_id)

                # for later use
                self.games.append(self.game)

                # Create a dictionary with information about the created game
                response_data = {
                    "message": "game Created",
                    "game_id": self.game.game_id,
                    "players": [
                        {"playerName": player.playerName, "playerId": player.playerId}
                        for player in self.game.players
                    ]
                }
                print(jsonify(response_data))

                # Return the response as JSON
                return jsonify(response_data)
            else:
                return jsonify({"message": "No JSON data received"})

        except Exception as e:
            print("Error processing JSON data:", e)
            return f"Error processing JSON data: {e}"

    def join_existing_game(self):
        try:
            data = request.get_json()
            if data:
                player_obj = Player(data.get('playerName'), data.get('playerId'))
                self.game.addPlayer(player_obj)
                # Create a dictionary with information about the created game
                response_data = {
                    "message": "Joined game",
                    "game_id": self.game.game_id,
                    "players": [
                        {"playerName": player.playerName, "playerId": player.playerId}
                        for player in self.game.players
                    ]
                }
                print(jsonify(response_data))
                # Return the response as JSON
                return jsonify(response_data)
            else:
                return jsonify({"message": "No JSON data received"})

        except Exception as e:
            print("Error processing JSON data:", e)
            return f"Error processing JSON data: {e}"

    def get_next_question(self):
        print("changing the question")
        self.game.question = random.choice(self.questions)

    def get_question(self):
        print("obtaining current Question")
        if self.game.question is None:
            self.resetAllPlayerAnswers()
            self.get_next_question()

        question = self.game.question
        response_data = {
            "message": "Question recieved",
            "question_text": question.questionText,
            "answer": question.answer,
            "unit": question.unit
        }

        return jsonify(response_data)

    def recieve_answer(self):
        data = request.get_json()
        player = self.search_player_by_id(data.get('playerId'))
        player.currentAnswer = data.get('answer')
        return "success"

    def returnGameReslts(self):
        print("Recived all")
        if self.allAnswersPresent():
            print("All Answers there")
            sortedPlayers = self.sort_players_by_proximity(self.game.question.answer)
            print(sortedPlayers)

            # return Game result, enter Next Question
            response_data = {
                "message": "Game results returned",
                "game_id": self.game.game_id,
                "correctAnswer": self.game.question.answer,
                "playerListSorted": [
                    {"playerName": player.playerName, "playerId": player.playerId, "currentAnswer": player.currentAnswer}
                    for player in sortedPlayers
                ]
            }
            print(response_data)
            self.game.question = None
            return jsonify(response_data)

        else:
            print("Not all players answered")
            # return some type of false

    # Function to sort players based on the proximity of their answers to the correct answer
    def sort_players_by_proximity(self, correct_answer):
        # Custom key function to calculate absolute difference between player's answer and correct answer
        def proximity_key(player):
            return abs(player.currentAnswer - correct_answer)

        # Sort players based on the proximity of their answers to the correct answer
        sorted_players = sorted(self.game.players, key=proximity_key)
        return sorted_players

    def allAnswersPresent(self):
        for player in self.game.players:
            if player.currentAnswer is "":
                return False
        return True

    def search_player_by_id(self, search_player_id):
        print("searching for ID" + str(search_player_id))
        for player in self.game.players:
            if player.playerId == search_player_id:
                return player
        return None

    def init_question_stack(self):
        # Creating 5 instances of Question class
        question1 = Question("Text1", 1, "unit1")
        question2 = Question("Text2", 2, "unit2")
        question3 = Question("Text3", 3, "unit3")
        question4 = Question("Text4", 4, "unit4")
        question5 = Question("Text5", 5, "unit5")

        self.questions.append(question1)
        self.questions.append(question2)
        self.questions.append(question3)
        self.questions.append(question4)
        self.questions.append(question5)

    def resetAllPlayerAnswers(self):
        for player in self.game.players:
            player.currentAnswer = ""


