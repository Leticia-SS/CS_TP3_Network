import socket

def main():
    HOST, PORT = "0.0.0.0", 6000
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))
        print(f"[+] Servidor UDP escutando em {HOST}:{PORT}")
        
        while True:
            try:
                dados, endereco = sock.recvfrom(1024)
                print(f"[+] Recebido de {endereco}: {dados.decode()}")
                
                resposta = b"OK:" + dados
                sock.sendto(resposta, endereco)
                print(f"[+] Enviado para {endereco}: {resposta.decode()}")
                
            except KeyboardInterrupt:
                print("\n[-] Servidor encerrado.")
                break

if __name__ == "__main__":
    main()

