import socket
import threading
from random import randint
from time import perf_counter
import numpy as np
from math import sqrt, floor, ceil
import io
import pickle
import json

serverPost: str = "null"
length: int = 4
increment: int = 1
s: str = ""
lst: str = ""

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


##=========================================
## TRANSITIONS

class Transition(object):
    def __init__(self, toState):
        self.toState = toState

    def Execute(self):
        print("Transitioning...")


##=========================================
## STATES

class State(object):
    def __init__(self, FSM):
        self.FSM = FSM
        self.timer = 0
        self.startTime = 0

    def Enter(self):
        self.timer = randint(0, 5)
        self.startTime = int(perf_counter())

    def Execute(self):
        pass

    def Exit(self):
        pass


class Idle(State):
    def __init__(self, FSM, name):
        self.name = name
        super(Idle, self).__init__(FSM)

    def Enter(self):
        print(self.name + " is starting to become idle.")
        super(Idle, self).Enter()

    def Execute(self):
        print(self.name + " is idle.")
        if (serverPost == "CollectWood"):
            self.FSM.ToTransition("toCollectWood")
        if (serverPost == "CollectIron"):
            self.FSM.ToTransition("toCollectIron")

    def Exit(self):
        print(self.name + " is no longer idle.")


class CollectWood(State):
    def __init__(self, FSM, name):
        self.name = name
        super(CollectWood, self).__init__(FSM)

    def Enter(self):
        print(self.name + " has found some wood.")
        super(CollectWood, self).Enter()

    def Execute(self):
        print(self.name + " is carrying the wood to the lumbermill.")
        self.FSM.ToTransition("toLumbermill")

    def Exit(self):
        print(self.name + " Dropped off the wood at the lumbermill.")


class CollectIron(State):
    def __init__(self, FSM, name):
        self.name = name
        super(CollectIron, self).__init__(FSM)

    def Enter(self):
        print(self.name + " has found some iron.")
        super(CollectIron, self).Enter()

    def Execute(self):
        print(self.name + " is carrying the iron to the blacksmith.")
        self.FSM.ToTransition("toBlacksmith")

    def Exit(self):
        print(self.name + " Dropped off the iron at the blacksmith.")


class Lumbermill(State):
    def __init__(self, FSM, name):
        self.name = name
        super(Lumbermill, self).__init__(FSM)

    def Enter(self):
        print("Lumbermill has received wood from " + self.name + " and is starting to process it")
        super(Lumbermill, self).Enter()

    def Execute(self):
        print("Lumbermill is processing the wood.")
        self.FSM.ToTransition("toIdle")

    def Exit(self):
        print("Lumbermill has finished processing the wood.")


class Blacksmith(State):
    def __init__(self, FSM, name):
        self.name = name
        super(Blacksmith, self).__init__(FSM)

    def Enter(self):
        print("Blacksmith has received iron from " + self.name + " and is starting to process it")
        super(Blacksmith, self).Enter()

    def Execute(self):
        print("Lumbermill is processing the iron.")
        self.FSM.ToTransition("toIdle")

    def Exit(self):
        print("Lumbermill has finished processing the iron.")


##=========================================
## FINITE STATE MACHINES

class FSM(object):
    def __init__(self, character, name):
        self.name = name
        self.char = character
        self.states = {}
        self.transitions = {}
        self.curState = None
        self.prevState = None
        self.trans = None
        # print(1)

    def AddTransition(self, transName, transition):
        self.transitions[transName] = transition
        # print(2)

    def AddState(self, stateName, state):
        self.states[stateName] = state
        # print(3)

    def SetState(self, stateName):
        self.prevState = self.curState
        self.curState = self.states[stateName]
        # print(4)

    def ToTransition(self, toTrans):
        self.trans = self.transitions[toTrans]
        # print(5)

    def Execute(self):
        # print(6)
        global increment
        global length
        if (self.trans):
            self.curState.Exit()
            self.trans.Execute()
            # print(1)
            self.SetState(self.trans.toState)
            # print(2)
            self.curState.Enter()
            self.trans = None
            increment += 1
        if (increment < length):
            self.curState.Execute()
        if (increment == length):
            increment = 1
            self.SetState("Idle")


##=========================================
## IMPLEMENTATION

Char = type("Char", (object,), {"day": 0})


