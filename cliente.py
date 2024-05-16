import socket
import threading

# função para receber mensagens do servidor
def receive_messages(client_socket):
    while True:
        try:
            msg = client_socket.recv(1024)
            if not msg:
                break
            print(msg.decode())
        except:
            break

#função principal do cliente
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 55555))

    # recebe e envia a senha
    msg = client.recv(1024).decode()
    print(msg)
    keyword = input()
    client.send(keyword.encode())

    # inicia uma thread para receber mensagens do servidor
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    # envia mensagens para o servidor
    while True:
        msg = input()
        client.send(msg.encode())

if __name__ == "__main__":
    start_client()
