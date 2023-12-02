import traceback
from rpc import name_server
from rpc.client import Client
from rpc.rpc_exceptions import *
import time
import json

def test_last_news() -> None:
    try:
        client = Client((name_server.NAME_SERVER_STD_ADDR))

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
        client = Client((name_server.NAME_SERVER_STD_ADDR))

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


def test_server_name() -> None:
    client = Client((name_server.NAME_SERVER_STD_ADDR))

    task = -1
    while(task != 0):
        try:
            task = int(input("\nSelecione a tarefa:\n1 - Somar\n2 - Subtrair\n3 - Multiplicar\n4 - Dividir\n5 - Lista de Números Primos\n6 - Ver notícias do IF Barbacena\n7 - Validar CPF\n0 - Sair\nEscolha uma opção: "))
        
            try:
                if task == 1:
                    print("\n\nSOMAR")
                    while(True):
                        try:
                            print("Total = " + str(client.sum(float(input("1° Nro: ")), float(input("2° Nro: ")))) + "\n")
                            break
                        except ValueError:
                            print("Digite somente VALORES NUMÉRICOS, abestado...")
                if task == 2:
                    print("\n\nSUBTRAIR")
                    while(True):
                        try:
                            print("Diferença = " + str(client.sub(float(input("1° Nro: ")), float(input("2° Nro: ")))) + "\n")
                            break
                        except ValueError:
                            print("Digite somente VALORES NUMÉRICOS, abestado...")
                if task == 3:
                    print("\n\nMULTIPLICAR")
                    while(True):
                        try:
                            print("Produto = " + str(client.mul(float(input("1° Nro: ")), float(input("2° Nro: ")))) + "\n")
                            break
                        except ValueError:
                            print("Digite somente VALORES NUMÉRICOS, abestado...")
                if task == 4:
                    print("\n\nDIVIDIR")
                    while(True):
                        try:
                            print("Quociente = " + str(client.div(float(input("1° Nro: ")), float(input("2° Nro: ")))) + "\n")
                            break
                        except ValueError:
                            print("Digite somente VALORES NUMÉRICOS, abestado...")
                if task == 4:
                    print("\n\nDIVIDIR")
                    while(True):
                        try:
                            print("Quociente = " + str(client.div(float(input("1° Nro: ")), float(input("2° Nro: ")))) + "\n")
                            break
                        except ValueError:
                            print("Digite somente VALORES NUMÉRICOS, abestado...")
                if task == 5:
                    print("\n\nNÚMEROS PRIMOS")
                    while(True):
                        try:
                            final = int(input("Verificando quando primos existem entre 0 e o valor fornecido.\nForneça um número inteiro: "))
                            values = [i for i in range(0, final)]

                            m_res = client.is_prime_multiprocess(*values)
                            print(f"\nPrimos entre 0 e {final}: ")

                            for num, is_prime in m_res:
                                if is_prime:
                                    print(num, end="  ")

                            print("\n")
                            break
                        except ValueError:
                            print("Digite somente VALORES NUMÉRICOS, abestado...")   
                if task == 6:
                    print("\n\nNOTÍCIAS DO IFET BARBACENA")
                    while(True):
                        try:
                            num = int(input("Quantas notícias tu quer ver: "))

                            response = client.last_news_if_barbacena(num)
                            print(f"\nÚltimas {num} notícias: ")

                            if response:
                                count = 1
                                for link in response:
                                    print(f"{count}) {link[0]}:\n\t{link[1]}\n\n")
                                    count += 1
                                    
                            break
                        except ValueError:
                            print("Digite somente VALORES NUMÉRICOS, abestado...")   
                if task == 7:
                    print("\n\nVALIDAR CPF")
                    while(True):
                        try:
                            cpf = input("Forneça um CPF: ")
                            print(f"O CPF {cpf} é {'válido' if client.validate_cpf(cpf) else 'inválido'}!")
                            break
                        except ValueError:
                            print("Digite somente VALORES NUMÉRICOS, abestado...") 
                
            except ConnectionError as ce:
                traceback.print_exc()
                print("\n\nERRO: Houve alguma indisponibilidade no servidor que executa essa tarefa... :(")
            except ServerNotRespondingError as snre:
                print("\n\nERRO: Parece que o servidor de nomes não quer mais nomear... :(")
            except ServerTimeoutError as ste:
                print("\n\nERRO: O servidor de nomes demorou muito para responder, talvez ele não goste de você... Ou só tá desligado")
            except NoServersFoundError as nsfe:
                print("\n\nERRO: Nenhum dos servidores disponíveis executam essa tarefa... :(")
            except InvalidArguments as ia:
                print("\n\nERRO: Se tu ficar mandando coisa errada fica difícil, mande os argumentos corretos... Faz favor")
            except ZeroDivisionError as zde:
                print("\n\nERRO: 1° mandamento da matemática: não divirás por zero ! (Ou talvez o resultado seja infinito...)")
            except Exception as e:
                traceback.print_exc()
                print("\n\nERRO: Rolou algum BO desconhecido... Xinga o cara que fez esse treco")


        except ValueError:
            task = -1
        except KeyboardInterrupt:
            print("\n\nMas já vai? Não ceita uma xícara de café?\n")
            break

    client.close()

if __name__ == "__main__":
    # start = time.time()

    test_server_name()

    # end = time.time()

    # print(f"A função levou {end - start} segundos para ser executada.")

    
    