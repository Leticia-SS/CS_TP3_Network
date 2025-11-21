import socket
import ssl

def main():
    HOST, PORT = '0.0.0.0', 8443
    
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_3
    
    context.load_cert_chain('localhost.crt', 'localhost.key')
    
    context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!eNULL:!MD5:!DSS:!RC4:!3DES')
    
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE 
    
    print("[+] Configurações de segurança aplicadas:")
    print(f"    - TLS mínimo: {context.minimum_version}")
    print(f"    - TLS máximo: {context.maximum_version}")
    print(f"    - Cifras: {context.get_ciphers()[:3]}...")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_servidor:
        sock_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_servidor.bind((HOST, PORT))
        sock_servidor.listen()
        
        with context.wrap_socket(sock_servidor, server_side=True) as sock_tls:
            print(f"[+] Servidor HTTPS SEGURO escutando em https://{HOST}:{PORT}/")
            print("[+] Testes:")
            print('    curl -vk --tlsv1.3 --tls-max 1.3 https://127.0.0.1:8443/')
            print('    curl -vk --tlsv1.2 --tls-max 1.2 https://127.0.0.1:8443/')
            print('    # Tentativa com TLS 1.1 deve FALHAR:')
            print('    curl -vk --tlsv1.1 --tls-max 1.1 https://127.0.0.1:8443/')
            print("[+] Pressione Ctrl+C para encerrar\n")
            
            try:
                while True:
                    try:
                        sock_cliente, endereco = sock_tls.accept()
                        
                        cipher = sock_cliente.cipher()
                        version = sock_cliente.version()
                        print(f"[+] Conexão ACEITA de {endereco}")
                        print(f"    TLS: {version}, Cifra: {cipher[0]}")
                        
                        with sock_cliente:
                            dados = sock_cliente.recv(1024).decode('utf-8')
                            
                            if dados.startswith('GET /'):
                                corpo_resposta = "hello world! (TLS seguro)"
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
                            print(f"    Resposta enviada\n")
                            
                    except ssl.SSLError as e:
                        print(f"[-] Conexão REJEITADA de {endereco}: {e}\n")
                        
            except KeyboardInterrupt:
                print("\n[-] Servidor HTTPS seguro encerrado")

if __name__ == "__main__":
    main()
