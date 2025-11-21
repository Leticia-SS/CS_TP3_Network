import socket

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2.0)  # Timeout de 2 segundos
    sock.connect(('192.0.2.1', 12345))
    print("Conectado com sucesso!")
except socket.timeout:
    print("timeout")
except Exception as e:
    print(f"Erro: {e}")
finally:
    sock.close()
