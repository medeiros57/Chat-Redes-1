import socket
import threading

# define uma senha
SECRET_KEYWORD = "melancia"

# armazena os clientes conectados
clients = {}

# função para lidar com a comunicação de cada cliente
def handle_client(client_socket, name):
    global clients
    try:
        client_socket.send("Conectado com sucesso! Digite 'LIST' para ver os usuários online ou envie uma mensagem no formato '@nome: mensagem'. Para enviar uma mensagem para todos, use '@all: mensagem'\n".encode())
        
        while True:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break

            if msg.strip().upper() == "LIST":
                # envia a lista de usuários conectados
                client_list = "Usuários online: " + ", ".join(clients.keys()) + "\n"
                client_socket.send(client_list.encode())
            elif msg.startswith("@"):
                # envia uma mensagem para um usuário específico ou para todos
                try:
                    recipient_name, message = msg[1:].split(":", 1)
                    recipient_name = recipient_name.strip()
                    if recipient_name.lower() == "all":
                        for client_name, client in clients.items():
                            if client != client_socket:
                                client.send(f"[{name} para todos] {message.strip()}\n".encode())
                    elif recipient_name in clients:
                        clients[recipient_name].send(f"[{name}] {message.strip()}\n".encode())
                    else:
                        client_socket.send(f"Usuário '{recipient_name}' não encontrado.\n".encode())
                except ValueError:
                    client_socket.send("Formato da mensagem incorreto. Use '@nome: mensagem'.\n".encode())
            else:
                client_socket.send("Comando não reconhecido. Digite 'LIST' para ver os usuários online ou envie uma mensagem no formato '@nome: mensagem'. Para enviar uma mensagem para todos, use '@all: mensagem'\n".encode())
    except Exception as e:
        print(f"Erro no handle_client: {e}")
    finally:
        print(f"[DESCONECTADO] {name} desconectado.")
        clients.pop(name, None)
        client_socket.close()

# função principal do servidor
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind(("0.0.0.0", 55555))
    except socket.error as e:
        print(f"Erro ao ligar o servidor na porta 5555: {e}")
        server.close()
        return
    
    server.listen(5)
    print("[INICIANDO] Servidor iniciado e aguardando conexões...")

    while True:
        client_socket, addr = server.accept()
        
        client_socket.send("Digite seu nome: ".encode())
        name = client_socket.recv(1024).decode().strip()
        
        if name in clients:
            client_socket.send("Nome já está em uso. Desconectando...\n".encode())
            client_socket.close()
            continue

        client_socket.send("Digite a palavra-chave para se conectar: ".encode())
        keyword = client_socket.recv(1024).decode()
        
        if keyword.strip() != SECRET_KEYWORD:
            client_socket.send("Palavra-chave incorreta. Desconectando...\n".encode())
            client_socket.close()
            continue

        clients[name] = client_socket
        print(f"[NOVA CONEXÃO] {addr} conectado como {name}.")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, name))
        client_handler.start()

if __name__ == "__main__":
    start_server()
