"""
Главный поток
Обрабатывает все соединения
"""

import socket
import threading
from player import Player
from game import Game
import json


class Server(object):
    PLAYERS = 4

    def __init__(self):
        self.connection_queue = []
        self.game_id = 0

    def player_thread(self, conn, player):
        while True:
            try:
                try:
                    data = conn.recv(1024)
                    data = json.loads(data.decode())
                    #print("[LOG] Recieved data:", data)
                except Exception as e:
                    break

                keys = [int(key) for key in data.keys()]
                send_msg = {key: [] for key in keys}
                last_board = None

                for key in keys:
                    if key == -1:  # get game, return players list
                        if player.game:
                            send = {player.get_name(): player.get_score() for player in player.game.players}
                            send_msg[-1] = send
                        else:
                            send_msg[-1] = []

                    if player.game:
                        if key == 0:  # guess
                            correct = player.game.player_guess(player, data['0'][0])
                            send_msg[0] = correct
                        elif key == 1:  # skip
                            skip = player.game.skip(player)
                            send_msg[1] = skip
                        elif key == 2:  # get chat
                            content = player.game.round.chat.get_chat()
                            send_msg[2] = content
                        elif key == 3:  # get board
                            board = player.game.board.get_board()
                            if last_board != board:
                                last_board = board
                                send_msg[3] = board
                        elif key == 4:  # get score
                            scores = player.game.get_player_scores()
                            send_msg[4] = scores
                        elif key == 5:  # get round
                            round = player.game.round_count
                            send_msg[5] = round
                        elif key == 6:  # get word
                            word = player.game.round.word
                            send_msg[6] = word
                        elif key == 7:  # get skips
                            skips = player.game.round.skips
                            send_msg[7] = skips
                        elif key == 8:  # update board
                            if player.game.round.player_drawing == player:
                                x, y, color = data['8'][:3]
                                player.game.update_board(x, y, color)
                        elif key == 9:  # get round time
                            t = player.game.round.time
                            send_msg[9] = t
                        elif key == 10: # clear board
                            player.game.board.clear()
                        elif key == 11:
                            send_msg[11] = player.game.round.player_drawing == player

                send_msg = json.dumps(send_msg)
                conn.sendall(send_msg.encode() + ".".encode())

            except Exception as e:
                print(f"[EXCEPTION] {player.get_name()}:", e)
                break

        if player.game:
            player.game.player_disconnected(player)

        if player in self.connection_queue:
            self.connection_queue.remove(player)

        print(f"[DISCONNECT] {player.get_name()} DISCONNECTED")
        conn.close()

    def handle_queue(self, player):
        self.connection_queue.append(player)

        if len(self.connection_queue) >= self.PLAYERS:
            game = Game(self.game_id, self.connection_queue[:])

            for p in game.players:
                p.set_game(game)

            self.game_id += 1
            self.connection_queue = []
            print(f"[GAME] Game {self.game_id} started...")

    def authentication(self, conn, addr):
        try:
            data = conn.recv(1024)
            name = str(data.decode())
            if not name:
                raise Exception("No name received")

            conn.sendall("1".encode())

            player = Player(addr, name)
            self.handle_queue(player)
            thread = threading.Thread(target=self.player_thread, args=(conn, player))
            thread.start()
        except Exception as e:
            print("[EXCEPTION]", e)
            conn.close()

    def connection_thread(self):
        server = "localhost"
        port = 5555

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)

        s.listen()
        print("Waiting for a connection, Server Started")

        while True:
            conn, addr = s.accept()
            print("[CONNECT] New connection!")

            self.authentication(conn, addr)


if __name__ == "__main__":
    s = Server()
    thread = threading.Thread(target=s.connection_thread)
    thread.start()
