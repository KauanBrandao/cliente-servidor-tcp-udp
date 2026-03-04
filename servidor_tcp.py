import socket


servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('127.0.0.1', 5000))
servidor.listen(1)


print("Servidor TCP disponível na porta 5000")

conexao, endereco = servidor.accept()
print(f"Conectado a {endereco}")


while True:
    mensagem = conexao.recv(1024).decode()
    if not mensagem:
        break
    print(f"Cliente falou: {mensagem}")

    resposta = input(f"Resposta do servidor: ")
    conexao.send(resposta.encode())

conexao.close()
servidor.close()