import socket
from threading import Thread
from datetime import datetime
import shutil
import os

def serve_msg():
    msg = datetime.now().strftime("[%H:%M:%S] ") + "Server:"
    return msg

# Function to handle incoming messages from clients
def listen(client):
    try:
        while True:
            msg = client.recv(1024).decode()    # Receive messages from client
            print(f"incoming message: {msg}")
            if msg == "QUIT_REQUEST_FLAG":  # Handle client disconnection

                for user in users:
                    exit_msg = f"{serve_msg()} user {user_names[users.index(client)]} has left the chat"
                    if user != client:
                        user.send(exit_msg.encode())

                client.close()
                print(f"user {user_names[users.index(client)]} quit")
                users.remove(client)
                print(f"Number of  users: {len(users)}")
                break   # Exit the loop and stop listening for this client
            elif msg == "ATTACHMENT_FLAG":   # Handle file transfer request
                file_name = client.recv(1024).decode()  # Receive file name from client
                client.send(f"ATTACHMENT_FLAG = 0".encode())    # Acknowledge file transfer request
                client.send(file_name.encode())  # Send back file name confirmation
                data = client.recv(1024).decode()
                file = open(file_name, 'w')
                file.write(data)
                file.close()
                shutil.move(file_name, "downloads")
                client.send(f"{serve_msg()}File recieved".encode())
                curr_time = datetime.now().strftime("[%H:%M:%S] ")
                send_msgs(f"{serve_msg()} {user_names[users.index(client)]} has sent an attachment")
                print(data)
                send_msgs(data)
            else:   # Print normal chat messages
                msg = user_names[users.index(client)] + ": " + msg
                curr_time = datetime.now().strftime("[%H:%M:%S] ")
                msg = curr_time + msg + "\n"
                for user in users:
                    if user != client:
                        user.send(msg.encode())
    except:     # Handles client disconnection from server, sends message to all clients
        msg = f"{serve_msg()} user {user_names[users.index(client)]} has left the chat"
        for user in users:
            if user != client:
                user.send(msg.encode())
        # Server side message indicating quitting clients
        client.close()
        print(f"user {user_names[users.index(client)]} quit")
        users.remove(client)
        print(f"Number of  users: {len(users)}")






def send_msgs(msg):
    messages.append(msg)
    for user in users:
        if msg != "ATTACHMENT_FLAG= 1":
            user.send(msg.encode())

def check_user_names(user_name):
    if len(user_names) != 0:
        for users in user_names:
            print(users)
            if user_name == users:
                return 0
    return 1


# Main, starts server and accepts incoming client connections
if __name__ == '__main__':
    users = []
    user_names = []
    user_addr = []
    messages = []
    chat_room_size = 3

    server_port = 18006 # Define the port number for the server
    host_name = 'local host'

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket
    name = socket.gethostname()
    server_ip = socket.gethostbyname(name)  # get the server ip
    serverSocket.bind(('', server_port))    # Bind the socket to localhost and port
    serverSocket.listen()        # Start listening for incoming connections

    print("server IP= ", server_ip, "port= ", server_port)
    print('The server is ready to receive')


    while True:

        connectionSocket, addr = serverSocket.accept()  # Accept a new client connection
        print("join requested")
        connectionSocket.send('server connection acknowledged\n'.encode())

        msg = connectionSocket.recv(1024).decode()


        user_name_flag = 0

        if msg == "JOIN_REQUEST_FLAG":
            print("username requested")
            if (len(users) > chat_room_size + 1):   # Rejects user if chatroom is full
                print("Chatroom full user rejected")
                connectionSocket.send('JOIN_REJECT_FLAG'.encode())
                connectionSocket.close()
            connectionSocket.send("JOIN_REQUEST_FLAG = 1".encode())


            while user_name_flag == 0:





                user_name = connectionSocket.recv(1024).decode()
                user_name_flag = check_user_names(user_name)
                if user_name_flag == 0:
                    connectionSocket.send('JOIN_REJECT_FLAG'.encode())

                else:
                    connectionSocket.send('JOIN_ACCEPT_FLAG = 1'.encode())
                    if len(messages) != 0:
                        history = ""
                        for i in messages:
                            history += history + i
                        connectionSocket.send(history.encode())
                    msg = f"{serve_msg()} {user_name} has joined the chat\n"
                    send_msgs(msg)
                    users.append(connectionSocket)
                    user_names.append(user_name)
                    user_addr.append(addr)

                    # Start a new thread to handle communication with the connected client
                    connectionSocket.send(f"{serve_msg()} Welcome to the chat {user_name}\n".encode())
                    thread = Thread(target=listen, args=(connectionSocket,))

                    thread.daemon = True

                    thread.start()
                    print(f"New user added. Number of  users: {len(users)}")
                    user_name_flag == 1




        elif msg == "REPORT_REQUEST_FLAG":
            print("report requested")
            if len(users) > 0:

                string = ""
                for i in range(len(user_names)):
                    string += user_names[i] + " ip: " + str(user_addr[i][0]) + " port: " + str(user_addr[i][0] + "\n")
                    print(string)
                connectionSocket.send(string.encode())
            else:
                connectionSocket.send('chat room empty'.encode())
        elif msg == "QUIT_REQUEST_FLAG":
            connectionSocket.send("QUIT_ACCEPT_FLAG".encode())
            connectionSocket.close()
            print(f"user {connectionSocket} connection terminated")
            break











    msg = ""


    for connectionSocket in users:
        connectionSocket.close()

    serverSocket.close()