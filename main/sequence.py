from channel_set import ChannelState

__author__ = 'Eric Burlingame'

class SequenceRunner:

    def __init__(self, controller, id, sequence, channelSet = None, percent = 100,
                 cued = False, fade = -1, wait = -1, step = 0, repeat = True):
        self.controller = controller
        self.patch = controller.patch

        self.id = id
        self.sequence = sequence
        self.channelSet = channelSet
        self.percent = percent
        self.cued = cued
        self.fade = fade
        self.wait = wait
        self.repeat = repeat
        self.done = False

        self.currentStep = step
        self.paused = False
        self.elapsed = 0
        self.elapsedTotal = self.get_fade() + self.get_wait()

        self.advance()


    # Takes the difference in time since last update in seconds
    def update(self, diff):
        if not self.paused:
            self.elapsed += diff

            if self.cued == False:
                if self.elapsed >= self.elapsedTotal:
                    self.advance()

    def advance(self):
        if self.done:
            return
        toSet = None
        # Fade up this step
        self.fade_step()
        self.currentStep += 1
        self.elapsed = 0
        if self.currentStep >= len(self.sequence.steps):
            if self.repeat:
                self.currentStep = 0
            else:
                self.done = True

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False

    def fade_step(self):
        step = self.sequence.steps[self.currentStep]
        # Apply the channel set to the saved sequence step, if supplied
        if self.channelSet == None:
            toSet = step.get_channel_state(self.controller, self.percent)
        else:
            toSet = step.get_custom_channel_state(self.controller, self.percent, self.channelSet)
        # print "Setting step %s" % self.currentStep
        # print "Setting step %s fade %s " % (self.currentStep, self.get_fade())
        self.patch.set_channel_state(toSet, self.get_fade())
        # Set the total elapsed so we will wait the correct amount for this step
        self.elapsedTotal = self.get_fade() + self.get_wait()

    def get_fade(self):
        ourFade = self.fade
        stepFade = self.sequence.get_step(self.currentStep).fade
        default = self.controller.defaultFade
        if ourFade != -1:
            return ourFade
        elif stepFade != -1:
            return stepFade
        else:
            return default

    def get_wait(self):
        ourWait = self.wait
        stepWait = self.sequence.get_step(self.currentStep).wait
        default = self.controller.defaultWait
        if ourWait != -1:
            return ourWait
        elif stepWait != -1:
            return stepWait
        else:
            return default

    def to_string(self):
        str = "Sequence %s (Running id %s) " % (self.sequence.name, self.id)
        if self.percent != 100:
            str += "Percent: %s %\t\t" % self.percent
        if self.cued != False:
            str += "Manually Cued\t\t"
        if self.fade != None:
            str += "Fade: %s\t\t" % self.fade
        if self.wait != None:
            str += "Wait: %s\t\t" % self.wait
        if self.repeat != True:
            str += "Not repeating\t\t"
        if self.channelSet != None:
            str += "Channels: %s\t\t" % self.channelSet.to_string()
        return str

class Sequence:

    def __init__(self, name, repeat):
        self.name = name
        self.repeat = repeat
        self.steps = []

    def append_step(self, sequenceStep):
        self.steps.append(sequenceStep)
        self.reindex_steps()

    def insert_step(self, sequenceStep, stepNumber):
        self.steps.insert(stepNumber, sequenceStep)
        self.reindex_steps()

    def replace_step(self, sequenceStep, stepNumber):
        self.delete_step(stepNumber)
        self.insert_step(sequenceStep, stepNumber)
        self.reindex_steps()

    def delete_step(self, stepNumber):
        i = 0
        for step in self.steps:
            if i == stepNumber:
                self.steps.remove(step)
                return i
            i += 1
        self.reindex_steps()
        return -1

    def reindex_steps(self):
        i = 0
        for step in self.steps:
            step.number = i
            i += 1

    def get_step(self, number):
        return self.steps[number]

    def to_string_short(self):
        return "Sequence %s with %s steps" % (self.name, len(self.steps))

    def to_string(self):
        str = "Sequence %s \n" % self.name
        str += "\t %s Steps:" % len(self.steps)
        for step in self.steps:
            str += "\n\t\t\t" + step.to_string()
        return str

    def to_command(self):
        str = ""
        for step in self.steps:
            str += step.to_command(self)
        return str


class SequenceStep:
    def __init__(self, number, label, channelState, fade = -1, wait = -1):
        self.channelState = channelState
        self.fade = fade
        self.wait = wait
        self.number = number
        self.label = label

    def to_string(self):
        str = "Step #" + self.number + ": \n"
        str += "\t Fade: %s" % self.fade
        str += "\t Wait: %s" % self.wait
        for state in self.channelState.states:
            str += "\n\t\tChannel %s at %s" % (state["number"], state["value"])
        return str

    def get_channel_state(self, controller, percent):
        values = self.channelState.get_sorted_pairs()
        newState = ChannelState(controller)
        ratio = (percent / 100.0)
        for value in values:
            newState.channel_at(value["number"], value["value"] * ratio)

        return newState

    def get_custom_channel_state(self, controller, percent, channelSet):
        set = channelSet.set
        values = self.channelState.get_sorted_pairs()
        newState = ChannelState(controller)
        ratio = (percent / 100.0)
        i = 0
        for channel in set:
            newState.channel_at(channel, values[i]["value"] * ratio)
            i = (i + 1) % len(values)

        return newState

    def to_string(self):
        return "Step %s (Fade: %s, Wait: %s): %s" % (self.number, self.fade, self.wait, self.channelState.to_string())

    def to_command(self, sequence):
        str = "save sequence %s "
        if self.fade != -1:
            str += "fade %s " % self.fade
        if self.wait != -1:
            str += "wait %s " % self.wait

        str += "{ %s } " % self.channelState.to_string()
        return str

