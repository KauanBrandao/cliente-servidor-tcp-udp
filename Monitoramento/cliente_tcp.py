import socket
import psutil
import json
import time

HOST_SERVIDOR = '54.232.166.204'
PORTA_SERVIDOR = 8080

def coletar_dados():
    
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory().percent
    disco = psutil.disk_usage('/').percent
    
    
    rede = psutil.net_io_counters()
    mb_enviados = round(rede.bytes_sent / (1024 * 1024), 2)
    mb_recebidos = round(rede.bytes_recv / (1024 * 1024), 2)
    
    
    processos = len(psutil.pids())
    boot_time = psutil.boot_time()
    uptime_horas = round((time.time() - boot_time) / 3600, 1)
    
    
    bateria = psutil.sensors_battery()
    energia = "Tomada" if (bateria is None or bateria.power_plugged) else f"Bateria ({bateria.percent}%)"

    return {
        "cpu": cpu,
        "ram": ram,
        "disco": disco,
        "rede_env": mb_enviados,
        "rede_rec": mb_recebidos,
        "processos": processos,
        "uptime": uptime_horas,
        "energia": energia
    }

def enviar_dados():
    print(f"Iniciando serviço avançado de telemetria para {HOST_SERVIDOR}...")
    
    while True:
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((HOST_SERVIDOR, PORTA_SERVIDOR))
            print(f"\n[🟢 CONECTADO] Link estabelecido! Transmitindo pacote completo.")
            
            while True:
                payload = json.dumps(coletar_dados())
                cliente.send(payload.encode('utf-8'))
                
                print(f"[SUCESSO] Pacote enviado -> Tamanho: {len(payload)} bytes")
                time.sleep(2)
                
        except Exception as e:
            print(f"\n[🔴 DESCONECTADO] Falha na rede: {e}")
            print("Tentando reconectar em 5 segundos...")
            time.sleep(5)

if __name__ == '__main__':
    enviar_dados()