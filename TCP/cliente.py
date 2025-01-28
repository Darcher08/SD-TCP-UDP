import socket
import os

def send_file(filename, host, port):
    # Crear socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # STREAM especifico para TCP
    
    try:
        # Conectar al servidor
        client_socket.connect((host, port))
        print(f"Conectado a {host}:{port}")
        
        # Verificar si el archivo existe
        if not os.path.exists(filename):
            raise FileNotFoundError(f"El archivo {filename} no existe")
        
        # Enviar nombre del archivo
        client_socket.send(os.path.basename(filename).encode())
        
        # Abrir y enviar el archivo
        with open(filename, 'rb') as file:
            while True:
                # Leer archivo en chunks de 4096 bytes
                data = file.read(4096)
                if not data:
                    break
                client_socket.send(data)
        
        print("Archivo enviado exitosamente")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        client_socket.close()
        print("Conexión cerrada")

if __name__ == "__main__":
    # Configuración del cliente
    server_host = 'localhost'  # Cambiar por la IP del servidor
    server_port = 12345       # Mismo puerto que el servidor
    file_to_send = 'archivo.txt'  # Nombre del archivo a enviar
    
    send_file(file_to_send, server_host, server_port)