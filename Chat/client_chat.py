import socket
import threading
import customtkinter as ctk

IP_SERVIDOR = '18.217.154.195'
PORTA = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receber_mensagens():
    """Esta função roda em segundo plano, escutando a rede"""
    while True:
        try:
            mensagem = cliente.recv(1024).decode()
            
            caixa_texto.insert(ctk.END, f"Contato: {mensagem}\n")
            caixa_texto.see(ctk.END) 
        except:
            print("Conexão com o servidor foi perdida.")
            cliente.close()
            break

def enviar_mensagem(evento=None):
    """Pega o texto da interface e joga na rede"""
    mensagem = campo_entrada.get()
    if mensagem:
      
        caixa_texto.insert(ctk.END, f"Você: {mensagem}\n")
        caixa_texto.see(ctk.END)
        
        cliente.send(mensagem.encode())
     
        campo_entrada.delete(0, ctk.END)


ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

janela = ctk.CTk()
janela.title("Chat Universitário")
janela.geometry("400x500")

caixa_texto = ctk.CTkTextbox(janela, width=380, height=400, corner_radius=10)
caixa_texto.pack(pady=10)


frame_inferior = ctk.CTkFrame(janela, fg_color="transparent")
frame_inferior.pack(pady=5, fill="x", padx=10)

campo_entrada = ctk.CTkEntry(frame_inferior, width=280, placeholder_text="Digite sua mensagem...", corner_radius=20)
campo_entrada.pack(side="left", padx=5)

janela.bind('<Return>', enviar_mensagem) 


botao_enviar = ctk.CTkButton(frame_inferior, text="Enviar", width=80, corner_radius=20, fg_color="#FF69B4", hover_color="#FF1493", command=enviar_mensagem)
botao_enviar.pack(side="right")


try:
    cliente.connect((IP_SERVIDOR, PORTA))
    caixa_texto.insert(ctk.END, "[Sistema] Conectado ao servidor!\n\n")
    
    thread_receber = threading.Thread(target=receber_mensagens)
    thread_receber.start()
    
    janela.mainloop()

except Exception as e:
    print(f"Erro ao conectar: {e}. O servidor está rodando?")