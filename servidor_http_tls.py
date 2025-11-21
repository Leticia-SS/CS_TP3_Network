import socket
import ssl

def main():
    HOST, PORT = '0.0.0.0', 8443
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('localhost.crt', 'localhost.key')
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_servidor:
        sock_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_servidor.bind((HOST, PORT))
        sock_servidor.listen()
        
        with context.wrap_socket(sock_servidor, server_side=True) as sock_tls:
            print(f"[+] Servidor HTTPS escutando em https://{HOST}:{PORT}/")
            
            try:
                while True:
                    sock_cliente, endereco = sock_tls.accept()
                    print(f"[+] Conexão TLS aceita de {endereco}")
                    
                    with sock_cliente:
                        dados = sock_cliente.recv(1024).decode('utf-8')
                        print(f"[+] Requisição HTTP recebida via TLS:")
                        
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
                        print(f"[+] Resposta HTTP enviada via TLS\n")
                        
            except KeyboardInterrupt:
                print("\n[-] Servidor HTTPS encerrado") 
            except ssl.SSLError as e:
                print(f"[-] Erro SSL: {e}")
            except Exception as e:
                print(f"[-] Erro inesperado: {e}")

if __name__ == "__main__":
    main()


