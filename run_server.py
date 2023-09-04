from remote_procedure_call import Server

def start_server() -> None:
    try: 
        server = Server()
        server.start()
    except KeyboardInterrupt:
        server.close()

if __name__ == "__main__":
    start_server()