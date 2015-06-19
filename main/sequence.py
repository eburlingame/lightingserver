from channel_set import ChannelState

__author__ = 'eric'

class SequenceRunner:

    def __init__(self, controller, id, sequence, channelSet = None, percent = 100, fade = -1, wait = -1, step = 0):
        self.controller = controller
        self.patch = controller.patch

        self.id = id
        self.sequence = sequence
        self.channelSet = channelSet
        self.percent = percent
        self.fade = fade
        self.wait = wait

        self.currentStep = step
        self.paused = False
        self.elapsed = 0

        self.advance_step()


    # Takes the difference in time since last update in seconds
    def update(self, diff):
        if not self.paused:
            self.elapsed += diff
            total = self.get_fade() + self.get_wait()

            if self.elapsed > total:
                self.advance_step()

    def advance_step(self):
        toSet = None
        step = self.sequence.steps[self.currentStep]
        # Apply the channel set to the saved sequence step, if supplied
        if self.channelSet == None:
            toSet = step.get_channel_state(self.controller, self.percent)
        else:
            toSet = step.get_custom_channel_state(self.controller, self.percent, self.channelSet)

        self.patch.set_channel_state(toSet, self.get_fade())
        self.currentStep += 1

    def get_fade(self):
        if self.fade != -1:
            return self.fade
        return self.sequence.get_step(self.currentStep).fade

    def get_wait(self):
        if self.wait != -1:
            return self.wait
        return self.sequence.get_step(self.currentStep).wait

class Sequence:

    def __init__(self, name):
        self.name = name
        self.steps = []

    def append_step(self, sequenceStep):
        self.steps.append(sequenceStep)
        self.reindex_steps()

    def insert_step(self, sequenceStep, stepNumber):
        self.steps.insert(stepNumber, sequenceStep)
        self.reindex_steps()

    def delete_step(self, stepNumber):
        i = 0
        for step in self.steps:
            if i == stepNumber:
                self.steps.remove(step)
                return
            i += 1
        self.reindex_steps()

    def reindex_steps(self):
        i = 0
        for step in self.steps:
            step.number = i
            i += 1

    def get_step(self, number):
        return self.steps[number]

class SequenceStep:
    def __init__(self, number, label, channelState, fade = -1, wait = -1):
        self.channelState = channelState
        self.fade = fade
        self.wait = wait
        self.number = number
        self.label = label

    def toString(self):
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