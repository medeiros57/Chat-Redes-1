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
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            break

# função principal do cliente
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 55555))

    # envia o nome do usuário
    msg = client.recv(1024).decode()
    print(msg)
    name = input()
    client.send(name.encode())

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
        try:
            msg = input()
            if msg.strip().lower() == 'quit':
                break
            client.send(msg.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            break

    client.close()

if __name__ == "__main__":
    start_client()