class RobotMaid(Char):
    def __init__(self, name):
        self.name = name
        self.FSM = FSM(self, name)

        ## TRANSITIONS
        self.FSM.AddTransition("toIdle", Transition("Idle"))
        self.FSM.AddTransition("toLumbermill", Transition("Lumbermill"))
        self.FSM.AddTransition("toBlacksmith", Transition("Blacksmith"))
        self.FSM.AddTransition("toCollectWood", Transition("CollectWood"))
        self.FSM.AddTransition("toCollectIron", Transition("CollectIron"))

        ## STATES
        self.FSM.AddState("Idle", Idle(self.FSM, name))
        self.FSM.AddState("CollectWood", CollectWood(self.FSM, name))
        self.FSM.AddState("CollectIron", CollectIron(self.FSM, name))
        self.FSM.AddState("Lumbermill", Lumbermill(self.FSM, name))
        self.FSM.AddState("Blacksmith", Blacksmith(self.FSM, name))

        self.FSM.SetState("Idle")

    def Execute(self):
        self.FSM.Execute()


if __name__ == '__main__':
    r = RobotMaid("Claus")
    # s = RobotMaid("Hendrik")
    # t = RobotMaid("Rob")
    # u = RobotMaid("Charlie")
    # v = RobotMaid("Roger")


def ServerPost(data):
    serverPost = data

    return serverPost


def index_2d(data, search):
    for i, e in enumerate(data):
        try:
            return i, e.index(search)
        except ValueError:
            pass
    raise ValueError("{} is not in list".format(repr(search)))

    # Function to string into grid form
    # def gridStr(string):
    # l = len(string)
    # k = 0
    # global s
    #
    # row = floor(sqrt(l))
    # column = ceil(sqrt(l))
    #
    # if (row * column < l):
    #     row = column
    #
    # s = [[0 for j in range(column)]
    #      for i in range(row)]
    #
    # # convert the string into grid
    # for i in range(row):
    #     for j in range(column):
    #
    #         if k >= l:
    #             s[i][j] = " "
    #             k += 1
    #
    #         else:
    #             s[i][j] = string[k]
    #             k += 1
    #
    # # Printing the grid
    # for i in range(row):
    #     for j in range(column):
    #         if s[i][j] == " ":
    #             break
    #
    #         print(s[i][j], end="")
    #
    #     print()



# def method(string):
#     column = 9
#     row = 9
#     increment = 0
#     tempArray = [[0 for j in range(column)]
#                  for i in range(row)]
#
#     for i in range(row):
#         for j in range(column):
#             tempArray[i][j] = string[increment]
#             increment += 1
#
#     return tempArray

# def make2DArray(string):
#     y = 0
#     x = 0
#     string[,] newArray = string[8,8]
#
#     for elem in s:
#         newArray[x,y] = elem;
#         x++;
#         if(x % 8)
#             y++;


def handle_client(client_socket):
    global serverPost
    global length

    while True:

        try:
            data = client_socket.recv(4096)

            if not data: break

            if data.decode("utf-8") == "CollectWood":
                print("client received: " + data.decode("utf-8") + " from server.")
                serverPost = data.decode("utf-8")
                for i in range(length):
                    startTime = perf_counter()
                    timeInterval = 1
                    while (startTime + timeInterval > perf_counter()):
                        pass
                    r.Execute()
                    if (i > length - 2):
                        serverPost = ""
                        print("String is " + serverPost + "EMPTY!")

                # client_socket.send(stringDataPos.encode("utf-8"))

            if data.decode("utf-8") == "CollectIron":
                print("client received: " + data.decode("utf-8") + " from server.")
                serverPost = data.decode("utf-8")
                for i in range(length):
                    startTime = perf_counter()
                    timeInterval = 1
                    while (startTime + timeInterval > perf_counter()):
                        pass
                    r.Execute()
                    if (i > length - 2):
                        serverPost = ""
                        print("String is " + serverPost + "EMPTY!")

            if data.decode("utf-8") != "":
                msgReceived = data.decode("utf-8")

                # gridStr(msgReceived)
                function(msgReceived, 9)
                # print(lst[0][0])
                # position = index_2d(s, "y")
                # print(position)
                # indices = [i for i, x in enumerate(s) if x == "y"]
                # print(indices)
                # value = "y"
                # result = [(index, row.index(value)) for index, row in enumerate(s) if value in row]
                # print(result)

                # temArray = method(msgReceived)
                # print(temArray)

                # a = np.array(lst)
                # print(a)
                # print(a[2][0])
                # b = np.where(a == "y")
                # print(b)

                # Def
                # make2DArray(string
                # s):
                #
                # int
                # y = 0;
                # int
                # x = 0;
                # string[,] newArray = string[8, 8]
                #
                # for elem in s:
                #     newArray[x, y] = elem;
                #     x + +;
                #     if (x % 8)
                #         y + +;

            # Function to string into grid form
            def function(str, k):
                global lst
                for i in range(len(str)):
                    if i % k == 0:
                        sub = str[i:i + k]
                        print(sub)
                        lst = []
                        for j in sub:
                            lst.append(j)
                    print(' '.join(lst))

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
