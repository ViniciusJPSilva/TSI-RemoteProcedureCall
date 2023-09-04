from remote_procedure_call import Client

def test_client():
    client = Client()
    print(client.sum(1.65, 3.99999999999999999))
    print(client.sub(-15, -45, 20))
    print(client.mul(5, 5))
    print(client.div(10, 2, 5, 2))
    client.close()


if __name__ == "__main__":
    test_client()