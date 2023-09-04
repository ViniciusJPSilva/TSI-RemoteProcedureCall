import socket

BUFFER_SIZE = 4096
STD_PORT = 14000
LOCAL_HOST = "127.0.0.1"

STD_ENCODE = "UTF-8"
STD_BYTE_ORDER = "big"
DATA_LENGTH_RESERVED_BYTES = 4

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
    length_bytes = receiver_socket.recv(DATA_LENGTH_RESERVED_BYTES)
    
    if not length_bytes:
        return None
    
    length = int.from_bytes(length_bytes, byteorder = STD_BYTE_ORDER)

    message = b""
    while len(message) < length:
        chunk = receiver_socket.recv(length - len(message))
       
        if not chunk:
            break  
        
        message += chunk

    return message.decode(STD_ENCODE)
    
# receive_socket_message()


def send_socket_message(sender_socket: socket.socket, message: str) -> None:
    """
    Envia uma mensagem através de um soquete.

    :param sender_socket: O soquete usado para enviar a mensagem.
    :param message: A mensagem a ser enviada como uma string.
    :return: Nenhum valor é retornado.
    """
    message_bytes = message.encode(STD_ENCODE)
    length = len(message_bytes).to_bytes(DATA_LENGTH_RESERVED_BYTES, byteorder = STD_BYTE_ORDER)

    sender_socket.sendall(length + message_bytes)

# send_socket_message()