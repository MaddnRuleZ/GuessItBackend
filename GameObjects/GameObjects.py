import random

class Game:
    def __init__(self, player1):
        self.game_id = self.generate_game_id()  # Generate game ID
        self.players = [player1]  # List to store players
        self.question = None

    def generate_game_id(self):
        # Generate a 5-digit random integer for game ID
        return random.randint(10000, 99999)

    def addPlayer(self, player):
        self.players.append(player)

class Player:
    def __init__(self, playerName, playerId):
        self.playerName = playerName
        self.playerId = playerId
        self.currentAnswer = ""

class Question:
    def __init__(self, questionText, answer, unit):
        self.questionText = questionText
        self.answer = answer
        self.unit = unit
        self.usedThisGame = False
