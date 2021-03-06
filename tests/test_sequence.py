__author__ = 'Eric Burlingame'

from unittest import TestCase

from main.sequence import *
from main.controller import Controller
from main.channel_set import *

class SequenceTest(TestCase):

    def test_sequence_step(self):
        controller = Controller()
        state = ChannelState(controller)
        step = SequenceStep(0, "Test", state, 1, 2) # number, label, channelState, fade = -1, wait = -1

        self.assertEquals(0, step.number)
        self.assertEquals("Test", step.label)
        self.assertEquals(state, step.channelState)
        self.assertEquals(1, step.fade)
        self.assertEquals(2, step.wait)

        step1 = SequenceStep(0, "Step 1", state, 1, 2)
        step2 = SequenceStep(1, "Step 2", state, 1, 2)
        step3 = SequenceStep(2, "Step 3", state, 1, 2)
        step4 = SequenceStep(3, "Step 4", state, 1, 2)

        sequence = Sequence("Test Sequence")

        self.assertEquals("Test Sequence", sequence.name)

        sequence.append_step(step1)
        sequence.append_step(step2)
        sequence.append_step(step3)

        self.assertEquals(step1, sequence.get_step(0))
        self.assertEquals(step2, sequence.get_step(1))
        self.assertEquals(step3, sequence.get_step(2))

        sequence.insert_step(step4, 1)

        self.assertEquals(step1, sequence.get_step(0))
        self.assertEquals(step4, sequence.get_step(1))
        self.assertEquals(step2, sequence.get_step(2))
        self.assertEquals(step3, sequence.get_step(3))

        self.assertEquals(0, sequence.get_step(0).number)
        self.assertEquals(1, sequence.get_step(1).number)
        self.assertEquals(2, sequence.get_step(2).number)
        self.assertEquals(3, sequence.get_step(3).number)

        sequence.delete_step(2)

        self.assertEquals(step1, sequence.get_step(0))
        self.assertEquals(step4, sequence.get_step(1))
        self.assertEquals(step3, sequence.get_step(2))

    def test_sequence_runner(self):
        controller = Controller()
        controller.patch.patch_channel(1, 1)
        controller.patch.patch_channel(2, 2)
        controller.patch.patch_channel(3, 3)

        step1 = SequenceStep(0, "", ChannelState(controller, "1 * 100; 2+3*0"), 2, 3)
        step2 = SequenceStep(1, "", ChannelState(controller, "2 * 100; 1+3*0"), 2, 3)
        step3 = SequenceStep(2, "", ChannelState(controller, "3 * 100; 1+2*0"), 2, 3)

        sequence = Sequence("Test")
        sequence.append_step(step1)
        sequence.append_step(step2)
        sequence.append_step(step3)

        # print controller.patch.dmx

        runner = SequenceRunner(controller, 0, sequence)

        # Two Seconds
        runner.update(1); controller.update(1)
        runner.update(1); controller.update(1)

        self.assertEquals(255, controller.patch.dmx[0])
        self.assertEquals(0, controller.patch.dmx[1])
        self.assertEquals(0, controller.patch.dmx[2])

        # Four Seconds
        runner.update(1); controller.update(1)
        runner.update(1); controller.update(1)
        runner.update(1); controller.update(1)
        runner.update(1); controller.update(1)

        # print controller.patch.dmx

        self.assertEquals(127.5, controller.patch.dmx[0])
        self.assertEquals(127.5, controller.patch.dmx[1])
        self.assertEquals(0, controller.patch.dmx[2])

    def test_save_sequence(self):
        controller = Controller()

        controller.patch_channel(1, 1)
        controller.patch_channel(2, 2)
        controller.patch_channel(3, 3)

        print controller.at(ChannelState(controller, "1 at 100"))
        print controller.patch.dmx
        # name, insert = False, step = -1, fade = -1, wait = -1, all = False, cued = False, channelSet = None
        print controller.save_sequence("Test")

        self.assertEquals(1, len(controller.sequences))
        self.assertEquals(1, len(controller.sequences[0].steps))
        self.assertEquals(1, controller.sequences[0].steps[0].channelState.get_num_channels())
        self.assertEquals(-1, controller.sequences[0].steps[0].fade)
        self.assertEquals(-1, controller.sequences[0].steps[0].wait)
        self.assertEquals(0, controller.sequences[0].steps[0].number)
        self.assertEquals("Test", controller.sequences[0].steps[0].label)

        print controller.save_sequence("Test", False, -1, 10, 5)

        self.assertEquals(1, len(controller.sequences))
        self.assertEquals(2, len(controller.sequences[0].steps))
        self.assertEquals(1, controller.sequences[0].steps[1].channelState.get_num_channels())
        self.assertEquals(10, controller.sequences[0].steps[1].fade)
        self.assertEquals(5, controller.sequences[0].steps[1].wait)
        self.assertEquals(1, controller.sequences[0].steps[1].number)
        self.assertEquals("Test", controller.sequences[0].steps[1].label)


        # With "All" flag
        print controller.save_sequence("test", False, -1, 1, 2, True)

        self.assertEquals(2, len(controller.sequences))
        self.assertEquals(1, len(controller.sequences[1].steps))
        self.assertEquals(3, controller.sequences[1].steps[0].channelState.get_num_channels())
        self.assertEquals(1, controller.sequences[1].steps[0].fade)
        self.assertEquals(2, controller.sequences[1].steps[0].wait)
        self.assertEquals(0, controller.sequences[1].steps[0].number)
        self.assertEquals("test", controller.sequences[1].steps[0].label)

        # With "cued" flag
        print controller.save_sequence("test", False, -1, 1, 2, False, True)

        self.assertEquals(2, len(controller.sequences))
        self.assertEquals(2, len(controller.sequences[1].steps))
        self.assertEquals(1, controller.sequences[1].steps[1].channelState.get_num_channels())
        self.assertEquals(1, controller.sequences[1].steps[1].fade)
        self.assertEquals(-1, controller.sequences[1].steps[1].wait)
        self.assertEquals(1, controller.sequences[1].steps[1].number)
        self.assertEquals("test", controller.sequences[1].steps[1].label)

        # With custom channel set
        channelSet = ChannelSet({2, 3})
        print controller.save_sequence("test", False, -1, -1, -1, False, False, channelSet)

        self.assertEquals(2, len(controller.sequences))
        self.assertEquals(3, len(controller.sequences[1].steps))
        self.assertEquals(2, controller.sequences[1].steps[2].channelState.get_num_channels())
        self.assertEquals(-1, controller.sequences[1].steps[2].fade)
        self.assertEquals(-1, controller.sequences[1].steps[2].wait)
        self.assertEquals(2, controller.sequences[1].steps[2].number)
        self.assertEquals("test", controller.sequences[1].steps[2].label)

        print controller.list_sequences()

        print controller.print_sequence("Test")
        print controller.print_sequence("test")




