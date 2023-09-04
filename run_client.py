from remote_procedure_call import Client
import time

def test_client():
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