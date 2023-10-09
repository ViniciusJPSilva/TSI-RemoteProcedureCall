from rpc.name_server import NameServer

def start_server() -> None:
    try: 
        server = NameServer()
        server.start()
    except KeyboardInterrupt:
        server.close()

if __name__ == "__main__":
    start_server()