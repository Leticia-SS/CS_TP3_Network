import socket
import signal
import sys

HOST = '0.0.0.0'  
PORT = 5000       

def main():
    sock_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock_servidor.bind((HOST, PORT))
        sock_servidor.listen()
        print(f"[+] Servidor de eco escutando em {HOST}:{PORT}")
        print("[+] Pressione Ctrl+C para encerrar o servidor.\n")

        while True:
            sock_cliente, endereco_cliente = sock_servidor.accept()
            print(f"[+] Conexão aceita de {endereco_cliente[0]}:{endereco_cliente[1]}")

            with sock_cliente:
                dados = sock_cliente.recv(1024)
                if not dados:
                    print(f"[-] Cliente {endereco_cliente} desconectou sem enviar dados.")
                    continue

                mensagem = dados.decode('utf-8')
                print(f"[Dados recebidos de {endereco_cliente}]: {mensagem}", end='')

                sock_cliente.sendall(dados)
                print(f"[+] Dados ecoados de volta para {endereco_cliente}.")

    except KeyboardInterrupt:
        print("\n\n[-] Encerrando servidor (KeyboardInterrupt).")
    finally:
        sock_servidor.close()
        print("[-] Socket do servidor fechado.")

if __name__ == "__main__":
    main()
