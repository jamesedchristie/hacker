import socket
import sys

with socket.socket() as socket1:
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    address = (hostname, port)
    socket1.connect(address)
    message = sys.argv[3].encode()
    socket1.send(message)
    response = socket1.recv(1024)
    response = response.decode()
    print(response)
