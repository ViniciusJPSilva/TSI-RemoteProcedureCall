class ServerTimeoutError(Exception):
    """
    Exceção levantada quando ocorre um timeout ao tentar se comunicar com um servidor.

    :param message: Uma mensagem de erro personalizada (opcional).
    """
    def __init__(self, message = "O servidor demorou muito para responder."):
        super().__init__(message)

class ServerNotRespondingError(Exception):
    """
    Exceção levantada quando um servidor não responde a uma solicitação.

    :param message: Uma mensagem de erro personalizada (opcional).
    """
    def __init__(self, message = "O servidor não respondeu."):
        super().__init__(message)

class NoServersFoundError(Exception):
    """
    Exceção levantada quando nenhum servidor é encontrado ou disponível.

    :param message: Uma mensagem de erro personalizada (opcional).
    """
    def __init__(self, message = "Nenhum servidor encontrado."):
        super().__init__(message)

class InvalidArguments(Exception):
    """
    Exceção levantada quando argumentos inválidos são fornecidos.

    :param message: Uma mensagem de erro personalizada (opcional).
    """
    def __init__(self, message = "Argumentos inválidos."):
        super().__init__(message)
