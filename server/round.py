"""
round of the game
"""
import time as t
from _thread import *
from chat import Chat


class Round(object):
    def __init__(self, word, player_drawing, game):
        self.word = word
        self.player_drawing = player_drawing
        self.player_guessed = []
        self.players_skipped = []
        self.skips = 0
        self.game = game
        self.player_scores = {player: 0 for player in self.game.players}
        self.time = 75
        self.chat = Chat(self)
        start_new_thread(self.time_thread, ())

    def time_thread(self):
        while self.time > 0:
            t.sleep(1)
            self.time -= 1
        self.end_round("Time is up")

    def skip(self, player):
        if player not in self.players_skipped:
            self.players_skipped.append(player)
            self.skips += 1
            self.chat.update_chat(f"Player has voted to skip ({self.skips}/{len(self.game.players) - 2}")
            if self.skips >= len(self.game.players) - 2:
                return True

        return False

    def get_scores(self):
        return self.player_scores

    def get_score(self, player):
        if player in self.player_scores:
            return self.player_scores[player]
        else:
            raise Exception("Player not in score list")

    def guess(self, player, word):
        """
        :returns bool если игрок дал правильный ответ
        :param player: Player
        :param word: str
        :return: bool
        """
        correct = word == self.word
        if correct:
            self.player_guessed.append(player)
            self.chat.update_chat(f"{player.name} has guessed the word.")
            return True
        
        self.chat.update_chat(f"{player.name} guessed {word}")
        return False

    def player_left(self, player):
        if player in self.player_scores:
            del self.player_scores[player]

        if player in self.player_guessed:
            self.player_guessed.remove(player)

        if player == self.player_drawing:
            self.chat.update_chat(f"Round hs been skipped because the drawing player left.")
            self.end_round("Drawing player leaves")

    def end_round(self, msg):
        for player in self.game.players:
            if player in self.player_scores:
                player.update_score(self.player_scores[player])
        self.game.end_round()
