import socket

# Set the IP address and port number for the server
IP_ADDRESS = '192.168.0.122'
PORT = 5000

# Create a socket and bind it to the IP address and port
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP_ADDRESS, PORT))

# Listen for incoming connections
server_socket.listen()
print(f'Listening for incoming connections on {IP_ADDRESS}:{PORT}...')

# Accept an incoming connection
client_socket, client_address = server_socket.accept()
print(f'Accepted connection from {client_address}')

while True:    

    # Receive data over the socket connection
    data = client_socket.recv(1024)
    print(f'Received data: {data.decode()}')

    # save the data to a file
    

# Close the socket connection
client_socket.close()