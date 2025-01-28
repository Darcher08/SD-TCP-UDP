import socket
import os
import struct
import time

def send_file(filename, host, port):
    # Crear socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5.0)  # Timeout de 5 segundos para retransmisiones
    
    # Configuración
    buffer_size = 8192
    server_address = (host, port)
    
    try:
        # Verificar si el archivo existe
        if not os.path.exists(filename):
            raise FileNotFoundError(f"El archivo {filename} no existe")
        
        # Obtener tamaño del archivo
        file_size = os.path.getsize(filename)
        
        # Enviar información inicial del archivo
        file_info = struct.pack('!256sQ', os.path.basename(filename).encode(), file_size)
        client_socket.sendto(file_info, server_address)
        
        # Esperar confirmación del servidor
        data, _ = client_socket.recvfrom(buffer_size)
        if data != b"OK":
            raise Exception("No se recibió confirmación del servidor")
        
        # Abrir y enviar el archivo
        with open(filename, 'rb') as file:
            packet_num = 0
            
            while True:
                file_data = file.read(buffer_size - 4)  # -4 bytes para el número de secuencia
                if not file_data:
                    break
                
                while True:
                    try:
                        # Preparar paquete con número de secuencia
                        packet = struct.pack('!I', packet_num) + file_data
                        client_socket.sendto(packet, server_address)
                        
                        # Esperar ACK
                        data, _ = client_socket.recvfrom(buffer_size)
                        ack = struct.unpack('!I', data)[0]
                        
                        if ack == packet_num:
                            # ACK recibido, continuar con el siguiente paquete
                            packet_num += 1
                            # Mostrar progreso
                            progress = (file.tell() / file_size) * 100
                            print(f"Progreso: {progress:.2f}%", end='\r')
                            break
                            
                    except socket.timeout:
                        print(f"\nTimeout - Reintentando paquete {packet_num}")
                        continue
        
        print("\nArchivo enviado exitosamente")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        client_socket.close()

if __name__ == "__main__":
    # Configuración del cliente
    server_host = 'localhost'  # Cambiar por la IP del servidor
    server_port = 12345       # Mismo puerto que el servidor
    file_to_send = 'gatito.png'  # Nombre del archivo multimedia a enviar
    
    send_file(file_to_send, server_host, server_port)