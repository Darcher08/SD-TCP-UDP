import socket
import os

def start_server():
    # Configuración del servidor
    host = '0.0.0.0'
    port = 12345
    
    # Crear socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Servidor escuchando en {host}:{port}")
    
    try:
        # Aceptar una única conexión
        client_socket, address = server_socket.accept()
        print(f"Conexión aceptada desde {address}")
        
        # Recibir nombre del archivo
        filename = client_socket.recv(1024).decode()
        if not filename:
            print("No se recibió nombre de archivo")
            return
            
        print(f"Recibiendo archivo: {filename}")
        
        # Abrir archivo para escribir en modo binario
        with open(f"received_{filename}", 'wb') as file:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                file.write(data)
        
        print(f"Archivo recibido y guardado como received_{filename}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Cerrar las conexiones
        client_socket.close()
        server_socket.close()
        print("Servidor cerrado")

if __name__ == "__main__":
    start_server()
