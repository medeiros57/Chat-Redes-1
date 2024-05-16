import socket
import threading

# define a senha
SECRET_KEYWORD = "melancia"

# lista para armazenar os clients
clients = []

# função para lidar com a comunicação de cada cliente
def handle_client(client_socket, addr):
    global clients
    print(f"[NOVA CONEXÃO] {addr} conectado.")
    try:
        # autenticação do cliente. Nome não é verificado, coloquei apenas para cada usuário ter um nome reconhecivel
        client_socket.send("Digite seu nome: ".encode())
        name = client_socket.recv(1024).decode().strip()

        client_socket.send("Digite a senha para se conectar: ".encode())
        keyword = client_socket.recv(1024).decode()
        
        if keyword.strip() != SECRET_KEYWORD:
            client_socket.send("Senha incorreta. Desconectando...".encode())
            client_socket.close()
            return
        
        client_socket.send("Conectado com sucesso! Você pode começar a conversar.".encode())
        clients.append((client_socket, name))
        
        while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            print(f"[{name}] {msg.decode()}")
            # envia a mensagem para todos os clientes, exceto o remetente
            for client, client_name in clients:
                if client != client_socket:
                    client.send(f"[{name}] {msg.decode()}".encode())
    except:
        pass
    finally:
        print(f"[DESCONECTADO] {name} desconectado.")
        clients = [(client, client_name) for client, client_name in clients if client != client_socket]
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
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    start_server()
