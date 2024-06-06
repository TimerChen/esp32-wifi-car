import socket
import pygame
import time
import re

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
MESSAGE = b"Hello, World!"

print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)


class GameServer():
    def __init__(self, player_ids, addr):
        self.UDP_IP = "0.0.0.0"
        self.UDP_PORT = 5005
        self.MESSAGE = b"Hello, World!"
        self.players_ids = player_ids
        self.player_addresses = [None] * len(player_ids)
        self.sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
        self.player_socks = [None] * len(player_ids)
        self.sock.bind(addr)
        self.reset()

    def _wait_player(self,):
        while None in self.player_addresses:
            data, addr = self.sock.recvfrom(1024)
            data = data.decode("utf-8")
            print(f"Waiting for player {data}")
            if data.startswith("[JOIN]"):
                # example: [JOIN]0,5006
                # player_id, port = data[6:].split(',')
                # player_id = int(player_id)
                # port = int(port)
                player_id = int(data[6:])
                if player_id in self.players_ids:
                    i = self.players_ids.index(player_id)
                    self.player_addresses[i] = addr
                    # self.player_socks[i] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    # self.player_socks[i].bind(addr)
                    print(f"[INFO] Player {player_id} joined.")
                
                    
        print("[INFO] All Players Joined.")

    def reset(self,):
        self.player_addresses = [None] * len(self.players_ids)
        self.player_socks = [None] * len(self.players_ids)
        self._wait_player()

    def _check_alive(self,):
        for i, addr in enumerate(self.player_addresses):
            self.sock.sendto(b"[ALIVE]", addr)
            
            # recv with timelimit
            self.player_socks[i].settimeout(1)
            try:
                data, addr = self.sock.recvfrom(1024)
                data = data.decode("utf-8")
            except socket.timeout:
                print(f"[ERROR] player {i} is timeout.")
                return False

            if data != b"[ALIVE]":
                return False
        return True

    def step(self, actions):
        if actions[0] == -1:
            # check alive
            self._check_alive()
            return

        for i, act in enumerate(actions):
            if act == 0:
                # no action
                data = "[DATA]0".encode("utf-8")
            elif act == 1:
                # move forward
                data = "[DATA]1".encode("utf-8")
            # elif act == -1:
                # check alive
            print("send to", self.player_addresses[i], data)
            self.sock.sendto(data, self.player_addresses[i])
        


if __name__ == '__main__':
    server = GameServer([0,], (UDP_IP, UDP_PORT))

    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((640, 480))

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check every 100ms
        time.sleep(0.1)

        # Check if 'A' key is pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            server.step([1,])
        else:
            server.step([0,])
            

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()