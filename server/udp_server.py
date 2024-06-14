import socket
import pygame
import time
import re
import numpy as np

# UDP_IP = "127.0.0.1"
UDP_IP = "0.0.0.0"
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
        
        self.last_act = [None] * len(player_ids)

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
        # if actions[0] == -1:
        #     # check alive
        #     self._check_alive()
        #     return

        for i, act in enumerate(actions):
            if (act != self.last_act[i]).any():
                # seed only when state changed
                print("motor_vec", act)
                self.last_act[i] = act
                data = f"[DATA]".encode("utf-8")
                # for a in act:
                for j in range(4):
                    a = act[j]
                    a = min(a, 255)
                    a = max(a, -255)
                    data = data + int(a).to_bytes(2, byteorder='little', signed=True)
                # if act == 0:
                #     # no action
                #     data = "[DATA]0".encode("utf-8")
                # elif act == 1:
                #     # move forward
                #     data = "[DATA]1".encode("utf-8")
                # elif act == -1:
                    # check alive
                print("send to", self.player_addresses[i], data)
                self.sock.sendto(data, self.player_addresses[i])
        
def get_vec(k):
    # if keys[pygame.K_q]:
    v = 255
    if k == pygame.K_q:
        a = -v
        b = +v
        # server.step([(a, b, b, a),])
        motor_vec = (a, b, b, a)
    # elif keys[pygame.K_e]:
    elif k == pygame.K_e:
        a = v
        b = -v
        # server.step([(a, b, b, a),])
        motor_vec = (a, b, b, a)
    else:
        # if keys[pygame.K_w]:
        if k == pygame.K_w:
            # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            # server.step([(255, 255, 255, 255),])
            l, r = v, v
        # elif keys[pygame.K_s]:
        elif k == pygame.K_s:
            # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            # server.step([(l, r, l, r),])
            l, r = -v, -v
        # elif keys[pygame.K_a]:
        elif k == pygame.K_a:
            # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            # server.step([(255, -255, 255, -255),])
            l = v
            r = -v
        # elif keys[pygame.K_d]:
        elif k == pygame.K_d:
            # sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
            l = -v
            r = v
        else:
            l = 0
            r = 0
            # server.step([(0, 0, 0, 0),])
        
        motor_vec = (l, r, l, r)
    
    return np.array(motor_vec)

if __name__ == '__main__':
    # Initialize Pygame
    pygame.init()
    joystick_num = pygame.joystick.get_count()
    js = None
    if joystick_num > 0:
        js = pygame.joystick.Joystick(0)
        js.init()
        n_axes = js.get_numaxes()
        print("has joystick", n_axes)
        
    server = GameServer([0,], (UDP_IP, UDP_PORT))


    # Set up the display
    screen = pygame.display.set_mode((640, 480))

    # Main loop
    running = True
        
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check every 100ms
        time.sleep(0.001)

        # Check if 'A' key is pressed
        # joystick
        if js is not None:
            pass
        else:
            keys = pygame.key.get_pressed()
            motor_vec = np.array([0, 0, 0, 0])
            for k in [pygame.K_q, pygame.K_e, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]:
                if keys[k]:
                    motor_vec = motor_vec + get_vec(k)
                    # print("add", k, motor_vec)
                    # break
        if np.abs(motor_vec).max() > 0:
            motor_vec = motor_vec / np.abs(motor_vec).max() * 100
        motor_vec.astype(np.int32)
        server.step([motor_vec])

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()