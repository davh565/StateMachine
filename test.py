from stateMachine import *
from machine import Pin, Timer

class ButtonEvents:

    isPressed = False
    isReleased = True

    isHeld = False
    isLongHeld = False
    isToggled = False

    def getToggled(self): return self.isToggled
    def getNotToggled(self): return not self.isToggled
    def getHeld(self): return self.isHeld
    def getLongHeld(self): return self.isLongHeld
    def getReleased(self): return self.isReleased

    def onEdge(self,timer):
        # print("test")

        val = button.value()
        if val == 0 :
            self.isPressed = True
            self.isReleased = not self.isPressed
            timerHold.init(mode=Timer.ONE_SHOT, period=2000, callback=btn.onHold)
            timerLongHold.init(mode=Timer.ONE_SHOT, period=10000, callback=btn.onLongHold)
        else : 
            self.isPressed = False
            self.isReleased = not self.isPressed
            if not (self.isHeld or self.isLongHeld):
                self.onToggle()
            self.isHeld = False
            self.isLongHeld = False
            
            self.acknowledgeHold = False
            self.acknowledgeLongHold = False
            timerHold.deinit()
            timerLongHold.deinit()
        # print(self.isToggled)


    def onHold(self, timer):
        self.isHeld = True
        self.acknowledgeHold = False

    def onLongHold(self, timer):
        self.isHeld = False
        self.isLongHeld = True
        self.acknowledgeLongHold = False

    def onToggle(self):
        self.isToggled = not self.isToggled

def debounce(pin):
    timerDebounce.init(mode=Timer.ONE_SHOT, period=20, callback=btn.onEdge)



###################################
# Register a new hardware timer.
timerDebounce = Timer(0)
timerHold = Timer(1)
timerLongHold = Timer(2)

# Setup the button input pin with a pull-up resistor.
button = Pin(0, Pin.IN, Pin.PULL_UP)
ledR = Pin(2, Pin.OUT)
ledG = Pin(4, Pin.OUT)
ledB = Pin(5, Pin.OUT)

#
btn = ButtonEvents()
# Register an interrupt on rising button input.
button.irq(debounce, Pin.IRQ_RISING or Pin.IRQ_FALLING)


################################
################ States
def relayOnLoop():
    print("This is the relay on loop")
def relayOnEnter():
    print("This is the relay on State")

def relayOffLoop():
    print("This is the relay off loop")
def relayOffEnter():
    print("This is the relay off State")

def ConnectOnLoop():
    print("This is the connect on loop")
def ConnectOnEnter():
    print("This is the connect on State")

def ConnectOffLoop():
    print("This is the connect off loop")
def ConnectOffEnter():
    print("This is the connect off State")

def mQTTOnLoop():
    print("This is the MQTT on loop")
def mQTTOnEnter():
    print("This is the MQTT on State")

def mQTTOffLoop():
    print("This is the MQTT off loop")
def mQTTOffEnter():
    print("This is the MQTT off State")

def dimLoop():
    print("This is the dim loop")
def dimEnter():
    print("This is the dim State")

RelayOff = State("Relay Off",loop=relayOffLoop,enter=relayOffEnter)
RelayOn = State("Relay On",loop=relayOnLoop,enter=relayOnEnter)
ConnectOff = State("Connecting Off",loop=ConnectOffLoop,enter=ConnectOffEnter)
ConnectOn = State("Connecting On",loop=ConnectOnLoop,enter=ConnectOnEnter)
mQTTOff = State("MQTT Off",loop=mQTTOffLoop,enter=mQTTOffEnter)
mQTTOn = State("MQTT On",loop=mQTTOnLoop,enter=mQTTOnEnter)
Dim = State("Dim",loop=dimLoop,enter=dimEnter)

statesDict = {
    "Relay Off" : RelayOff,
    "Relay On" : RelayOn,
    "Connecting Off" : ConnectOff,
    "Connecting On" : ConnectOn,
    "MQTT Off" : mQTTOff,
    "MQTT On" : mQTTOn,
    "Dim" : Dim
    }

################ TRANSITIONS

# TransitionName = Transition("Name",triggerFunc{returns bool},"SourceState","TargetState")
relayOff_relayOn = Transition("Relay Toggle On",btn.getToggled,"Relay Off","Relay On")
relayOn_relayOff = Transition("Relay Toggle Off",btn.getToggled,"Relay On","Relay Off")
relayOn_connectOn = Transition("Relay LongHold",btn.getToggled,"Relay On","Connecting On")
mQTTOn_relayOn = Transition("MQTT LongHold",btn.getToggled,"MQTT On","Relay On")
connectOn_relayOn = Transition("Connect On Fail",btn.getToggled,"Connecting On","Relay On")
connectOn_mQTTOn = Transition("Connect On Success",btn.getToggled,"Connecting On","MQTT On")
mQTTOn_connectOn = Transition("MQTT On Drop",btn.getToggled,"MQTT On","Connecting On")
mQTTOff_mQTTOn = Transition("MQTT Toggle On",btn.getToggled,"MQTT Off","MQTT On")
mQTTOn_mQTTOff = Transition("MQTT Toggle Off",btn.getToggled,"MQTT On","MQTT Off")
connectOff_relayOff = Transition("Connect Off Fail",btn.getToggled,"Connecting Off","Relay Off")
connectOff_mQTTOff = Transition("Connect Off Success",btn.getToggled,"Connecting Off","MQTT Off")
mQTTOff_connectOff = Transition("MQTT Off Drop",btn.getToggled,"MQTT Off","Connecting Off")
mQTTOn_dim = Transition("MQTT Hold",btn.getToggled,"MQTT On","Dim")
dim_mQTTOn = Transition("Dim Release",btn.getToggled,"Dim","MQTT On")
dim_connectOn = Transition("Dim Drop",btn.getToggled,"Dim","Connecting On")

transitionsDict = {
    "Relay Toggle On" : relayOff_relayOn,
    "Relay Toggle Off" : relayOn_relayOff,
    "Relay LongHold" : relayOn_connectOn,
    "MQTT LongHold" : mQTTOn_relayOn,
    "Connect On Fail" : connectOn_relayOn,
    "Connect On Success" : connectOn_mQTTOn,
    "MQTT On Drop" : mQTTOn_connectOn,
    "MQTT Toggle On" : mQTTOff_mQTTOn,
    "MQTT Toggle Off" : mQTTOn_mQTTOff,
    "Connect Off Fail" : connectOff_relayOff,
    "Connect Off Success" : connectOff_mQTTOff,
    "MQTT Off Drop" : mQTTOff_connectOff,
    "MQTT Hold" : mQTTOn_dim,
    "Dim Release" : dim_mQTTOn,
    "Dim Drop" : dim_connectOn,
    }
    gi

################ STATE MACHINE
sm = StateMachine(statesDict,transitionsDict,"Relay Off")


while True:
    sm.checkTransitions()
    # smDevice.run()


