from random import randint
from time import perf_counter

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
        self.timer = randint(0,5)
        self.startTime = int(perf_counter())
    def Execute(self):
        pass
    def Exit(self):
        pass

class Idle(State):
    def __init__(self, FSM, name):
        self.name = name
        super(Idle,self).__init__(FSM)

    def Enter(self):
        print(self.name + " is starting to become idle.")
        super(Idle, self).Enter()

    def Execute(self):
        print(self.name + " is idle.")
        self.FSM.ToTransition("toCollectWood")

    def Exit(self):
        print(self.name + " is no longer idle.")

class CollectWood(State):
    def __init__(self, FSM, name):
        self.name = name
        super(CollectWood,self).__init__(FSM)

    def Enter(self):
        print(self.name + " has found some wood.")
        super(CollectWood, self).Enter()

    def Execute(self):
        print(self.name + " is carrying the wood to the lumbermill.")
        self.FSM.ToTransition("toLumbermill")

    def Exit(self):
        print(self.name + " Dropped off the wood at the lumbermill.")

class Lumbermill(State):
    def __init__(self, FSM, name):
        self.name = name
        super(Lumbermill,self).__init__(FSM)

    def Enter(self):
        print("Lumbermill has received wood from " + self.name + " and is starting to process it")
        super(Lumbermill, self).Enter()

    def Execute(self):
        print("Lumbermill is processing the wood.")
        self.FSM.ToTransition("toIdle")

    def Exit(self):
        print("Lumbermill has finished processing the wood.")


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
        #print(1)

    def AddTransition(self, transName, transition):
        self.transitions[transName] = transition
        #print(2)

    def AddState(self, stateName, state):
        self.states[stateName] = state
        #print(3)

    def SetState(self, stateName):
        self.prevState = self.curState
        self.curState = self.states[stateName]
        #print(4)

    def ToTransition(self, toTrans):
        self.trans = self.transitions[toTrans]
        #print(5)

    def Execute(self):
        #print(6)
        if(self.trans):
            self.curState.Exit()
            self.trans.Execute()
            self.SetState(self.trans.toState)
            self.curState.Enter()
            self.trans = None
        self.curState.Execute()


##=========================================
## IMPLEMENTATION

Char = type("Char", (object,), {"day":0})

class RobotMaid(Char):
    def __init__(self, name):
        self.name = name
        self.FSM = FSM(self, name)

        ## TRANSITIONS
        self.FSM.AddTransition("toIdle", Transition("Idle"))
        self.FSM.AddTransition("toLumbermill", Transition("Lumbermill"))
        self.FSM.AddTransition("toCollectWood", Transition("CollectWood"))

        ## STATES
        self.FSM.AddState("Idle", Idle(self.FSM, name))
        self.FSM.AddState("CollectWood", CollectWood(self.FSM, name))
        self.FSM.AddState("Lumbermill", Lumbermill(self.FSM, name))

        self.FSM.SetState("Idle")

    def Execute(self):
        self.FSM.Execute()


if __name__ == '__main__':
    r = RobotMaid("Claus")
    #s = RobotMaid("Hendrik")
    #t = RobotMaid("Rob")
    #u = RobotMaid("Charlie")
    #v = RobotMaid("Roger")




    # for i in range(5):
    #     startTime = perf_counter()
    #     timeInterval = 1
    #     while (startTime + timeInterval > perf_counter()):
    #         pass
    #     r.Execute()
    #     s.Execute()
    #     t.Execute()
    #     u.Execute()
    #     v.Execute()