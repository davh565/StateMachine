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