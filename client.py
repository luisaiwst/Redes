import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 5005
ADDR = (HOST, PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

nome = input("nome: ")
s.sendto(f"LOGIN:{nome}".encode(), ADDR)

def ouvir():
    while True:
        try:
            msg, _ = s.recvfrom(1024)
            sys.stdout.write("\033[A\033[K")
            sys.stdout.flush()
            print(msg.decode())
        except:
            break

threading.Thread(target=ouvir, daemon=True).start()

while True:
    msg = input()
    s.sendto(msg.encode(), ADDR)
    if not msg:
        sys.stdout.write("\033[A\033[K")
        sys.stdout.flush()