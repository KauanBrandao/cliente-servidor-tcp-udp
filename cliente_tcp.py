import socket 


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 5000))
print("Conectado ao servidor TCP! Digite 'sair' para encerrar.")


while True:
    mensagem = input("Cliente mensagem: ")
    if (mensagem.lower() == 'sair'):
        break

    cliente.send(mensagem.encode())


    resposta = cliente.recv(1024).decode()
    print(f"Resposta do servidor: {resposta}")

cliente.close()