import connection
import threading
import json
import multiprocessing
import time
import math
import mathematics
import concurrent.futures
from cache import Cache
from web_scraping import get_links
from typing import Tuple, Any, List

SUM = "__SUM__"
SUB = "__SUB__"
MUL = "__MUL__"
DIV = "__DIV__"
PRIME = "__PRIME__"
MULTIPROCESS_PRIME = "__MUL_PROC_PRIME__"
LAST_NEWS_IF_BQ = "__LAST_NEWS_IF_BQ__"

END = "__END__"

ERR = "__ERROR__"
ERR_DIV_BY_ZERO = "__ERR_DIV_0__"

JSON_KEY_TASK = "task"
JSON_KEY_ARGS = "args"
JSON_KEY_RESS = "result"

MAX_ITEMS_CACHE = 10

CACHE_LOG_FILE = "./cache/cache_log.bin"
CACHE_PERSIST_TIME = 0.5 #Em minutos

NEWS_URL = "https://www.ifsudestemg.edu.br/noticias/barbacena/?b_start:int={}"
NEWS_IN_PAGE = 20

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
        self.client_socket = None
        try:
            self.client_socket = connection.create_client_connection(server_ip, server_port)
        except:
            raise ConnectionError("Erro ao se conectar ao servidor!")
        self.cache = Cache.init_using_file(CACHE_LOG_FILE, MAX_ITEMS_CACHE)
        self.last_cache_persistence = None


    def __del__(self):
        """
        Fecha a conexão do cliente com o servidor ao destruir o objeto.
        """
        self.close()


    def close(self):
        """
        Persiste o cache e fecha a conexão do cliente com o servidor.
        """
        self.__persist_cache()
        if self.client_socket:
            self.client_socket.close()
        


    def __send_request(self, task: str, args):
        """
        Envia uma solicitação para o servidor e recebe uma resposta.

        :param task: A operação que deseja solicitar ao servidor.
        :param args: Argumentos para a operação.
        :return: A resposta do servidor após processar a solicitação.
        """
        cache_key = self.cache.create_key(task if task not in [PRIME, MULTIPROCESS_PRIME] else PRIME, args)
        response = self.cache.verify_cache(cache_key)
        
        if response == None:
            request_str = json.dumps({
                    JSON_KEY_TASK: task,
                    JSON_KEY_ARGS: args
                })
            connection.send_socket_message(self.client_socket, request_str)

            response_str = connection.receive_socket_message(self.client_socket)
            response = json.loads(response_str)[JSON_KEY_RESS]

            if response not in [ERR, ERR_DIV_BY_ZERO]:
                self.cache.add_in_cache(cache_key, response)
                self.__timed_persist_cache()

        return response
    

    def __timed_persist_cache(self) -> bool:
        now = time.time()
        if (not self.last_cache_persistence) or (now - self.last_cache_persistence >= CACHE_PERSIST_TIME * 60):
            self.last_cache_persistence = now
            return self.__persist_cache()
    
    def __persist_cache(self) -> bool:
        return Cache.persist_cache_file(self.cache, CACHE_LOG_FILE)

    def sum(self, *args: float) -> float:
        """
        Envia uma solicitação de soma para o servidor e retorna o resultado.

        :param args: Números a serem somados.
        :return: Resultado da soma.
        """
        response = self.__send_request(SUM, args)
        try:
            return float(response)
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
            return float(response)
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
            return float(response)
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
            return float(response)
        except Exception:
            if response == ERR_DIV_BY_ZERO:
                raise ZeroDivisionError("Impossível dividir por zero!")
            else:
                raise Exception("Argumentos inválidos!")
            
            
    def is_prime(self, *args: int) -> List[Tuple[int, bool]]:
        """
        Envia uma solicitação de identificação de um número primo para o servidor e retorna o resultado.

        :param args: Números a serem identificados.
        :return: True caso seja primo, False caso contrário.
        """
        response = self.__send_request(PRIME, args)
        try:
            return response
        except Exception:
            raise Exception("Argumentos inválidos!")
        
        
    def is_prime_multiprocess(self, *args: int) -> List[Tuple[int, bool]]:
        """
        Envia uma solicitação de identificação de um número primo para o servidor e retorna o resultado.
        Exige que o servidor processe os dados utilizando multiprocessamento.

        :param args: Números a serem identificados.
        :return: True caso seja primo, False caso contrário.
        """
        response = self.__send_request(MULTIPROCESS_PRIME, args)
        try:
            return response
        except Exception:
            raise Exception("Argumentos inválidos!")

    def last_news_if_barbacena(self, count: int) -> List[Tuple[str, str]]:
        response = self.__send_request(LAST_NEWS_IF_BQ, [count])
        try:
            return response
        except Exception:
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
        print("Somou") 
        result = { JSON_KEY_RESS: ERR }
        try:
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else mathematics.add(args)
        finally:
            return json.dumps(result)
        
    
    def __sub_task(self, *args) -> str:
        """
        Executa a tarefa de subtração.

        :param args: Números a serem somados.
        :return: Resultado da soma.
        """        
        result = { JSON_KEY_RESS: ERR }
        try:
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else mathematics.sub(args)
        finally:
            return json.dumps(result)
        
    
    def __mul_task(self, *args) -> str:
        """
        Executa a tarefa de multiplicação.

        :param args: Números a serem usados na multiplicação.
        :return: Resultado da multiplicação.
        """
        result = { JSON_KEY_RESS: ERR }
        try:
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else mathematics.mul(args)
        finally:
            return json.dumps(result)
    

    def __div_task(self, *args) -> str:
        """
        Executa a tarefa de multiplicação.

        :param args: Números a serem usados na multiplicação.
        :return: Resultado da multiplicação.
        """
        result = { JSON_KEY_RESS: ERR }
        try:
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else mathematics.div(args)
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
        result = { JSON_KEY_RESS: ERR }
        try:
            res = []
            [res.append((number, mathematics.is_prime(number))) for number in args]
            result[JSON_KEY_RESS] = ERR if len(args) < 1 else res
        finally:
            return json.dumps(result)
        
        
    def __is_prime_multiprocessing_task(self, *args) -> str:
        """
        Verifica se os números fornecidos são primos usando múltiplos processos e retorna o resultado como uma string JSON.

        :param args: Uma lista de números inteiros a serem verificados.
        :return: Uma string JSON contendo os resultados da verificação de primos para cada número.
        """
        pool = multiprocessing.Pool()
        try:
            results = pool.map(mathematics.is_prime, args)
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
        quantity_requested = int(args[0])
        num_pages = math.ceil(quantity_requested / NEWS_IN_PAGE)

        links_list = []

        # for i in range(0, num_pages * NEWS_IN_PAGE, 20):
        #     request_result = get_links(NEWS_URL.format(i), "summary url")
        #     if request_result:
        #         links_list = [*links_list, *request_result]

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