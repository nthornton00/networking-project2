from socket import *
from threading import Thread
import sys
from datetime import datetime
import shutil




# Function to send chat messages from the client
# Handles special commands for quitting and sending attachments
def send_chat(clientSocket):
    try:
        while True:


            sentence = input() #Get user input
            file_name = sentence
            file_path = sentence.split(".")




            if sentence.lower() == "#q":    #Quit command for client
                #clientSocket.send("QUIT_REQUEST_FLAG".encode())
                print("goodbye send")
                sys.exit(0)


            elif sentence.lower() == "#a":  #Send attachment command
                clientSocket.send("ATTACHMENT_FLAG".encode())
                sentence = input("Enter filename: ")
                clientSocket.send(sentence.encode())






            elif sentence.lower() != "#q" and sentence.lower() != "#a" and file_path[0] !="ATTACHMENT_FLAG" :   #Otherwise, send normal chat message
                clientSocket.send(sentence.encode())
    except: #Close client socket if necessary
        clientSocket.close()
        sys.exit()




# Function to listen for messages from the server
def listen_chat(client):

        attachment_flag = 0


        while True:
            chat = client.recv(1024).decode()   # Receive messages from server


            if chat == "QUIT_ACCEPT_FLAG":  # Handle quit message from server
                client.close()
                print("goodbye")
                sys.exit(0)

            elif chat == "ATTACHMENT_FLAG = 0":     # Handle file sending
                file_name = client.recv(1024).decode()
                file = open(file_name, 'r')
                data = file.read()
                file.close()
                clientSocket.send(data.encode())

            elif chat == "ATTACHMENT_FLAG= 1":  # Handle file received, save chat to a file
                file_name = client.recv(1024).decode()
                data = client.recv(1024).decode()
                file = open(file_name,'w')
                file.write(data)
                file.close()
                print(f"file contents: {data}")
                #shutil.move('chat.txt', "C:\\Users\\Josh's PC\\Downloads", copy_function=shutil.copytree)


            else:
                print(chat) # Print received chat messages



if __name__ == '__main__':
    serverName = "localhost"
    serverPort = 18006

    # Create a TCP client socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    user_name = ""

    print("Connection Successful.")
    print(clientSocket.recv(1024).decode())
    print("Please Select an Option:")
    print("Option 1: Get Chatroom Report")
    print("Option 2: Join Chatroom")
    print("Option 3: Quit Program")

    while True:
        msg = input("option:")
        if msg == "2":  # Join Chatroom
            print("Option 2 selected")
            clientSocket.send("JOIN_REQUEST_FLAG".encode())
            msg = clientSocket.recv(1024).decode()
            if msg == "JOIN_REQUEST_FLAG = 1":
                flag = 0
                while flag == 0:
                    user_name = input("Choose username: ")
                    clientSocket.send(user_name.encode())
                    if clientSocket.recv(1024).decode() == "JOIN_ACCEPT_FLAG = 1":
                        print(f"user name selected = {user_name}")
                        break


                    else:
                        print("username in use")

            try:
                listen_thread = Thread(target=listen_chat, args=(clientSocket,))
                listen_thread.daemon = True
                listen_thread.start()
                while True:
                    #listen_thread = Thread(target=listen_chat, args=(clientSocket,))
                    #send_thread = Thread(target=send_chat, args=(clientSocket,))
                    #listen_thread.daemon = True
                    #send_thread.daemon = True
                    #listen_thread.start()
                    #send_thread.start()
                    send_chat(clientSocket) # Start sending messages
            except:
                clientSocket.close()
                sys.exit(0)
            else:
                print("Chat room full")
                clientSocket.close()
                exit()

        elif msg == "1":  # Request chatroom report
            print("Option 1 selected")
            clientSocket.send("REPORT_REQUEST_FLAG".encode())
            print(clientSocket.recv(1024).decode())

        elif msg == "3":    # Quit program
            print("option 3 selected")
            clientSocket.send("QUIT_REQUEST_FLAG".encode())
            print("Goodbye")
            break
        else:
            break











# user options
#while True:
 #   sentence = input()
  #  sentence = username + ": " + sentence
  #  curr_time = datetime.now().strftime("[%H:%M:%S] ")
   # sentence = curr_time + sentence
   # clientSocket.send(sentence.encode())





# close clientSocket
    clientSocket.close()
    print("Socket Closed")