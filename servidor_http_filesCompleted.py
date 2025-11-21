import socket
import os
from datetime import datetime

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
    ).encode('utf-8')

def parse_requisicao_http(dados):
    linhas = dados.split('\r\n')
    
    metodo, caminho, versao = linhas[0].split(' ') if linhas else ('', '', '')
    
    cabecalhos = {}
    indice_corpo = 0
    
    for i, linha in enumerate(linhas[1:], 1):
        if not linha:
            indice_corpo = i + 1
            break
        if ':' in linha:
            chave, valor = linha.split(':', 1)
            cabecalhos[chave.strip()] = valor.strip()
    
    corpo = '\r\n'.join(linhas[indice_corpo:]) if indice_corpo < len(linhas) else ''
    
    return metodo, caminho, versao, cabecalhos, corpo

def main():
    HOST, PORT = '0.0.0.0', 8080
    
    if not os.path.exists('index.html'):
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Servidor HTTP Python</title>
</head>
<body>
    <h1>Servidor HTTP Expandido</h1>
    <p>Rotas disponíveis:</p>
    <ul>
        <li>GET / - Esta página</li>
        <li>GET /status - Status do servidor em JSON</li>
        <li>POST /echo - Ecoa o corpo da requisição</li>
    </ul>
</body>
</html>""")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_servidor:
        sock_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_servidor.bind((HOST, PORT))
        sock_servidor.listen()
        
        print(f"[+] Servidor HTTP expandido escutando em http://{HOST}:{PORT}/")
        print("[+] Rotas disponíveis:")
        print("    GET  /       - Página HTML")
        print("    GET  /status - Status do servidor em JSON")
        print("    POST /echo   - Ecoa o corpo da requisição")
        print("\n[+] Testes:")
        print('    curl -v http://127.0.0.1:8080/status')
        print('    curl -X POST --data "abc" http://127.0.0.1:8080/echo')
        print('    curl -X POST --data "{\\"message\\":\\"hello\\"}" http://127.0.0.1:8080/echo')
        print("[+] Pressione Ctrl+C para encerrar\n")
        
        try:
            while True:
                sock_cliente, endereco = sock_servidor.accept()
                
                with sock_cliente:
                    dados = sock_cliente.recv(10240).decode('utf-8')
                    print(f"[+] Requisição recebida de {endereco}")
                    
                    metodo, caminho, versao, cabecalhos, corpo = parse_requisicao_http(dados)
                    
                    print(f"    Método: {metodo}, Caminho: {caminho}")
                    if cabecalhos.get('Content-Length'):
                        print(f"    Content-Length: {cabecalhos['Content-Length']}")
                    
                    if metodo == 'GET' and caminho == '/':
                        conteudo, sucesso = carregar_arquivo('index.html')
                        if sucesso:
                            resposta = gerar_resposta_http("200 OK", "text/html", conteudo)
                            print("    Resposta: 200 OK (index.html)")
                        else:
                            resposta = gerar_resposta_http("404 Not Found", "text/plain", "Not Found")
                            print("    Resposta: 404 Not Found")
                    
                    elif metodo == 'GET' and caminho == '/status':
                        timestamp = datetime.now().isoformat()
                        json_resposta = f'{{"status":"ok","time":"{timestamp}"}}'
                        resposta = gerar_resposta_http("200 OK", "application/json", json_resposta)
                        print("    Resposta: 200 OK (JSON status)")
                    
                    elif metodo == 'POST' and caminho == '/echo':
                        resposta = gerar_resposta_http("200 OK", "text/plain", corpo)
                        print(f"    Resposta: 200 OK (Echo: {corpo[:50]}{'...' if len(corpo) > 50 else ''})")
                    
                    else:
                        resposta = gerar_resposta_http("404 Not Found", "text/plain", "Not Found")
                        print("    Resposta: 404 Not Found")
                    
                    sock_cliente.sendall(resposta)
                    print("    Resposta enviada\n")
                    
        except KeyboardInterrupt:
            print("\n[-] Servidor HTTP encerrado")

if __name__ == "__main__":
    main()


