import socket
import time
import sys

def main():
    HOST, PORT = "127.0.0.1", 5000
    max_tentativas = 3
    timeout_espera = 1  
    
    for tentativa in range(1, max_tentativas + 1):
        try:
            print(f"Tentativa {tentativa} de {max_tentativas}: Conectando a {HOST}:{PORT}")
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                sock.connect((HOST, PORT))
                
                print("[+] Conexão estabelecida!")
                
                mensagem = "PING\n"
                sock.sendall(mensagem.encode())
                print(f"[+] Enviado: {mensagem.strip()}")
                
                resposta = sock.recv(1024).decode()
                print(f"[+] Recebido: {resposta.strip()}")
                
                break
                
        except (ConnectionRefusedError, socket.timeout) as e:
            print(f"[-] Falha na tentativa {tentativa}: {e}")
            
            if tentativa < max_tentativas:
                print(f"[+] Aguardando {timeout_espera} segundo antes da próxima tentativa...")
                time.sleep(timeout_espera)
            else:
                print("[-] Todas as tentativas falharam. Encerrando.")
                sys.exit(1)
                
        except Exception as e:
            print(f"[-] Erro inesperado: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()

