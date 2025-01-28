import socket
import os

def start_server():
    # Configuración del servidor
    host = '0.0.0.0'  # Escucha en todas las interfaces
    port = 12345      # Puerto arbitrario
    
    # Crear socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permitir reutilizar el puerto
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Vincular socket al host y puerto
    server_socket.bind((host, port))
    
    # Escuchar conexiones entrantes
    server_socket.listen(1)
    print(f"Servidor escuchando en {host}:{port}")
    
    while True:
        # Aceptar conexión
        client_socket, address = server_socket.accept()
        print(f"Conexión aceptada desde {address}")
        
        try:
            # Recibir nombre del archivo
            filename = client_socket.recv(1024).decode()
            print(f"Recibiendo archivo: {filename}")
            
            # Abrir archivo para escribir en modo binario
            with open(f"received_{filename}", 'wb') as file:
                while True:
                    # Recibir datos en chunks de 4096 bytes
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    file.write(data)
            
            print(f"Archivo recibido y guardado como received_{filename}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        finally:
            client_socket.close()
            print("Conexión cerrada")

if __name__ == "__main__":
    start_server()