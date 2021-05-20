import socket

server_url = 'putzeys.synology.me:5001/'
server = socket.gethostbyname(server_url)

# Create TCP socket with ipv4
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect client to server
client.connect((server, 80))

message = 'HEAD / HTTP/1.1\r\n'