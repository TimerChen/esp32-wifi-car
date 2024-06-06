import socket
SERVER_PORT = 5005
UDP_IP = "127.0.0.1"
UDP_PORT = 5006

# send to server: JOIN
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(b"[JOIN]0", (UDP_IP, SERVER_PORT))

# recv
# sock = socket.socket(socket.AF_INET, # Internet
#                      socket.SOCK_DGRAM) # UDP
# sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: %s" % data)