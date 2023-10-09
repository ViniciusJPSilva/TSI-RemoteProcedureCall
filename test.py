from rpc import name_server
import web_utils.connection as connection
import rpc.tasks as tasks

socket = connection.create_client_connection("0.0.0.0", is_tcp = False)
connection.send_udp_socket_message(socket, "teste", (connection.LOCAL_HOST, name_server.NAME_SERVER_STD_PORT))

print(connection.receive_udp_socket_message(socket)[0].decode())
socket.close()
