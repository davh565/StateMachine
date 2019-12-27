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
    # checks if each transition's trigger is true. If so, checks if current
    # state is in list of source states. if so, change state to corresponding
    # target state
    def checkTransitions(self):
        for transition in self.transitions:
            currentTransition = self.transitions[transition]
            if currentTransition.checkTrigger():
                if self.currentStateName in currentTransition.sourceStates:
                    index = currentTransition.sourceStates(self.currentStateName)
                    self.changeState(currentTransition.targetStates[index])
            # if currentTransition.checkTrigger() \
            # and self.currentStateName == currentTransition.sourceState:
            #     self.changeState(currentTransition.targetState)

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
    # sources: list of str equal to key of source states
    # targets: list of str equal to key of target states
    # sources and targets should be lists of equal size. elements that share an
    # index represent a source-destination pair
    def __init__(self, name,trigger,sources,targets):
        self.name = name
        self.getTrigger = trigger
        self.sourceStates = sources
        self.targetStates = targets

    def checkTrigger(self):
        return self.getTrigger()