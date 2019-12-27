class StateMachine:
    # states: dict containing all possible states
    # transistions: dict containing all possible transitions
    # initialstate: str equal to key of starting state
    def __init__(self,states,transitions,initialState):
        self.currentStateName = initialState
        self.states = states
        self.transitions = transitions
    
    def __call__(self):
        self.checkTransitions()
        self.run()
    
    # This method should be called continously in a loop
    def run(self):
        currentState = self.states[self.currentStateName]
        # Run current State's loop function, if it exists
        if callable(currentState.loop): currentState.loop()

    # This method should be called continously in a loop
    def checkTransitions(self):
        for transition in self.transitions:
            currentTransition = self.transitions[transition]
            if currentTransition.checkTrigger() \
            and self.currentStateName == currentTransition.sourceState:
                self.changeState(currentTransition.targetState)

    # call leave function, if any, switch to new State, call enter function, if any
    def changeState(self,newState):
        endingState = self.states[self.currentStateName]
        if callable(endingState.leave): endingState.leave()
        
        self.currentStateName = newState
        
        startingState = self.states[self.currentStateName]
        if callable(startingState.enter): startingState.enter()


class State:
    # name: str name of State
    # loop: func to run continuously while in given state
    # enter: func to run once upon entering state
    # leave: func to run once upon leaving state
    def __init__(self,name,loop=None,enter=None,leave=None):
        self.name = name
        self.loop = loop
        self.enter = enter
        self.leave = leave


class Transition:
    # name: str name of Transition
    # trigger: func to trigger transition. Should return Bool
    # source: str equal to key of source state
    # target: str equal to key of targer state
    def __init__(self, name,trigger,source,target):
        self.name = name
        self.getTrigger = trigger
        self.sourceState = source
        self.targetState = target

    def checkTrigger(self):
        return self.getTrigger()