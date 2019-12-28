import keyboard as kb
from time import sleep
from smartLightSwitch import sm

def trig1():
    if kb.is_pressed('1'):
        sleep(0.25)
        return True
def trig2():
    if kb.is_pressed('2'):
        sleep(0.25)
        return True
def trig3():
    if kb.is_pressed('3'):
        sleep(0.25)
        return True
def trig4():
    if kb.is_pressed('4'):
        sleep(0.25)
        return True
def trig5():
    if kb.is_pressed('5'):
        sleep(0.25)
        return True
def trig6():
    if kb.is_pressed('6'):
        sleep(0.25)
        return True
def trig7():
    if kb.is_pressed('7'):
        sleep(0.25)
        return True
def trig8():
    if kb.is_pressed('8'):
        sleep(0.25)
        return True
def trig9():
    if kb.is_pressed('9'):
        sleep(0.25)
        return True
def trig0():
    if kb.is_pressed('0'):
        sleep(0.25)
        return True


def isPressed():
    return kb.is_pressed('0')
def isHeld():
    return True
def isLongHeld():
    return True
def isOnline():
    return True
def prevStateIsLocalOff():
    if sm.oldStateName == "LocalOff":
        return True
    else:
        return False
def prevStateIsLocalOn():
    if sm.oldStateName == "LocalOn":
        return True
    else:
        return False
def prevStateDimUp():
    if sm.oldStateName == "DimUp":
        return True
    else:
        return False
def isReleased():
    return not kb.is_pressed('0')
