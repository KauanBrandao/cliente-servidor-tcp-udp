# Resumo do trabalho de redes:

### Para estabelecer a conexão entre dois processos ou duas máquinas diferentes é necessário que exista um servidor disponível para isso, então o primeiro passo foi criar o servidor tcp abaixo: 

```python
# servidor_tcp.py
import socket

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('127.0.0.1', 5000))
servidor.listen(1)

print("Servidor TCP aguardando na porta 5000...")
conexao, endereco = servidor.accept()
print(f"Conectado a {endereco}")

while True:
    mensagem = conexao.recv(1024).decode()
    if not mensagem: 
        break
    print(f"Cliente: {mensagem}")
    
    resposta = input("Você (Servidor): ")
    conexao.send(resposta.encode())

conexao.close()
servidor.close()

```

### O que acontece nesse trecho de código é o seguinte: criamos um socket (que basicamente é a ponte entre a aplicação e o sistema operacional, responsável por estabelecer a comunicação, geralmente TCP ou UDP, entre dois processos ou máquinas). É nele que configuramos o IP e a porta local da conexão.

### Colocamos ele para "escutar" as conexões que forem feitas no servidor. Quando o cliente fizer a conexão, o servidor vai aceitá-la e capturar os dados da conexão e o endereço do cliente.

### No while é onde acontece a conversa entre os dois processos. O servidor pega a mensagem recebida da conexão (cliente) e a decodifica para mostrar no nosso terminal. Após isso, é criado um input para o servidor digitar algo para o cliente, e logo em seguida a resposta é enviada, codificando a mensagem novamente.


```python
# cliente_tcp.py
import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('127.0.0.1', 5000))
print("Conectado ao Servidor TCP! Digite 'sair' para encerrar.")

while True:
    mensagem = input("Você (Cliente): ")
    if mensagem.lower() == 'sair':
        break
    
    cliente.send(mensagem.encode())
    
    resposta = cliente.recv(1024).decode()
    print(f"Servidor: {resposta}")

cliente.close()
```
### No cliente a lógica é muito parecida, mas ao invés de criar o socket para ficar escutando em uma porta e um IP específicos, ele se conecta diretamente ao IP e à porta do servidor.

### No while é onde acontece novamente a conversa: o cliente manda uma mensagem (codificada) e depois recebe a mensagem que o servidor mandou, decodificando-a.

---

# Como testar:

## Nécessario executar primeiro o servidor, depois o cliente

### Execute em um terminal -> python servidor_tcp.py, em seguida, em outro terminal execute -> python cliente_tcp.py



