from typing import List

def add(numbers: List[float]) -> float:
    """
    Soma uma lista de números.

    :param numbers: Uma lista de números para serem somados.
    :return: A soma dos números na lista.
    """
    return sum(numbers)


def sub(numbers: List[float]) -> float:
    """
    Subtrai uma lista de números.

    :param numbers: Uma lista de números para serem subtraídos.
    :return: O resultado da subtração dos números na lista.
    """
    return (numbers[0] + sum([num * -1 for num in numbers[1:]]))


def mul(numbers: List[float]) -> float:
    """
    Multiplica uma lista de números.

    :param numbers: Uma lista de números para serem multiplicados.
    :return: O produto dos números na lista.
    """
    product = numbers[0]
    for number in numbers[1:]:
        product *= number
    return product


def div(numbers: List[float]) -> float:
    """
    Divide uma lista de números.

    :param numbers: Uma lista de números para serem divididos.
    :return: O resultado da divisão dos números na lista.
    """
    quotient = numbers[0]
    for number in numbers[1:]:
        quotient  /= number
    return quotient


def is_prime(number: int) -> bool:
    """
    Verifica se um número é primo.

    :param number: O número a ser verificado.
    :return: True se o número for primo, False caso contrário.
    """
    if number <= 1:
        return False
    if number <= 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    return True