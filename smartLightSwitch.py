from stateMachine import *
from triggers import *

def localOff():
    print("This is the LocalOff loop")
def localOn():
    print("This is the LocalOn loop")
def fail():
    print("This is the Fail loop")
def remoteOff():
    print("This is the RemoteOff loop")
def remoteOn():
    print("This is the RemoteOn loop")
def dimUp():
    print("This is the DimUp loop")
def dimDown():
    print("This is the DimDown loop")

# State = State("Name",loopFunction,enterFunction,leaveFunction)
LocalOff = State("LocalOff",None,localOff,None)
LocalOn = State("LocalOn",None,localOn,None)
Fail = State("Fail",None,fail,None)
RemoteOff = State("RemoteOff",None,remoteOff,None)
RemoteOn = State("RemoteOn",None,remoteOn,None)
DimUp = State("DimUp",None,dimUp,None)
DimDown = State("DimDown",None,dimDown,None)

statesList = [
    LocalOff,
    LocalOn,
    Fail,
    RemoteOff,
    RemoteOn,
    DimUp,
    DimDown,
]

# NAME = Transition(
#     triggerFunction
#     [SourceStates]
#     [TargetStates]
# )
LONGHOLD_AND_ONLINE = Transition(
    "Longhold&&Online",
    trig1,
    [LocalOff,LocalOn],
    [RemoteOff,RemoteOn])
LONGHOLD_AND_NOT_ONLINE = Transition(
    "Longhold&&!Online",
    trig2,
    [LocalOff,LocalOn],
    [Fail,Fail])
LONGHOLD_OR_NOT_ONLINE = Transition(
    "Longhold||!Online",
    trig3,
    [RemoteOff,RemoteOn],
    [LocalOff,LocalOn])
PRESS = Transition(
    "Press",
    trig4,
    [LocalOff,LocalOn,RemoteOff,RemoteOn],
    [LocalOn,LocalOff,RemoteOn,RemoteOff])
RELEASE = Transition(
    "Release",
    trig5,
    [DimUp,DimDown],
    [RemoteOn,RemoteOn])
PREVSTATE_LOCALON = Transition(
    "PrevState==LocalOn",
    trig6,
    [Fail],
    [LocalOn])
PREVSTATE_LOCALOFF = Transition(
    "PrevState==LocalOff",
    trig7,
    [Fail],
    [LocalOff])
PREVSTATE_DIMUP_AND_HOLD = Transition(
    "PrevState==DimUp&&Hold",
    trig8,
    [RemoteOn],
    [DimDown])
PREVSTATE_NOT_DIMUP_AND_HOLD = Transition(
    "PrevState!=DimUp&&Hold",
    trig9,
    [RemoteOn],
    [DimUp])
NOT_ONLINE = Transition(
    "!Online",
    trig0,
    [DimUp,DimDown],
    [LocalOn,LocalOn])

transitionsList = [
    LONGHOLD_AND_ONLINE,
    LONGHOLD_AND_NOT_ONLINE,
    LONGHOLD_OR_NOT_ONLINE,
    PRESS,
    RELEASE,
    PREVSTATE_LOCALON,
    PREVSTATE_LOCALOFF,
    PREVSTATE_DIMUP_AND_HOLD,
    PREVSTATE_NOT_DIMUP_AND_HOLD,
    NOT_ONLINE,
]

sm = StateMachine(statesList,transitionsList,"LocalOff")

while True:
    sm.checkTransitions()
    sm.run()
