from rpc.server import Server
from rpc.servers_list import SERVERS_LIST

def start_server() -> None:
    try: 
        server = Server(port = SERVERS_LIST[0][1])
        server.start()
    except KeyboardInterrupt:
        server.close()

if __name__ == "__main__":
    start_server()
