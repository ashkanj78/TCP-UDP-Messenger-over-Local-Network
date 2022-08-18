import socket
import select
import sys
import pickle
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 9000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP,PORT))
server_socket.listen()
sockets_list = [server_socket]
clients = {}
print(f'Listening for connections on {IP}:{PORT}')
def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False

name=[]
while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user

            print('Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8')))
            name.append(user['data'].decode('utf-8'))
        else:
            message = receive_message(notified_socket)
            if message is False or (message["data"].decode("utf-8") == "bye") :
                for person in name:
                    if person == clients[notified_socket]['data'].decode('utf-8'):
                        name.remove(person)

                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]

                continue
            user = clients[notified_socket]
            
            vector=(message["data"].decode("utf-8")).split("$$$$$$$")
            if len(vector)==1:
                print_message=vector[0]
            else:
                print_message=vector[1]
                client_name=vector[0]
                
            print(f'Received message from {user["data"].decode("utf-8")}: {print_message}')
            host_name=user["data"].decode("utf-8")
            check=False
                
            strsend=""
            for each in name:
                strsend = strsend + str(each) +","
            if print_message == "List":
                strsend = strsend.encode('utf-8')
                strsend_header = f"{len(strsend):<{HEADER_LENGTH}}".encode('utf-8')
                for client_socket in clients:
                    if client_socket == notified_socket:
                        client_socket.send(user['header'] + user['data']+ strsend_header + strsend)
            elif client_name=="Broadcast":
                for client_socket in clients:
                    if client_socket != notified_socket:   
                        print("b")
                        strsend = print_message.encode('utf-8')
                        strsend_header = f"{len(strsend):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(user['header'] + user['data'] + strsend_header + strsend)
                    if client_socket == notified_socket:
                        m ="sent"
                        strsend = m.encode('utf-8')
                        strsend_header = f"{len(strsend):<{HEADER_LENGTH}}".encode('utf-8')
                        client_socket.send(user['header'] + user['data']+ strsend_header + strsend)
            else :
                if client_name in name and client_name !=host_name:
                    for client_socket in clients:
                        if clients[client_socket]['data'].decode("utf-8") == client_name:
                            strsend = print_message.encode('utf-8')
                            strsend_header = f"{len(strsend):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(user['header'] + user['data'] + strsend_header + strsend)
                        if clients[client_socket]['data'].decode("utf-8") == host_name:
                            m ="sent"
                            strsend = m.encode('utf-8')
                            strsend_header = f"{len(strsend):<{HEADER_LENGTH}}".encode('utf-8')
                            client_socket.send(user['header'] + user['data']+ strsend_header + strsend)
                
                elif client_name in name and client_name ==host_name:
                    m ="you sent the message to yourself "
                    strsend = m.encode('utf-8')
                    strsend_header = f"{len(strsend):<{HEADER_LENGTH}}".encode('utf-8')
                    for client_socket in clients:
                        if clients[client_socket]['data'].decode("utf-8") == host_name:
                            client_socket.send(user['header'] + user['data']+ strsend_header + strsend)
                else:
                    m ="notice:can not find client named <"+client_name+"> in online clients"
                    strsend = m.encode('utf-8')
                    strsend_header = f"{len(strsend):<{HEADER_LENGTH}}".encode('utf-8')
                    for client_socket in clients:
                        if clients[client_socket]['data'].decode("utf-8") == host_name:
                            client_socket.send(user['header'] + user['data']+ strsend_header + strsend)
    
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
