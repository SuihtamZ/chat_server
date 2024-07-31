import socket
import threading

nickname = input("Ingresa tu nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print('Ocurrió un error!')
            client.close()
            break

def write():
    while True:
        message = input()
        if message.lower() == 'salir':
            client.send(f'{nickname} dejó el chat!'.encode('utf-8'))
            client.close()
            print('Te has desconectado del servidor.')
            break
        client.send(f'{nickname}: {message}'.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
                