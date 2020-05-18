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

class CleanDishes(State):
    def __init__(self, FSM, name):
        self.name = name
        super(CleanDishes,self).__init__(FSM)

    def Enter(self):
        print(self.name + " is preparing to clean dishes.")
        super(CleanDishes, self).Enter()

    def Execute(self):
        print(self.name + " is cleaning dishes.")
        if(self.startTime + self.timer <= perf_counter()):
            if not(randint(1,3) %2):
                self.FSM.ToTransition("toVacuum")
            else:
                self.FSM.ToTransition("toSleep")

    def Exit(self):
        print(self.name + " is finishing cleaning dishes.")

class Vacuum(State):
    def __init__(self, FSM, name):
        self.name = name
        super(Vacuum,self).__init__(FSM)

    def Enter(self):
        print(self.name + " is starting to Vacuum.")
        super(Vacuum, self).Enter()

    def Execute(self):
        print(self.name + " is vacuuming.")
        if(self.startTime + self.timer <= perf_counter()):
            if not(randint(1,3) %2):
                self.FSM.ToTransition("toSleep")
            else:
                self.FSM.ToTransition("toCleanDishes")

    def Exit(self):
        print(self.name + " finished Vacuuming.")

class Sleep(State):
    def __init__(self, FSM, name):
        self.name = name
        super(Sleep,self).__init__(FSM)

    def Enter(self):
        print(self.name + " is starting to Sleep.")
        super(Sleep, self).Enter()

    def Execute(self):
        print(self.name + " is sleeping.")
        if(self.startTime + self.timer <= perf_counter()):
            if not(randint(1,3) %2):
                self.FSM.ToTransition("toVacuum")
            else:
                self.FSM.ToTransition("toCleanDishes")

    def Exit(self):
        print(self.name + " is waking up from Sleep.")


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
        self.FSM.AddTransition("toSleep", Transition("Sleep"))
        self.FSM.AddTransition("toVacuum", Transition("Vacuum"))
        self.FSM.AddTransition("toCleanDishes", Transition("CleanDishes"))

        ## STATES
        self.FSM.AddState("Sleep", Sleep(self.FSM, name))
        self.FSM.AddState("CleanDishes", CleanDishes(self.FSM, name))
        self.FSM.AddState("Vacuum", Vacuum(self.FSM, name))

        self.FSM.SetState("Sleep")

    def Execute(self):
        self.FSM.Execute()


if __name__ == '__main__':
    r = RobotMaid("Claus")
    s = RobotMaid("Hendrik")
    t = RobotMaid("Rob")
    u = RobotMaid("Charlie")
    v = RobotMaid("Roger")
    for i in range(10):
        startTime = perf_counter()
        timeInterval = 1
        while (startTime + timeInterval > perf_counter()):
            pass
        r.Execute()
        s.Execute()
        t.Execute()
        u.Execute()
        v.Execute()