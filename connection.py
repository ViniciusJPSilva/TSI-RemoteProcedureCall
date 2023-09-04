import socket

BUFFER_SIZE = 4096
STD_PORT = 14000
LOCAL_HOST = "127.0.0.1"

STD_ENCODE = "UTF-8"

def create_server_connection(port: int = STD_PORT) -> socket.socket:
    """
    Cria e configura um socket do servidor.

    :param port: Número da porta do servidor.
    :return: Socket do servidor configurado.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", port))
    server_socket.listen(0)

    return server_socket

# create_server_connection()


def create_client_connection(server_ip: str, port: int = STD_PORT) -> socket.socket:
    """
    Cria uma conexão de cliente para o servidor.

    :param server_ip: Endereço IP do servidor.
    :param port: Número da porta do servidor.
    :return: Conexão do cliente.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    return client_socket

# create_client_connection()


def receive_socket_message(receiver_socket: socket.socket) -> str:
    """
    Recebe uma mensagem de um soquete.

    :param receiver_socket: O soquete para receber a mensagem.
    :return: A mensagem recebida como uma string decodificada.
    """
    full_message = b""
    while True:
        chunk = receiver_socket.recv(BUFFER_SIZE)
        if not chunk:
            break
        
        full_message += chunk

        if len(chunk) < BUFFER_SIZE:
            break

    return full_message.decode(STD_ENCODE)
    
# receive_socket_message()