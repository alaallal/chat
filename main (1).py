
import socket
import threading

clients = []
separator_token = "<SEP>"

def handle_client(client_socket, address):
    print(f"Подключен {address}")
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                # Отправляем сообщение всем клиентам
                broadcast(msg, client_socket)
            else:
                remove(client_socket)
                break
        except:
            continue

def broadcast(message, client_socket):
    for client in clients:
        # Отправляем сообщение и добавляем имя клиента перед сообщением
        if client != client_socket:
            try:
                client.send(message.encode())
            except:
                remove(client)

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8000))
    server_socket.listen(5)
    print("Сервер запущен и ждет подключения...")

    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, address)).start()

start_server()

