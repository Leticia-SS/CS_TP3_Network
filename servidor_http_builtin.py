from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import os

class MeuHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/':
            try:
                with open('index.html', 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                self._responder(200, 'text/html', conteudo)
            except FileNotFoundError:
                self._responder(404, 'text/plain', 'Not Found')
                
        elif self.path == '/status':
            timestamp = datetime.now().isoformat()
            resposta = {'status': 'ok', 'time': timestamp}
            self._responder(200, 'application/json', json.dumps(resposta))
            
        else:
            self._responder(404, 'text/plain', 'Not Found')
    
    def do_POST(self):
        if self.path == '/echo':
            content_length = int(self.headers.get('Content-Length', 0))
            corpo = self.rfile.read(content_length).decode('utf-8')
            
            self._responder(200, 'text/plain', corpo)
        else:
            self._responder(404, 'text/plain', 'Not Found')
    
    def _responder(self, status_code, content_type, corpo):
        self.send_response(status_code)
        self.send_header('Content-Type', f'{content_type}; charset=utf-8')
        self.send_header('Content-Length', str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo.encode('utf-8'))
    
    def log_message(self, format, *args):
        print(f"[+] {self.client_address[0]} - - [{self.log_date_time_string()}] {format % args}")

def main():
    HOST, PORT = '0.0.0.0', 8080
    
    if not os.path.exists('index.html'):
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Servidor HTTP com http.server</title>
</head>
<body>
    <h1>Servidor HTTP usando http.server</h1>
    <p>Rotas disponíveis:</p>
    <ul>
        <li>GET / - Esta página</li>
        <li>GET /status - Status do servidor em JSON</li>
        <li>POST /echo - Ecoa o corpo da requisição</li>
    </ul>
</body>
</html>""")
        print("[!] Arquivo index.html criado automaticamente")
    
    print(f"[+] Iniciando servidor HTTP em http://{HOST}:{PORT}")
    print("[+] Rotas disponíveis:")
    print("    GET  /       - Página HTML")
    print("    GET  /status - Status do servidor em JSON")
    print("    POST /echo   - Ecoa o corpo da requisição")
    print("\n[+] Testes:")
    print('    curl -v http://127.0.0.1:8080/status')
    print('    curl -X POST --data "abc" http://127.0.0.1:8080/echo')
    print("[+] Pressione Ctrl+C para encerrar\n")
    
    server = HTTPServer((HOST, PORT), MeuHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[-] Servidor encerrado")
        server.server_close()

if __name__ == "__main__":
    main()
