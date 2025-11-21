import socket
import os

def carregar_arquivo(caminho_arquivo):
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            return arquivo.read(), True
    except FileNotFoundError:
        return None, False

def gerar_resposta_http(status_code, content_type, corpo):
    return (
        f"HTTP/1.1 {status_code}\r\n"
        f"Content-Type: {content_type}; charset=utf-8\r\n"
        f"Content-Length: {len(corpo)}\r\n"
        "\r\n"
        f"{corpo}"
    )

def main():
    HOST, PORT = '0.0.0.0', 8080
    
    if not os.path.exists('index.html'):
        print("[!] Criando arquivo index.html de exemplo...")
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Servidor HTTP Python</title>
</head>
<body>
    <h1>Hello World from HTML!</h1>
    <p>Este é um arquivo index.html servido pelo servidor HTTP customizado.</p>
</body>
</html>""")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_servidor:
        sock_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_servidor.bind((HOST, PORT))
        sock_servidor.listen()
        
        print(f"[+] Servidor HTTP com arquivos estáticos escutando em http://{HOST}:{PORT}/")
        print("[+] Testes:")
        print("    curl -v http://127.0.0.1:8080/")
        print("    curl -v http://127.0.0.1:8080/outro")
        print("[+] Pressione Ctrl+C para encerrar\n")
        
        try:
            while True:
                sock_cliente, endereco = sock_servidor.accept()
                
                with sock_cliente:
                    dados = sock_cliente.recv(1024).decode('utf-8')
                    print(f"[+] Requisição recebida de {endereco}")
                    
                    linhas = dados.split('\r\n')
                    if linhas and linhas[0].startswith('GET'):
                        caminho = linhas[0].split(' ')[1]
                        print(f"    Caminho: {caminho}")
                        
                        if caminho == '/':
                            conteudo, sucesso = carregar_arquivo('index.html')
                            if sucesso:
                                resposta = gerar_resposta_http("200 OK", "text/html", conteudo)
                                print("    Resposta: 200 OK (index.html)")
                            else:
                                resposta = gerar_resposta_http("404 Not Found", "text/plain", "Not Found")
                                print("    Resposta: 404 Not Found")
                        
                        else:
                            resposta = gerar_resposta_http("404 Not Found", "text/plain", "Not Found")
                            print("    Resposta: 404 Not Found")
                    
                    else:
                        resposta = gerar_resposta_http("400 Bad Request", "text/plain", "Bad Request")
                        print("    Resposta: 400 Bad Request")
                    
                    sock_cliente.sendall(resposta.encode('utf-8'))
                    print("    Resposta enviada\n")
                    
        except KeyboardInterrupt:
            print("\n[-] Servidor HTTP encerrado")

if __name__ == "__main__":
    main()


