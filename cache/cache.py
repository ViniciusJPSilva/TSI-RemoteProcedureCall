import pickle
from typing import Any

class Cache:
    def __init__(self, max_items: int, cache: dict):
        self.cache = cache
        self.max_items = max_items


    @staticmethod
    def init_using_file(file_name: str, max_items: int) -> 'Cache':
        """
        Inicializa um objeto Cache a partir de um arquivo, se possível, ou cria um novo se o arquivo não existir ou ocorrer um erro.

        :param file_name: O nome do arquivo a partir do qual os dados do cache serão lidos ou onde o cache será persistido.
        :param max_items: O número máximo de itens que o cache pode conter.
        :return: Uma instância da classe Cache.
        """
        cache = None
        try:
            with open(file_name, 'rb') as cache_file: 
                data = pickle.load(cache_file)
            cache = Cache(max_items, data)
        except Exception:
            cache = Cache(max_items, dict())
        
        return cache


    @staticmethod
    def persist_cache_file(cache: 'Cache', file_name: str) -> bool:
        """
        Persiste o cache em um arquivo especificado.

        :param cache: O objeto Cache a ser persistido.
        :param file_name: O nome do arquivo onde o cache será salvo.
        :return: True se a persistência do cache for bem-sucedida, False caso contrário.
        """
        try:
            with open(file_name, 'wb') as cache_file: 
                pickle.dump(cache.cache, cache_file)
            return True
        except TypeError:
            return False
        

    def create_key(self, task: str, args: Any) -> str:
        """
        Cria uma chave única com base no nome da tarefa e nos argumentos.

        :param task: Nome da tarefa.
        :param args: Argumentos da tarefa.
        :return: Uma chave única que representa a combinação da tarefa e dos argumentos.
        """
        key = task + "_" + "_".join(map(str, args))
        return key

    def verify_cache(self, new_key: str) -> Any:
        """
        Verifica se uma chave existe no cache e retorna o valor correspondente.

        :param new_key: A chave a ser verificada no cache.
        :return: O valor associado à chave se ela existir no cache, caso contrário, retorna None.
        """
        return self.cache.get(new_key)

    def add_in_cache(self, new_key: str, result: Any) -> bool:
        """
        Adiciona um novo par chave-valor ao cache, substituindo um item antigo, se necessário.

        :param new_key: A chave a ser adicionada ao cache.
        :param result: O valor a ser associado à chave no cache.
        :return: True se a chave foi adicionada com sucesso, False se a chave já existir no cache.
        """
        if len(self.cache) >= self.max_items:
            self.__remove_oldest_item()
        if new_key not in self.cache:
            self.cache[new_key] = result
            return True
        return False
    
    def clear(self) -> None:
        '''
        Apaga todo o conteúdo do dicioário, mas não o persiste na memória secundária.
        '''
        self.cache.clear()

    def __remove_oldest_item(self):
        ''' 
        Remove o item mais antigo do cache.
        '''
        if self.cache:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

    def get(self) -> dict:
        '''
        Retorna o cache.
        '''
        return self.cache
