import socket
import sys

def serve_forever(port, host = 'localhost'):
    while True:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = (host, port)
        try:
            client_socket.bind(server_address)
            client_socket.listen(1)
            _, client_address = client_socket.accept()
            print(f'Client address is {client_address[0]}')
            print(f'Client port is {client_address[1]}')
            client_socket.close()
        except (socket.error, OSError, ValueError):
            client_socket.close()


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    if ( len(sys.argv) > 3):
        print("Incorrect input data. Enter host and listening port")
    elif len(sys.argv) == 2:
        serve_forever(int(sys.argv[1]))
    elif len(sys.argv) == 1:
        serve_forever(8080)
    else:
        serve_forever(int(sys.argv[1]), sys.argv[2])