import socket
import os

def get_local_ip():
    """Ottiene l'indirizzo IP locale della macchina"""
    try:
        # Crea un socket per connettersi a un server esterno
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Non è necessario che la connessione avvenga realmente
        s.connect(("8.8.8.8", 80))
        # Ottiene l'indirizzo IP locale usato per la connessione
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # Fallback: ottiene il nome host e lo risolve in un indirizzo IP
        return socket.gethostbyname(socket.gethostname())

# Ottieni l'IP
ip_address = get_local_ip()
print(f"Indirizzo IP locale rilevato: {ip_address}")

serverIp = f"const SERVER_IP = \"{ip_address}\";"

# Scrivi il contenuto nel file
with open('static/ip_config.js', 'w') as f:
    f.write(serverIp)

print(f"File 'static/ip_config.js' generato con successo") 