import socket

def main():
    HOST, PORT = '0.0.0.0', 8080
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_servidor:
        sock_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_servidor.bind((HOST, PORT))
        sock_servidor.listen()
        
        print(f"[+] Servidor HTTP escutando em http://{HOST}:{PORT}/")
        print("[+] Teste com: curl -v http://127.0.0.1:8080/")
        print("[+] Pressione Ctrl+C para encerrar\n")
        
        try:
            while True:
                sock_cliente, endereco = sock_servidor.accept()
                
                with sock_cliente:
                    dados = sock_cliente.recv(1024).decode('utf-8')
                    print(f"[+] Requisição recebida de {endereco}:")
                    print(dados)
                    
                    if dados.startswith('GET /'):
                        corpo_resposta = "hello world!"
                        resposta_http = (
                            "HTTP/1.1 200 OK\r\n"
                            "Content-Type: text/plain; charset=utf-8\r\n"
                            f"Content-Length: {len(corpo_resposta)}\r\n"
                            "\r\n"
                            f"{corpo_resposta}"
                        )
                    else:
                        corpo_resposta = "404 - Página não encontrada"
                        resposta_http = (
                            "HTTP/1.1 404 Not Found\r\n"
                            "Content-Type: text/plain; charset=utf-8\r\n"
                            f"Content-Length: {len(corpo_resposta)}\r\n"
                            "\r\n"
                            f"{corpo_resposta}"
                        )
                    
                    sock_cliente.sendall(resposta_http.encode('utf-8'))
                    print(f"[+] Resposta enviada para {endereco}\n")
                    
        except KeyboardInterrupt:
            print("\n[-] Servidor HTTP encerrado")

if __name__ == "__main__":
    main()


