from remote_procedure_call import Server

def start_server() -> None:
    server = Server()
    
    server.start()

if __name__ == "__main__":
    start_server()