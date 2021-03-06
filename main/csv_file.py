__author__ = 'eric'
import re
import os
from sequence import *
from channel_set import *

class CSVFile:

    def __init__(self, filepath, controller):
        self.error = ""
        self.controller = controller

        try:
            file = open(filepath, 'r')
        except:
            raise Exception("File could not be opened")

        self.file = file
        self.name = os.path.splitext(os.path.basename(filepath))[0]

        self.sequence = Sequence(self.name)
        self.parse()

        file.close()

    def parse(self):
        for line in self.file:
            cols = re.split(",", line)
            if len(cols) < 5:
                raise Exception("File format invalid")


            number = int(cols[0])
            label = cols[1]
            fade = float(cols[2])
            wait = float(cols[3])

            channel = 0
            stepState = ChannelState(self.controller)
            for i in range(4, len(cols)):
                try:
                    value = int(cols[i])
                except:
                    value = 0
                channel += 1
                stepState.channel_at(channel, value)

            step = SequenceStep(number, label, stepState, fade, wait)
            self.sequence.append_step(step)
