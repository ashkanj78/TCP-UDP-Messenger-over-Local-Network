import socket
import select
import errno
import sys
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = int(sys.argv[2])
my_username = sys.argv[1]

def exit_from_server(client_socket):
    message="bye"
    if message:
        x=message
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
        if x=="bye":
            print('Connection closed by the client')
            exit()

def send_message(message,client_socket):
    if message:        
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)

def receive_message(client_socket,out):
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            if username != my_username: 
                out[0]=out[0]+ username+' > '+message+'\n'
            else:
                if message=="sent":
                    return True
                username="Server"
                out[0]=out[0]+ username+' > '+message+'\n'
            return True
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
    except Exception as e:
        print("Reading error: ".format(str(e)))
        sys.exit()


def receive_server_message(client_socket):
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            if username != my_username: 
                print_message=username+' > '+message
            else:
                if message=="sent":
                    print("%the message was sent correctly%")
                    return True
                username="Server"
                print(username+' > '+message)
            return True
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
    except Exception as e:
        print("Reading error: ".format(str(e)))
        sys.exit()

def receive_List(client_socket): 
    try:
        while True:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            client_list=message[:-1].split(",")
            print("Online clients: " , client_list)
            return True
    except IOError as e:  
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()
    except Exception as e:
        print("Reading error: ".format(str(e)))
        sys.exit()

def List(client_socket):
    message = "List"
    send_message(message,client_socket)
    receive_List(client_socket)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)
message_l=["",""]
print("commands\n 1.List :to see online clients \n 2.receive :receive message from other clients or server\n 3.send :send message to other clients\n 4.exit :close connection ")
print("#for Broadcast to all client , for #to enter <Broadcast>")
print("#for private message,for #to enter client name")
while True:
    command=str(input(">>"))
    while receive_message(client_socket,message_l):
        pass
    if command == "List" or command == "list" :
        List(client_socket)
        while True:
            if receive_List(client_socket):
                break   
    elif command == "receive" or command == "Receive":
        if len(message_l[0][:-1])!=0:        
            print(message_l[0][:-1])
        message_l[0]=""

    elif command == "send" or command == "Send":

        receiver=input("to>")
        message=str(input('message > '))
        send_message(receiver+"$$$$$$$"+message,client_socket)
        while True:
            if receive_server_message(client_socket):
                break

    elif command == "Exit" or command == "exit":
        exit_from_server(client_socket)
    else:
        print("invalid command,try again")


    
    
    