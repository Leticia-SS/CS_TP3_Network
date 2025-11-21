import socket
import threading
import sys

HOST = '0.0.0.0'
PORT = 5000

def handle_cliente(sock_cliente, endereco):
    print(f"[Thread {threading.current_thread().name}] Cliente {endereco} conectado")
    
    with sock_cliente:
        while True:
            try:
                dados = sock_cliente.recv(1024)
                if not dados:
                    break
                
                mensagem = dados.decode('utf-8')
                print(f"[Thread {threading.current_thread().name}] Recebido de {endereco}: {mensagem.strip()}")
                
                sock_cliente.sendall(dados)
                print(f"[Thread {threading.current_thread().name}] Ecoado para {endereco}: {mensagem.strip()}")
                
            except ConnectionResetError:
                break
    
    print(f"[Thread {threading.current_thread().name}] Cliente {endereco} desconectado")

def main():
    sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock_servidor.bind((HOST, PORT))
        sock_servidor.listen()
        print(f"[+] Servidor multithread escutando em {HOST}:{PORT}")
        print("[+] Pressione Ctrl+C para encerrar\n")
        
        threads = []
        
        while True:
            sock_cliente, endereco = sock_servidor.accept()
            
            thread = threading.Thread(
                target=handle_cliente,
                args=(sock_cliente, endereco),
                name=f"Cliente-{endereco[1]}"
            )
            thread.daemon = True
            thread.start()
            threads.append(thread)
            
    except KeyboardInterrupt:
        print("\n[-] Encerrando servidor...")
    finally:
        sock_servidor.close()
        print("[-] Socket do servidor fechado")

if __name__ == "__main__":
    main( )

