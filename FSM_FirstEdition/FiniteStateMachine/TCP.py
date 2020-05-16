import socket
import threading
import pickle
import json

# this is the ip we are connecting to
bind_ip = "127.0.0.1"
# this is the port we are connecting to
bind_port = 54000

# This listens on the ip address and when ever a connection comes in it's going to accept
# the connection
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(5)

# prints that we are listening on the aforementioned ip and port
print("[+] listening on %s:%d" % (bind_ip, bind_port))


def handle_client(client_socket):

    while True:

            try:
                data = client_socket.recv(4096)

                if not data: break

                if data.decode("utf-8") == "TOWER":
                    print("client says: " + data.decode("utf-8"))

                # if data.decode("utf-8") == "GRID":
                #     print("client says:" + data.decode("utf-8"))
                #     gridPos = cvObjectOne.OpenCV.detectGrid(cvObjectOne.OpenCV.testImgP1t1)
                #     print(gridPos)
                #     gridPosStr = str(gridPos)
                #     client_socket.send(gridPosStr.encode("utf-8"))

            except socket.error:
                print("Error Occured.")
                break

    client_socket.close()


while True:

        client, addr = server.accept()
        print("[+] Accepting connection from: %s:%d" % (addr[0], addr[1]))
        print("[+] Establishing a connection from %s:%d" % (addr[0], addr[1]))

        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()