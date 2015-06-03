from unittest import TestCase
from main.patch import Patch

__author__ = 'eric'


class TestPatch(TestCase):
    def test_patch_channel(self):
        patch = Patch()

        patch.patch_channel(1, 2)
        self.assertEquals(0, patch.channels[0].value)
        self.assertEquals(1, patch.channels[0].number)
        self.assertEquals(2, patch.channels[0].dmxAddr)

        self.assertRaises(Exception, patch.patch_channel, -1, 0)
        self.assertRaises(Exception, patch.patch_channel, 1, -1)
        self.assertRaises(Exception, patch.patch_channel, 1, 513)

        patch.set_channel(1, 100)
        patch.update_channels(1)
        self.assertEquals(100, patch.channels[0].value)

    def test_update_channels(self):
        patch = Patch()

        patch.patch_channel(1, 1, "Channel 1")
        patch.patch_channel(2, 2, "Channel 2")
        patch.patch_channel(3, 3, "Channel 3")
        patch.patch_channel(4, 4, "Channel 4")

        patch.channels[0].fadeTo(100, 0)
        patch.channels[1].fadeTo(50, 1)
        patch.channels[2].fadeTo(100, 2)

        # First second
        patch.update_channels(1)
        self.assertEquals(100, patch.channels[0].value)

        # Second second
        patch.update_channels(1)
        self.assertEquals(100, patch.channels[0].value)
        self.assertEquals(50, patch.channels[1].value)

        # Third second
        patch.update_channels(1)
        self.assertEquals(100, patch.channels[0].value)
        self.assertEquals(50, patch.channels[1].value)
        self.assertEquals(100, patch.channels[2].value)