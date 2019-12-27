from stateMachine import *

LocalOff = State("LocalOff")
LocalOn = State("LocalOn")
Fail = State("Fail")
RemoteOff = State("RemoteOff")
RemoteOn = State("RemoteOn")
DimUp = State("DimUp")
DimDown = State("DimDown")
statesDict = {}

LONGHOLD_AND_ONLINE = Transition("Longhold&&Online",
None,
[LocalOff,LocalOn],
[RemoteOff,RemoteOn])
LONGHOLD_AND_NOT_ONLINE = Transition("Longhold&&!Online",
None,
[LocalOff,LocalOn],
[Fail,Fail])
LONGHOLD_OR_NOT_ONLINE = Transition("Longhold||!Online",
None,
[RemoteOff,RemoteOn],
[LocalOff,LocalOn])
PRESS = Transition("Press",
None,
[LocalOff,LocalOn,RemoteOff,RemoteOn],
[LocalOn,LocalOff,RemoteOn,RemoteOff])
RELEASE = Transition("Release",
None,
[DimUp,DimDown],
[RemoteOn,RemoteOn])
PREVSTATE_LOCALON = Transition("PrevState==LocalOn",
None,
[Fail],
[LocalOn])
PREVSTATE_LOCALOFF = Transition("PrevState==LocalOff",
None,
[Fail],
[LocalOff])
PREVSTATE_DIMUP_AND_HOLD = Transition("PrevState==DimUp&&Hold",
None,
[RemoteOn],
[DimDown])
PREVSTATE_NOT_DIMUP_AND_HOLD = Transition("PrevState!=DimUp&&Hold",
None,
[RemoteOn],
[DimUp])
NOT_ONLINE = Transition("!Online",
None,
[DimUp,DimDown],
[LocalOn,LocalOn])
transitionsDict = {}

sm = StateMachine(statesDict,transitionsDict,"LocalOff")
