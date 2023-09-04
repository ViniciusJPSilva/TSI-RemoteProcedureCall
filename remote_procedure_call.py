from re import sub
import connection
import threading
import json
from typing import Tuple, Any

SUM = "__SUM__"
SUB = "__SUB__"
MUL = "__MUL__"
DIV = "__DIV__"

END = "__END__"

ERR = "__ERROR__"
ERR_DIV_BY_ZERO = "__ERR_DIV_0__"

JSON_KEY_TASK = "task"
JSON_KEY_ARGS = "args"
JSON_KEY_RESS = "result"


class Client:
    """
    Classe para criar um cliente que se conecta 
    a um servidor remoto para executar operações.
    """

    def __init__(self, server_ip: str = connection.LOCAL_HOST, 
                 server_port: int = connection.STD_PORT):
        """
        Inicializa um cliente com o endereço do servidor e o número da porta.

        :param server_ip: Endereço IP do servidor.
        :param server_port: Número da porta do servidor.
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = connection.create_client_connection(server_ip, server_port)

    def __del__(self):
        """
        Fecha a conexão do cliente com o servidor ao destruir o objeto.
        """
        self.close()

    def close(self):
        """
        Fecha a conexão do cliente com o servidor.
        """
        self.client_socket.close()

    def __send_request(self, operation: str, args):
        request = {
            JSON_KEY_TASK: operation,
            JSON_KEY_ARGS: args
        }
        request_str = json.dumps(request)
        self.client_socket.sendall(request_str.encode(connection.STD_ENCODE))

        response_str = connection.receive_socket_message(self.client_socket)
        response = json.loads(response_str)

        return response

    def sum(self, *args: float) -> float:
        """
        Envia uma solicitação de soma para o servidor e retorna o resultado.

        :param args: Números a serem somados.
        :return: Resultado da soma.
        """
        response = self.__send_request(SUM, args)
        try:
            return float(response[JSON_KEY_RESS])
        except Exception:
            raise Exception("Argumentos inválidos!")
        

    def sub(self, *args: float) -> float:
        """
        Envia uma solicitação de subtração para o servidor e retorna o resultado.

        :param args: Números a serem usados na subtração.
        :return: Resultado da subtração.
        """
        response = self.__send_request(SUB, args)
        
        try:
            return float(response[JSON_KEY_RESS])
        except Exception as error:
            raise Exception("Argumentos inválidos!")
        
        
    def mul(self, *args: float) -> float:
        """
        Envia uma solicitação de multiplicação para o servidor e retorna o resultado.

        :param args: Números a serem usados na multiplicação.
        :return: Resultado da multiplicação.
        """
        response = self.__send_request(MUL, args)
        try:
            return float(response[JSON_KEY_RESS])
        except Exception:
            raise Exception("Argumentos inválidos!")
        

    def div(self, *args: float) -> float:
        """
        Envia uma solicitação de divisão para o servidor e retorna o resultado.

        :param args: Números a serem usados na divisão.
        :return: Resultado da divisão.
        """
        response = self.__send_request(DIV, args)
        try:
            return float(response[JSON_KEY_RESS])
        except Exception:
            if response[JSON_KEY_RESS] == ERR_DIV_BY_ZERO:
                raise ZeroDivisionError("Impossível dividir por zero!")
            else:
                raise Exception("Argumentos inválidos!")
        


class Server:
    """
    Classe para criar um servidor que aceita conexões de clientes e executa operações.
    """

    def __init__(self, port: int = connection.STD_PORT):
        """
        Inicializa um servidor com o número da porta.

        :param port: Número da porta do servidor.
        """
        self.port = port
        self.server_socket = None
        self.operation_mapping = {
            SUM: self.__sum_task,
            SUB: self.__sub_task,
            MUL: self.__mul_task,
            DIV: self.__div_task,
        }

    def __del__(self):
        """
        Fecha o socket do servidor ao destruir o objeto.
        """
        if self.server_socket: 
            self.server_socket.close()

    def start(self) -> None:
        """
        Inicia o servidor e espera por conexões de clientes.
        """
        self.server_socket = connection.create_server_connection(self.port)
        print(f"O servidor está ouvindo na porta {self.port}...")
        connected_clients_threads = []
        try:
            while True:
                connection_socket, address = self.server_socket.accept()
                thread = threading.Thread(
                    target = self.__handle_client, args=(connection_socket, address))
                connected_clients_threads.append((thread, connection_socket))
                thread.setDaemon(True)
                thread.start()
        except KeyboardInterrupt:
            print("\nO servidor foi finalizado...")
        finally:
            # Força o encerramento de todas as Threads filhas.
            for thread, connection_client in connected_clients_threads:
                connection_client.close()
                thread.join(0)
            self.server_socket.close()

    def __handle_client(self, connection_socket: connection.socket.socket, 
                        address: Tuple[str, int]) -> None:
        """
        Escuta as mensagens do cliente e processa as tarefas solicitadas.

        :param connection_socket: Soquete de conexão com o cliente.
        :param address: Endereço do cliente.
        """
        print(f"{address[0]} conectou\n")
        with connection_socket:
            while True:
                message = connection.receive_socket_message(connection_socket)
                if message:
                    task, args = self.__decode_request_message(message)
                    if task == END:
                        break
                    if task not in self.operation_mapping:
                        continue
                    
                    connection_socket.sendall(self.operation_mapping[task](*args).encode(connection.STD_ENCODE))
                else:
                    break
        print(f"{address[0]} desconectou\n")

    def __sum_task(self, *args) -> str:
        """
        Executa a tarefa de soma.

        :param args: Números a serem somados.
        :return: Resultado da soma.
        """        
        result = {}
        try:
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else sum(args)
        except TypeError:
            result[JSON_KEY_RESS] = ERR
        
        return json.dumps(result)
    
    def __sub_task(self, *args) -> str:
        """
        Executa a tarefa de subtração.

        :param args: Números a serem somados.
        :return: Resultado da soma.
        """        
        result = {}
        try:
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else (args[0] + sum([num * -1 for num in args[1:]]))
        except TypeError:
            result[JSON_KEY_RESS] = ERR
        
        return json.dumps(result)
    
    def __mul_task(self, *args) -> str:
        """
        Executa a tarefa de multiplicação.

        :param args: Números a serem usados na multiplicação.
        :return: Resultado da multiplicação.
        """
        result = {}
        try:
            product = 1
            for number in args:
                product  *= number
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else product
        except TypeError:
            result[JSON_KEY_RESS] = ERR
        
        return json.dumps(result)
    

    def __div_task(self, *args) -> str:
        """
        Executa a tarefa de multiplicação.

        :param args: Números a serem usados na multiplicação.
        :return: Resultado da multiplicação.
        """
        result = {}
        try:
            if len(args) < 1:
                result[JSON_KEY_RESS] = ERR
            else:
                quotient = args[0]
                for number in args[1:]:
                    quotient  /= number
                result[JSON_KEY_RESS] = quotient
        except TypeError:
            result[JSON_KEY_RESS] = ERR
        except ZeroDivisionError:
            result[JSON_KEY_RESS] = ERR_DIV_BY_ZERO
        
        return json.dumps(result)
    

    def __decode_request_message(self, request_message: str) -> (str, Any):
        """
        Decodifica uma mensagem de solicitação JSON.

        :param request_message: A mensagem de solicitação JSON a ser decodificada.
        :return: Uma tupla contendo a tarefa (task) e 
                os argumentos (args) extraídos da mensagem.
        """
        request = json.loads(request_message)
        task = request.get(JSON_KEY_TASK)
        args = request.get(JSON_KEY_ARGS, [])

        return (task, args)