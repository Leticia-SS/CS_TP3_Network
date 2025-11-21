import socket

def main():
    HOST, PORT = "127.0.0.1", 6000
    mensagens = ["um", "dois", "tres"]
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        for msg in mensagens:
            print(f"[+] Enviando: {msg}")
            sock.sendto(msg.encode(), (HOST, PORT))
            
            try:
                sock.settimeout(2.0)
                resposta, servidor = sock.recvfrom(1024)
                print(f"[+] Resposta: {resposta.decode()}")
            except socket.timeout:
                print("[-] Timeout: nenhuma resposta recebida")
            
            print()

if __name__ == "__main__":
    main()

