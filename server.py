import socket
import datetime

clientes = {}

SALAS = {"1": "geral", "2": "games"}

def horario():
    return datetime.datetime.now().strftime("%H:%M")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("127.0.0.1", 5005))

print("Servidor UDP rodando")

while True:
    data_raw, addr = s.recvfrom(1024)
    data = data_raw.decode()

    if data.startswith("LOGIN:"):
        nome = data.split(":")[1]
        clientes[addr] = {"nome": nome, "sala": None}
        print(f"[{horario()}] {nome} {addr} conectou")
        continue

    if addr not in clientes:
        continue

    nome = clientes[addr]["nome"]

    if data == "/usuarios":
        lista = " ".join([c["nome"] for c in clientes.values()])
        s.sendto(f"[{horario()}] Online: {lista}".encode(), addr)

    elif data == "/salas":
        s.sendto(f"Salas: {', '.join(SALAS.values())}".encode(), addr)

    elif data in SALAS:
        clientes[addr]["sala"] = SALAS[data]
        s.sendto(f"Entrou em {SALAS[data]}".encode(), addr)

    elif data.startswith("/privado"):
        partes = data.split(" ")
        destino = partes[1]
        mensagem = " ".join(partes[2:])
        for c_addr, c_info in clientes.items():
            if c_info["nome"] == destino:
                s.sendto(f"[{horario()}] [P] {nome}: {mensagem}".encode(), c_addr)

    else:
        sala = clientes[addr]["sala"]
        msg = f"[{horario()}] [{'Geral' if sala is None else sala}] {nome}: {data}"
        print(msg)
        
        for c_addr, c_info in clientes.items():
            if c_info["sala"] == sala:
                s.sendto(msg.encode(), c_addr)