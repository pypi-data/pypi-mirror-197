import socket

# create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send a message to the server
server_address = ("localhost", 8000)
message = b"Hello, server!"
client_socket.sendto(message, server_address)

# close the socket
client_socket.close()
