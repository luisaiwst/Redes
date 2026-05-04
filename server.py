import socket
import threading
import datetime

clientes = {}

SALAS = {
    "1": "geral",
    "2": "games"
}

def horario():
    return datetime.datetime.now().strftime("%H:%M")

def handle_client(client_socket):

    msg = client_socket.recv(1024).decode()
    nome = msg.split(":")[1]

    clientes[client_socket] = {
        "nome": nome,
        "sala": None
    }

    print(f"[{horario()}] {nome} conectou")

    while True:
        try:
            data = client_socket.recv(1024).decode()

            if not data:
                nome = clientes[client_socket]["nome"]
                del clientes[client_socket]
                print(f"[{horario()}] {nome} desconectou")
                client_socket.close()
                break

            if data == "/usuarios":
                lista = ""
                for c in clientes.values():
                    lista += c["nome"] + " "
                client_socket.send(f"[{horario()}] Online: {lista}".encode())

            elif data == "/salas":
                client_socket.send(f"Salas: {', '.join(SALAS.values())}".encode())

            elif data == "/ajuda":
                client_socket.send("/usuarios /sala 1 /sala 2 /privado".encode())

            elif data in SALAS:
                clientes[client_socket]["sala"] = SALAS[data]
                client_socket.send(f"Entrou em {SALAS[data]}".encode())

            elif data.startswith("/privado"):
                partes = data.split(" ")
                destino = partes[1]

                mensagem = ""
                for i in range(2, len(partes)):
                    mensagem += partes[i] + " "

                for c in clientes:
                    if clientes[c]["nome"] == destino:
                        c.send(f"[{horario()}] [P] {nome}: {mensagem}".encode())

            else:
                nome = clientes[client_socket]["nome"]
                sala = clientes[client_socket]["sala"]

                if sala is None:
                    msg = f"[{horario()}] {nome}: {data}"

                    print(msg)

                    for c in clientes:
                        c.send(msg.encode())

                else:
                    msg = f"[{horario()}] [{sala}] {nome}: {data}"

                    print(msg)

                    for c in clientes:
                        if clientes[c]["sala"] == sala:
                            c.send(msg.encode())

        except:
            break


def start_server():
    s = socket.socket()
    s.bind(("127.0.0.1", 5005))
    s.listen()

    print("Servidor rodando")

    while True:
        c, addr = s.accept()
        threading.Thread(target=handle_client, args=(c,), daemon=True).start()


start_server()