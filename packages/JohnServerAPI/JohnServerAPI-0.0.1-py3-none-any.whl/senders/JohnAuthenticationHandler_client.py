import socket
import ssl

HOST = 'localhost'
PORT = 12345

# Create an SSL context and set the SSL/TLS protocol and cipher suite
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# ssl_context.set_ciphers('AES256-SHA256')
# ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
ssl_context.load_cert_chain(certfile='client.crt', keyfile='client.key')
# Load the CA file as a trusted root CA
ssl_context.load_verify_locations(cafile='ca.crt')
# Wrap the socket with SSL/TLS
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    ssl_sock = ssl_context.wrap_socket(sock, server_hostname=HOST)

    # Connect to the server
    ssl_sock.connect((HOST, PORT))

    # Verify the server's certificate
    cert = ssl_sock.getpeercert()
    if not cert:
        print('Server did not provide a certificate')
        ssl_sock.close()
    else:
        print(f'Server certificate: {cert}')

    # Send and receive data over the encrypted connection
    ssl_sock.sendall(b'Hello, server!')
    data = ssl_sock.recv(1024)
    print(f'Received from server: {data}')

    # Close the connection
    ssl_sock.close()

