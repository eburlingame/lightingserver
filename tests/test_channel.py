from unittest import TestCase
from main.channel import *

__author__ = 'Eric Burlingame'


class TestChannel(TestCase):

    def test_init(self):
        chn = Channel(1, 2, "Test", "Parcan")

        self.assertEqual(0, chn.value)
        self.assertEqual(1, chn.number)
        self.assertEqual(2, chn.dmxAddr)
        self.assertEqual("Test", chn.label)
        self.assertEqual("Parcan", chn.fixture)

        self.assertRaises(Exception, Channel, -1, 2, "", "")
        self.assertRaises(Exception, Channel, 1, -1, "", "")
        self.assertRaises(Exception, Channel, 1, 513, "", "")

    def test_fade(self):
        fade = Fade(100)
        self.assertEquals(100, fade.value)

        # Fade out in two seconds
        fade.start(0, 2)
        # First second
        fade.update(1)
        self.assertNotEqual(0, fade.value)
        # Second second
        fade.update(1)
        self.assertEquals(0, fade.value)

        fade = Fade(0)
        self.assertEquals(0, fade.value)

        # Fade to 50 in 0 seconds
        fade.start(50, 0)
        # First second
        fade.update(1)
        self.assertEquals(50, fade.value)
        fade.update(1)
        self.assertEquals(50, fade.value)

        self.assertRaises(Exception, fade.start, 256, 0)
