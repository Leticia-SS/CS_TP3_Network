import socket
import struct

porta = 8080
porta_network = socket.htons(8080)

print(f"Porta original: {porta}")
print(f"Porta após htons: {porta_network}")
print(f"Binário original: {bin(porta)}")
print(f"Binário após htons: {bin(porta_network)}")

# Demonstração com struct.pack
porta_packed = struct.pack('!H', 8080)
print(f"Struct.pack('!H', 8080): {porta_packed}")
print(f"Bytes em hex: {porta_packed.hex()}")

# Explicação
print("\n--- EXPLICAÇÃO ---")
print("A rede usa big-endian (ordem de bytes mais significativo primeiro)")
print("para garantir padronização na comunicação entre diferentes arquiteturas.")
print("htons() converte host byte order para network byte order (big-endian).")
