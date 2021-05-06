"""
Handles operations in game
"""
from board import Board
from round import Round
import random as r


class Game(object):
    def __init__(self, id, players):
        self.id = id
        self.players = players
        self.words_used = set()
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        self.round_count = 1
        self.start_new_round()

    def start_new_round(self):
        try:
            round_word = self.get_word()
            self.round = Round(round_word, self.players[self.player_draw_ind], self)
            self.round_count += 1

            if self.player_draw_ind >= len(self.players):
                self.end_round()
                self.end_game()

            self.player_draw_ind += 1
        except Exception as e:
            self.end_game()

    def player_guess(self, player, guess):
        return self.round.guess(player, guess)

    def player_disconnected(self, player):
        """
        Очистка объектов когда игрок отключается
        :param player: Player
        :return: Exception()
        """
        if player in self.players:
            
            self.players.remove(player)
            self.round.player_left(player)
            self.round.chat.update_chat(f"Player {player.get_name()} disconnected.")
        else:
            raise Exception("Player not in game")

        if len(self.players) <= 2:
            self.end_game()

    def skip(self, player):
        if self.round:
            new_round = self.round.skip(player)
            if new_round:
                self.round.chat.update_chat(f"Round has been skipped.")
                self.end_round()
                return True
            return False
        else:
            raise Exception("No round started yet")

    def end_round(self):
        self.round.chat.update_chat(f"Round {self.round_count} has ended.")
        self.start_new_round()
        self.board.clear()

    def update_board(self, x, y, color):
        if not self.board:
            raise Exception("No board created")
        self.board.update(x, y, color)

    def end_game(self):
        print(f"[GAME] Game {self.id} end")
        for player in self.players:
            player.game = None

    def get_word(self):
        with open('words.txt', "r", encoding='utf-8') as f:
            words = []
            for line in f:
                wrd = line.strip()
                if wrd not in self.words_used:
                    words.append(line.strip())

            self.words_used.add(wrd)

            rand = r.randint(0, len(words)-1)
            return words[rand].strip()

    def get_player_scores(self):
        scores = {player.get_name(): player.get_score() for player in self.players}
        return scores
