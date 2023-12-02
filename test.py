from rpc import name_server
import web_utils.connection as connection
import rpc.tasks as tasks
from tools.cpf import CPF

def test_server():
    socket = connection.create_client_connection("0.0.0.0", is_tcp = False)
    connection.send_udp_socket_message(socket, "teste", (connection.LOCAL_HOST, name_server.NAME_SERVER_STD_PORT))

    print(connection.receive_udp_socket_message(socket)[0].decode())
    socket.close()

def test_cpf():
    print(CPF.validate("22316444106"))


if __name__ == "__main__":
    test_cpf()