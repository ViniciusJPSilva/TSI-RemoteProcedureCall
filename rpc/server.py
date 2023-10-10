import web_utils.connection as connection
import threading
import json
import multiprocessing
import math
from mathematics.mathematics import *
import concurrent.futures
from rpc.tasks import *
from web_utils.web_scraping import get_links
from typing import Tuple, Any, List

END = "__END__"

ERR = "__ERROR__"
ERR_DIV_BY_ZERO = "__ERR_DIV_0__"

JSON_KEY_TASK = "task"
JSON_KEY_ARGS = "args"
JSON_KEY_RESS = "result"

NEWS_URL = "https://www.ifsudestemg.edu.br/noticias/barbacena/?b_start:int={}"
NEWS_IN_PAGE = 20

class Server:
    """
    Classe para criar um servidor que aceita conexões de clientes e executa operações.
    """

    def __init__(self, ip: str = connection.LOCAL_HOST, port: int = connection.STD_PORT):
        """
        Inicializa um servidor com o número da porta.

        :param port: Número da porta do servidor.
        """
        self.ip = ip
        self.port = port
        self.server_socket = None
        self.task_mapping = {
            SUM: self.__sum_task,
            SUB: self.__sub_task,
            MUL: self.__mul_task,
            DIV: self.__div_task,
            PRIME: self.__is_prime_task,
            MULTIPROCESS_PRIME: self.__is_prime_multiprocessing_task,
            LAST_NEWS_IF_BQ: self.__get_last_news_if_barbacena_task,
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
        self.server_socket = connection.create_server_connection(self.ip, self.port)
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


    def close(self) -> None:
        """
        Fecha o socket do servidor ao fechar o objeto.
        """
        if self.server_socket: 
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
                    if task not in self.task_mapping:
                        connection_socket.sendall(ERR.encode(connection.STD_ENCODE))
                        continue
                    
                    connection.send_socket_message(connection_socket, self.task_mapping[task](*args))
                else:
                    break
        print(f"{address[0]} desconectou\n")


    def __sum_task(self, *args) -> str:
        """
        Executa a tarefa de soma.

        :param args: Números a serem somados.
        :return: Resultado da soma.
        """       
        print("Somou...") 
        result = { JSON_KEY_RESS: ERR }
        try:
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else add(args)
        except Exception as e:
            print(e)
        finally:
            return json.dumps(result)
        
    
    def __sub_task(self, *args) -> str:
        """
        Executa a tarefa de subtração.

        :param args: Números a serem somados.
        :return: Resultado da soma.
        """   
        print("Subtraiu...")      
        result = { JSON_KEY_RESS: ERR }
        try:
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else sub(args)
        finally:
            return json.dumps(result)
        
    
    def __mul_task(self, *args) -> str:
        """
        Executa a tarefa de multiplicação.

        :param args: Números a serem usados na multiplicação.
        :return: Resultado da multiplicação.
        """
        print("Multiplicou...") 
        result = { JSON_KEY_RESS: ERR }
        try:
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else mul(args)
        finally:
            return json.dumps(result)
    

    def __div_task(self, *args) -> str:
        """
        Executa a tarefa de multiplicação.

        :param args: Números a serem usados na multiplicação.
        :return: Resultado da multiplicação.
        """
        print("Dividiu...") 
        result = { JSON_KEY_RESS: ERR }
        try:
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else div(args)
        except ZeroDivisionError:
            result[JSON_KEY_RESS] = ERR_DIV_BY_ZERO
        finally:
            return json.dumps(result)
        
        
    def __is_prime_task(self, *args) -> str:
        """
        Verifica se os números fornecidos são primos e retorna o resultado como uma string JSON.

        :param args: Uma lista de números inteiros a serem verificados.
        :return: Uma string JSON contendo os resultados da verificação de primos para cada número.
        """
        print("Eu vou dormir lá em cima...") 
        result = { JSON_KEY_RESS: ERR }
        try:
            res = []
            [res.append((number, is_prime(number))) for number in args]
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else res
        finally:
            return json.dumps(result)
        
        
    def __is_prime_multiprocessing_task(self, *args) -> str:
        """
        Verifica se os números fornecidos são primos usando múltiplos processos e retorna o resultado como uma string JSON.

        :param args: Uma lista de números inteiros a serem verificados.
        :return: Uma string JSON contendo os resultados da verificação de primos para cada número.
        """
        print("Eu vou dormir lá em cima... Mas tomei diversos PROCESSOS") 
        pool = multiprocessing.Pool()
        try:
            results = pool.map(is_prime, args)
            result = {JSON_KEY_RESS: ERR if len(args) < 1 else list(zip(args, results))}
        except Exception as e:
            result = {JSON_KEY_RESS: ERR}
        finally:
            pool.close()
            pool.join()
            return json.dumps(result)


    def __get_last_news_if_barbacena_task(self, *args) -> str:
        """
        Obtém as últimas notícias do IFET Campus Barbacena, se disponíveis, e retorna os links em uma string JSON.

        :param args: Uma lista contendo a quantidade de links solicitados como o primeiro elemento.
        :return: Uma string JSON contendo os links das últimas notícias de Barbacena.
        """
        print("Fofocando...") 
        quantity_requested = int(args[0])
        num_pages = math.ceil(quantity_requested / NEWS_IN_PAGE)

        links_list = []
        def get_links_from_page(page_number):
            return get_links(NEWS_URL.format(page_number), "summary url")

        # Usando ThreadPoolExecutor para executar as solicitações em paralelo
        with concurrent.futures.ThreadPoolExecutor() as executor:
            page_numbers = range(0, num_pages * NEWS_IN_PAGE, 20)
            futures = {executor.submit(get_links_from_page, page_number): page_number for page_number in page_numbers}

            for future in concurrent.futures.as_completed(futures):
                page_number = futures[future]
                request_result = future.result()
                if request_result:
                    links_list.extend(request_result)
        print("Webscrapou")
        return json.dumps({JSON_KEY_RESS: links_list[0:quantity_requested]})

    

    def __decode_request_message(self, request_message: str) -> Tuple[str, Any]:
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