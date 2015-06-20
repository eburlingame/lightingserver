__author__ = 'Eric Burlingame'

class Channel:

    # Takes the time difference in seconds
    def update(self, diff):
        self.fade.update(diff)
        self.value = self.fade.value

    def fadeTo(self, newValue, fadeTime):
        self.fade.start(newValue, fadeTime)

    def __init__(self, number, dmxAddr, label, fixture):
        if number < 0:
            raise Exception("Channel number must be positive")
        if dmxAddr > 512 or dmxAddr < 1:
            raise Exception("DMX number must be between 1 and 512")

        self.label = label # Name or label of the channel
        self.number = number # Channel's number
        self.dmxAddr = dmxAddr # Cchannel's mapped dmx adress
        self.fixture = fixture # Optional fixture field

        self.value = 0
        self.fade = Fade(self.value)

class Fade:

    # Starts a new fade, resetting the target value
    def start(self, newValue, time):
        self._startValue = self.value
        self._time = time
        if newValue > 100:
            newValue = 100
        elif newValue < 0:
            newValue = 0
        self._targetValue = newValue

    # Updates the current running fade
    # Takes the time difference in seconds
    def update(self, diff):
        if self._time == 0:
            self.value = self._targetValue

        # Run the fade only if it has not past the target value
        elif self._startValue > self._targetValue: # Fading down

            if self.value > self._targetValue:
                self.eval_fade(diff)
            else:
                self.value = self._targetValue

        elif self._startValue < self._targetValue: # Fading up

            if self.value < self._targetValue:
                self.eval_fade(diff)
            else:
                self.value = self._targetValue

    def eval_fade(self, diff):
        # Calculate gradient
        self.value += (self._targetValue - self._startValue) * diff / self._time
        # Filter for overflow
        if self.value > 100:
            self.value = 100
        elif self.value < 0:
            self.value = 0



    # Takes an inital value
    def __init__(self, value):
        self.value = value
        self._startValue = 0
        self._targetValue = 0
        self._time = 0