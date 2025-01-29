import socket
import os
import struct

def start_server():
    host = '0.0.0.0'
    port = 12345
    buffer_size = 8192
    
    # Crear socket UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    
    print(f"Servidor UDP escuchando en {host}:{port}")
    
    try:
        # Recibir información inicial del archivo
        data, client_address = server_socket.recvfrom(buffer_size)
        filename, file_size = struct.unpack('!256sQ', data[:264])
        filename = filename.strip(b'\x00').decode()
        
        print(f"Recibiendo archivo: {filename}")
        print(f"Tamaño del archivo: {file_size} bytes")
        print(f"Cliente: {client_address}")
        
        # Enviar confirmación de inicio
        server_socket.sendto(b"OK", client_address)
        
        # Preparar para recibir el archivo
        with open(f"received_{filename}", 'wb') as received_file:
            received_size = 0
            packet_num = 0
            
            while received_size < file_size:
                # Recibir paquete
                data, _ = server_socket.recvfrom(buffer_size)
                
                # Extraer número de secuencia y datos
                seq_num = struct.unpack('!I', data[:4])[0]
                file_data = data[4:]
                
                # Verificar si es el paquete esperado
                if seq_num == packet_num:
                    received_file.write(file_data)
                    received_size += len(file_data)
                    packet_num += 1
                    
                    # Enviar ACK
                    server_socket.sendto(struct.pack('!I', seq_num), client_address)
                    
                    # Mostrar progreso
                    progress = (received_size / file_size) * 100
                    print(f"Progreso: {progress:.2f}%", end='\r')
        
        print(f"\nArchivo recibido completamente: received_{filename}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        server_socket.close()
        print("\nServidor cerrado")

if __name__ == "__main__":
    start_server()
