from gui.app import App
from rpc import name_server
from rpc.client import Client

def main() -> None:
    with Client((name_server.NAME_SERVER_STD_ADDR)) as client:
        App(client).mainloop()

if __name__ == "__main__":
    main()