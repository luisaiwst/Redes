import socket


HOST = "127.0.0.1"
PORT = 5005

s = socket.socket()
s.connect((HOST, PORT))

nome = input("nome: ")
s.send(("LOGIN:" + nome).encode())

def ouvir():
    while True:
        try:
            msg = s.recv(1024).decode()
            print(msg)
        except:
            break

threading.Thread(target=ouvir, daemon=True).start()

while True:
    msg = input()
    s.send(msg.encode())