import random
from rpc import name_server
import web_utils.connection as connection
import json
import time
import socket
from rpc.tasks import *
from rpc.rpc_exceptions import *
from cache.cache import Cache
from functools import wraps
from typing import Tuple, Any, List
import traceback

ERR = "__ERROR__"
ERR_DIV_BY_ZERO = "__ERR_DIV_0__"

JSON_KEY_TASK = "task"
JSON_KEY_ARGS = "args"
JSON_KEY_RESS = "result"

MAX_ITEMS_CACHE = 10

CACHE_LOG_FILE = "./log/cache_log.bin"
WEB_CACHE_LOG_FILE = "./log/web_cache_log.bin"

MINUTE_IN_SECONDS = 60

CACHE_PERSIST_TIME = 0.5 # Em minutos

WEB_SCRAPING_TIME_LIMIT = 0.1 # Em minutos

NS_IP_INDEX = 0
NS_PORT_INDEX = 1

NAME_SERVER_TIMEOUT = 5.0 # Em segundos

def handle_rpc_exceptions(func):
    """
    Decorador para capturar exceções e relançá-las sem fazer nenhum tratamento adicional.

    Este decorador envolve uma função e captura exceções específicas, como ConnectionError e ValueError,
    relançando-as sem fazer tratamento adicional. Pode ser usado para padronizar a manipulação de exceções
    em funções decoradas.

    :param func: A função que será decorada.
    :return: Uma função decorada que captura e relança exceções.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError as ce:
            raise ce from None
        except ServerNotRespondingError as snre:
            raise snre from None
        except ServerTimeoutError as ste:
            raise ste from None
        except NoServersFoundError as nsfe:
            raise nsfe from None
        except InvalidArguments as ia:
            raise ia from None
        except ZeroDivisionError as zde:
            raise zde from None
        except Exception as e:
            raise e

    return wrapper


class Client:
    """
    Classe para criar um cliente que se conecta 
    a um servidor remoto para executar operações.
    """

    def __init__(self, name_server: Tuple[str, int], server_ip: str = connection.LOCAL_HOST, 
                 server_port: int = connection.STD_PORT):
        """
        Inicializa um objeto da classe Client.

        :param name_server: Uma tupla contendo o endereço IP e a porta do servidor de nomes.
        :param server_ip: O endereço IP do servidor ao qual o cliente se conectará. Padrão é 'localhost'.
        :param server_port: A porta do servidor ao qual o cliente se conectará. Padrão é a porta padrão definida em connection.STD_PORT.

        :return: None
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.name_server = name_server
        self.udp_socket = connection.create_client_connection(is_tcp = False)
        self.client_socket = None
        self.cache = Cache.init_using_file(CACHE_LOG_FILE, MAX_ITEMS_CACHE)
        self.web_cache = Cache.init_using_file(WEB_CACHE_LOG_FILE, 1)
        self.last_cache_persistence = None
        self.last_web_query = None

    def __enter__(self):
        """
        Método chamado ao entrar no bloco 'with'. Retorna o próprio objeto.
        """
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Método chamado ao sair do bloco 'with'. Chama o método 'close()'.

        :param exc_type: Tipo de exceção, se ocorreu uma. None em caso contrário.
        :param exc_value: Valor da exceção, se ocorreu uma. None em caso contrário.
        :param traceback: Rastreamento da pilha, se ocorreu uma exceção. None em caso contrário.
        """
        self.close()

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

        if self.udp_socket:
            self.udp_socket.close()
    

    def __connect_server(self, server_data: Tuple[str, int]) -> None:
        """
        Estabelece uma conexão com um servidor remoto com base nos dados fornecidos.

        :param server_data: Uma tupla contendo o endereço IP e a porta do servidor.
        :type server_data: Tuple[str, int]

        :raises ConnectionError: Lança uma exceção se ocorrer um erro ao se conectar ao servidor.
        """
        try:
            self.client_socket = connection.create_client_connection(*server_data)
        except:
            traceback.print_exc()
            raise ConnectionError("Erro ao se conectar ao servidor!")
        
        
    def __get_servers(self, task: str) -> List[Tuple[str, int]]:
        """
        Envia uma solicitação de tarefa para os servidores, recebe uma lista de servidores disponíveis como resposta e a retorna.

        :param task: A tarefa que será enviada aos servidores.
        :type task: str
        :return: Uma lista de tuplas contendo o endereço IP e a porta dos servidores disponíveis.
        :rtype: List[Tuple[str, int]]

        :raises ServerTimeoutError: Lança uma exceção se ocorrer um timeout na comunicação com o servidor.
        :raises ServerNotRespondingError: Lança uma exceção se o servidor não responder à solicitação.
        """
        try:
            # Timeout.
            self.udp_socket.settimeout(NAME_SERVER_TIMEOUT)

            connection.send_udp_socket_message(self.udp_socket, task, self.name_server)
            response, _ = connection.receive_udp_socket_message(self.udp_socket)

            # Verifique se a resposta não está vazia
            if response:
                return response.decode()
            else:
                raise ServerNotRespondingError()

        except socket.timeout:
            raise ServerTimeoutError()
        

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
            
            # Tentando obter os dados pelo servidor de nomes.
            servers_list = json.loads(self.__get_servers(task))
            
            if len(servers_list) == 0:
                raise NoServersFoundError("Nenhum servidor encontrado!")
            
            self.__connect_server(random.choice(servers_list))

            connection.send_socket_message(self.client_socket, request_str)

            response_str = connection.receive_socket_message(self.client_socket)
            response = json.loads(response_str)[JSON_KEY_RESS]

            if response == ERR:
                raise InvalidArguments()

            if response not in [ERR, ERR_DIV_BY_ZERO] and task not in [LAST_NEWS_IF_BQ]:
                self.cache.add_in_cache(cache_key, response)
            
            self.__timed_persist_cache()
            self.client_socket.close()

        return response
    

    def __timed_persist_cache(self) -> bool:
        """
        Verifica se é necessário persistir o cache com base no tempo e chama a função de persistência, se necessário.

        :return: True se o cache foi persistido, False caso contrário.
        """
        now = time.time()
        if (not self.last_cache_persistence) or (now - self.last_cache_persistence >= CACHE_PERSIST_TIME * MINUTE_IN_SECONDS):
            self.last_cache_persistence = now
            return self.__persist_cache()
    
    
    def __persist_cache(self) -> bool:
        """
        Persiste o cache em arquivos e registra a operação em um log.

        :return: True se a persistência do cache for bem-sucedida, False caso contrário.
        """
        Cache.persist_cache_file(self.web_cache, WEB_CACHE_LOG_FILE)
        return Cache.persist_cache_file(self.cache, CACHE_LOG_FILE)


    @handle_rpc_exceptions
    def sum(self, *args: float) -> float:
        """
        Envia uma solicitação de soma para o servidor e retorna o resultado.

        :param args: Números a serem somados.
        :return: Resultado da soma.
        """
        return float(self.__send_request(SUM, args))
        

    @handle_rpc_exceptions
    def sub(self, *args: float) -> float:
        """
        Envia uma solicitação de subtração para o servidor e retorna o resultado.

        :param args: Números a serem usados na subtração.
        :return: Resultado da subtração.
        """
        return float(self.__send_request(SUB, args))
        

    @handle_rpc_exceptions    
    def mul(self, *args: float) -> float:
        """
        Envia uma solicitação de multiplicação para o servidor e retorna o resultado.

        :param args: Números a serem usados na multiplicação.
        :return: Resultado da multiplicação.
        """
        return float(self.__send_request(MUL, args))
        

    @handle_rpc_exceptions
    def div(self, *args: float) -> float:
        """
        Envia uma solicitação de divisão para o servidor e retorna o resultado.

        :param args: Números a serem usados na divisão.
        :return: Resultado da divisão.
        """
        response = self.__send_request(DIV, args)
        
        if response == ERR_DIV_BY_ZERO:
            raise ZeroDivisionError("Impossível dividir por zero!")
        
        return float(response)
            

    @handle_rpc_exceptions     
    def is_prime(self, *args: int) -> List[Tuple[int, bool]]:
        """
        Envia uma solicitação de identificação de um número primo para o servidor e retorna o resultado.

        :param args: Números a serem identificados.
        :return: True caso seja primo, False caso contrário.
        """
        return self.__send_request(PRIME, args)
        
        
    @handle_rpc_exceptions
    def is_prime_multiprocess(self, *args: int) -> List[Tuple[int, bool]]:
        """
        Envia uma solicitação de identificação de um número primo para o servidor e retorna o resultado.
        Exige que o servidor processe os dados utilizando multiprocessamento.

        :param args: Números a serem identificados.
        :return: True caso seja primo, False caso contrário.
        """
        return self.__send_request(MULTIPROCESS_PRIME, args)


    @handle_rpc_exceptions
    def last_news_if_barbacena(self, count: int) -> List[Tuple[str, str]]:
        """
        Envia uma solicitação de webscraping no site de noticias do IFET Barbacena e retorna o resultado.

        :param args: Números de noticias requeridas.
        :return: Lista com o titulo e o link das respectivas noticias, em uma tupla.
        """
        response = self.__get_web_cache(count)
        if not response:
            response = self.__send_request(LAST_NEWS_IF_BQ, [count])
            self.web_cache.clear()
            self.web_cache.add_in_cache(str(count), response)

        return response
    
    @handle_rpc_exceptions
    def validate_cpf(self, cpf: str) -> bool:
        """
        Envia uma solicitação de webscraping no site de noticias do IFET Barbacena e retorna o resultado.

        :param args: Números de noticias requeridas.
        :return: Lista com o titulo e o link das respectivas noticias, em uma tupla.
        """
        return self.__send_request(VALDATE_CPF, cpf)


    def __get_web_cache(self, count: int) -> List[Tuple[str, str]]:
        """
        Obtém os dados da web "cacheados" se estiverem disponíveis e caso atenda ao limite de tempo.

        :param count: O número máximo de itens a serem obtidos do cache da web.
        :return: Lista com o titulo e o link das respectivas noticias, em uma tupla. (ou None se não disponíveis ou no limite de tempo).
        """
        now = time.time()
        if (not self.last_web_query) or (now - self.last_web_query >= WEB_SCRAPING_TIME_LIMIT * MINUTE_IN_SECONDS):
            self.last_web_query = now
        else:
            web_cache = self.web_cache.get()
            if web_cache:
                key = list(web_cache.keys())[0]
                total_links = int(key)
            
                if total_links >= count:
                    return web_cache[key][0:count]
        
        return None