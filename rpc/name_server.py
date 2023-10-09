import web_utils.connection as connection
from rpc.servers_list import OPERATION_SERVERS
import json

NAME_SERVER_STD_IP = "127.0.0.1"
NAME_SERVER_STD_PORT = 15000

NAME_SERVER_STD_ADDR = (NAME_SERVER_STD_IP, NAME_SERVER_STD_PORT)

class NameServer:
    def __init__(self, ip: str = NAME_SERVER_STD_IP, port: int = NAME_SERVER_STD_PORT):
        """
        Inicializa um servidor de nomes com o ip e o número da porta.

        :param port: Número da porta do servidor.
        """
        self.ip = ip
        self.port = port
        self.server_socket = None
        self.operation_servers = OPERATION_SERVERS

    def __del__(self):
        """
        Fecha o socket do servidor ao destruir o objeto.
        """
        if self.server_socket: 
            self.server_socket.close()


    def start(self) -> None:
        """
        Inicia o servidor de nomes e espera por conexões de clientes.
        """
        self.server_socket = connection.create_server_connection(self.ip, self.port, False)
        print(f"O servidor de nomes está ouvindo na porta {self.port}...")
        
        try:
            while True:
                operation, address = connection.receive_udp_socket_message(self.server_socket)
                print(address)
                server_list = [server for server, operations in self.operation_servers.items() if operation.decode() in operations]
                connection.send_udp_socket_message(self.server_socket, json.dumps(server_list), address)
        except KeyboardInterrupt:
            print("\nO servidor foi finalizado...")
        finally:
            self.server_socket.close()


    def close(self) -> None:
        """
        Fecha o socket do servidor ao fechar o objeto.
        """
        if self.server_socket: 
            self.server_socket.close()