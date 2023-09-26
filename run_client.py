from rpc.client import Client
import time
import json

def test_last_news() -> None:
    try:
        client = Client()

        response = client.last_news_if_barbacena(31)
        response = client.last_news_if_barbacena(14)
        # time.sleep(11)
        # response = client.last_news_if_barbacena(7)
        
        if response:
            count = 1
            for link in response:
                print(f"{count}) {link[0]}:\n\t{link[1]}\n\n")
                count += 1
        # print(f"Total = {count-1}")
        # print(f"Resultado: {client.sum(1, 2, 3)}")
        client.close()
    except ConnectionError:
        print("Erro durante a conexão! Verifique se o servidor está online.")


def test_cache() -> None:
    try:
        client = Client()

        # client.sum(5, 5.5, 5.55)
        # client.sum(5, 5.5, 5.55)
        # client.mul(1, 2, 3, 4, 5)
        # client.mul(1, 2, 3, 4)
        # client.sum(15.99, 0.001)
        # client.sum(15.99, 0.01)
        # try:
        #     client.div(5, 5.5, 0)
        # except ZeroDivisionError:
        #     pass
        # client.div(5, 5.5)
        # client.div(5, 5.5)
        # client.sum(5, 5.5, 5.55)
        # client.sub(5, 5.5, -6)
        # client.sum(5, 5.5, 5.55)
        # client.div(100, 10)
        # client.mul(1, 2, 3, 4, 5)
        # client.sum(5, 5.5, 5.56)
        # client.sub(5, 5.5, -6)
        # client.sub(5, 5.5, 6)
        # client.is_prime(1, 2, 3, 4, 5, 6)
        # client.is_prime(1, 2, 3, 4, 5, 6)
        # client.is_prime_multiprocess(1, 2, 3, 4, 5, 6)
        # client.is_prime_multiprocess(1, 2, 3, 4, 5)
        try:
            while True:
                print("Soma = " + str(client.sum(int(input("1° Nro: ")), int(input("2° Nro: ")))) + "\n\n")
                print(f"\n\nCACHE:\n{json.dumps(client.cache.cache, indent = 5)}")
        except KeyboardInterrupt:
            pass
        
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
    start = time.time()

    test_last_news()

    end = time.time()

    print(f"A função levou {end - start} segundos para ser executada.")

    
    