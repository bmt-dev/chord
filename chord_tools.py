import socket
import json

def json_recv(clientsocket):
    data = b''
    while True:
        tmp = clientsocket.recv(1024)
        if tmp == b'':
            break
        data += tmp
    result = json.loads(data)
    print('[' + result['type'] + '] received')
    return result
            
def json_send(ip, port, data):
    print('Sending ['+ data['type'] + '] request to ' + ip + ' ' + str(port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.send(json.dumps(data).encode())
