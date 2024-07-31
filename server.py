import socket
import threading

host = '127.0.0.1'  # Localhost
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message, sender_client=None):
    for client in clients:
        if client != sender_client:
            try:
                client.send(message)
            except:
                handle_disconnect(client)

def handle_disconnect(client):
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)
        client_ip = client.getpeername()
        client.close()
        broadcast(f'{nickname} dejó el chat!'.encode('utf-8'))
        print(f'{nickname} (IP: {client_ip}) se ha desconectado.')

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                handle_disconnect(client)
                break
            broadcast(message, client)
        except:
            handle_disconnect(client)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Conectado con la IP {str(address)}')

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'El nickname del cliente es {nickname}')
        broadcast(f'{nickname} se unió al chat!'.encode('utf-8'))
        client.send('Te has conectado correctamente al servidor!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print('Servidor listo para operar....')
receive()