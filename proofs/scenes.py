from main.channel_set import *
from main.scene import *
from main.controller import *

controller = Controller()

state = ChannelState(controller, "1*10;2*20;3*30;14*40")

scn = Scene("Foo", state, 10)

print scn.toString()

set = ChannelSet({1, 2, 3})

newState = scn.get_custom_channel_state(controller, set)
for chn in newState.states:
    print "%s at %s" % (chn["number"], chn["value"])