from remote_procedure_call import Client
import time
import json

def test_client() -> None:
    try:
        client = Client()

        print(client.sum(5, 5.5, 5.55))
        print(client.sum(5, 5.5, 5.55))
        print(client.mul(1, 2, 3, 4, 5))
        print(client.mul(1, 2, 3, 4))
        print(client.sum(15.99, 0.001))
        print(client.sum(15.99, 0.01))
        try:
            print(client.div(5, 5.5, 0))
        except ZeroDivisionError:
            pass
        print(client.div(5, 5.5))
        print(client.div(5, 5.5))
        print(client.sum(5, 5.5, 5.55))
        print(client.sub(5, 5.5, -6))
        print(client.sum(5, 5.5, 5.55))
        print(client.div(100, 10))
        print(client.mul(1, 2, 3, 4, 5))
        print(client.sum(5, 5.5, 5.56))
        print(client.sub(5, 5.5, -6))
        print(client.sub(5, 5.5, 6))
        print(client.is_prime(1, 2, 3, 4, 5, 6))
        print(client.is_prime(1, 2, 3, 4, 5, 6))
        print(client.is_prime_multiprocess(1, 2, 3, 4, 5, 6))
        print(client.is_prime_multiprocess(1, 2, 3, 4, 5))

        print(json.dumps(client.cache.cache, indent = 5))
        
        client.close()
    except ConnectionError:
        print("Erro durante a conexão! Verifique se o servidor está online.")
    
def test_multiprocess() -> None:
    client = Client()
    values = [i for i in range(10, 5000001)]

    # Contabilizando o tempo sem multiprocessamento.
    start = time.time()
    res = client.is_prime(*values)
    end = time.time()

    print(f"A execução sem multiprocessamento levou {round(end - start, 5)} segundos")
   
    # Contabilizando o tempo com multiprocessamento.
    m_start = time.time()
    m_res = client.is_prime_multiprocess(*values)
    m_end = time.time()

    print(f"A execução com multiprocessamento levou {round(m_end - m_start, 5)} segundos")
   
   # Exibindo as possíveis diferenças.
    for v, r in zip(res, m_res):
        if v[1] != r[1]:
            print(f"{v[0]}: {v[1]} - {r[0]}: {r[1]}")

    client.close()


if __name__ == "__main__":
    test_client()
    