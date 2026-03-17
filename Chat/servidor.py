import socket
import threading


clientes = []

def repassar_mensagens(mensagem, cliente_remetente):
    """Envia a mensagem recebida para todos os outros usuários do chat"""
    for cliente in clientes:
        if cliente != cliente_remetente:
            try:
                cliente.send(mensagem)
            except:
                cliente.close()
                clientes.remove(cliente)

def escutar_cliente(cliente, endereco):
    """Fica escutando infinitamente as mensagens de um cliente específico"""
    print(f"[NOVO USUÁRIO] {endereco} entrou no chat.")
    while True:
        try:
            mensagem = cliente.recv(1024)
            if mensagem:
                # Repassa a mensagem para a galera
                repassar_mensagens(mensagem, cliente)
            else:
                break
        except:
            break
    
    print(f"[DESCONECTOU] {endereco} saiu.")
    clientes.remove(cliente)
    cliente.close()

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('0.0.0.0', 5000))
servidor.listen()

print("Servidor de Chat TCP rodando na porta 5000...")

while True:
    cliente, endereco = servidor.accept()
    clientes.append(cliente)

    thread = threading.Thread(target=escutar_cliente, args=(cliente, endereco))
    thread.start()