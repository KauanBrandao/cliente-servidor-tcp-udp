import socket
import threading
import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

dispositivos_conectados = {}

def atender_cliente(conn, ip):
    print(f"\n[+] Nova máquina conectada: {ip}")
    
    dispositivos_conectados[ip] = {
        "cpu": 0, "ram": 0, "disco": 0, 
        "rede_env": 0, "rede_rec": 0, 
        "processos": 0, "uptime": 0, 
        "energia": "N/A", "status": "Conectado"
    }

    try:
        while True:
            dados = conn.recv(1024).decode('utf-8')
            if not dados:
                break
                
            info = json.loads(dados)
            
            dispositivos_conectados[ip].update({
                "cpu": info.get('cpu', 0),
                "ram": info.get('ram', 0),
                "disco": info.get('disco', 0),
                "rede_env": info.get('rede_env', 0),
                "rede_rec": info.get('rede_rec', 0),
                "processos": info.get('processos', 0),
                "uptime": info.get('uptime', 0),
                "energia": info.get('energia', 'N/A'),
                "status": "Conectado"
            })
    except Exception as e:
        pass
    finally:
        print(f"\n[-] Máquina desconectada: {ip}")
        if ip in dispositivos_conectados:
            dispositivos_conectados[ip]["status"] = "Desconectado"
        conn.close()

def iniciar_servidor_tcp():
    HOST = '0.0.0.0'
    PORT = 8080
    
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen(5)
    print(f"[*] Servidor TCP de Telemetria escutando na porta {PORT}...")

    while True:
        conn, addr = servidor.accept()
        ip = addr[0]
        
        thread = threading.Thread(target=atender_cliente, args=(conn, ip))
        thread.start()

@app.route('/dados', methods=['GET'])
def obter_dados():
    return jsonify(dispositivos_conectados)

if __name__ == '__main__':
    tcp_thread = threading.Thread(target=iniciar_servidor_tcp)
    tcp_thread.daemon = True
    tcp_thread.start()
    
    print("[*] Servidor API Web iniciando na porta 5000...")
    app.run(host='0.0.0.0', port=5000)