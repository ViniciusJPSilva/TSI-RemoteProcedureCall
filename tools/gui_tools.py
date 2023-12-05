from functools import wraps
import re
import customtkinter
from gui.top_level import TopLevelPopUp
from rpc.rpc_exceptions import ServerNotRespondingError, InvalidArguments, NoServersFoundError, ServerTimeoutError

def handle_exceptions(func):
    """
    Decorador para capturar exceções e tratá-las.

    Este decorador envolve uma função e captura exceções específicas, como ConnectionError e ValueError. Pode ser usado para padronizar a manipulação de exceções
    em funções decoradas.

    :param func: A função que será decorada.
    :return: Uma função decorada que captura e relança exceções.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ConnectionError:
            TopLevelPopUp("\n\nERRO: Houve alguma indisponibilidade no servidor que executa essa tarefa...")
        except ServerNotRespondingError:
            TopLevelPopUp("\n\nERRO: O servidor de nomes não está respondendo...")
        except ServerTimeoutError:
            TopLevelPopUp("\n\nERRO: O servidor de nomes demorou muito para responder...")
        except NoServersFoundError:
            TopLevelPopUp("\n\nERRO: Nenhum dos servidores disponíveis executam essa tarefa...")
        except InvalidArguments:
            TopLevelPopUp("\n\nERRO: Argumentos inválidos...")
        except ZeroDivisionError:
            TopLevelPopUp("\n\nERRO: Impossível dividir por 0 (zero)...")
        except Exception as e:
            print(e)
            TopLevelPopUp("\n\nERRO: Aconteceu algum erro inesperado...")

    return wrapper

def float_regex_validator(string: str) -> bool:
    """
    Valida uma string para garantir que seja um número válido.

    :param string: A string a ser validada.
    
    :return: True se a string for um número válido, False caso contrário.
    """
    regex = re.compile(r"(\+|\-)?[0-9.]*$")
    result = regex.match(string)
    return (string == ""
            or (string.count('+') <= 1
                and string.count('-') <= 1
                and string.count('.') <= 1
                and result is not None
                and result.group(0) != ""))


def float_validator(P: str) -> bool:
    """
    Função de validação para usar em widgets de entrada (Entry) no tkinter.

    :param P: A string inserida ou modificada no widget de entrada.

    :return: True se P for um número válido, False caso contrário.
    """
    return float_regex_validator(P)


def configure_float_only_entry(entry: customtkinter.CTkEntry) -> customtkinter.CTkEntry:
    """
    Configura um widget de entrada (Entry) para aceitar apenas números.

    :param entry: O widget de entrada a ser configurado.

    :return: O widget de entrada configurado.
    """
    entry.configure(
        validate="key",
        validatecommand=(entry.register(float_validator), "%P")
    )

    return entry



def int_validator(P: str) -> bool:
    return P.isdigit() or P == ""


def configure_int_only_entry(entry: customtkinter.CTkEntry) -> customtkinter.CTkEntry:
    entry.configure(
        validate="key",
        validatecommand=(entry.register(int_validator), "%P")
    )

    return entry

