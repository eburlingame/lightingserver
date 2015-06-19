# Simple DMX Lighting Server

## Overview

This is a simple lighting control program to output DMX. The DMX is outputted via the
[Open Lighting Framework's](https://www.openlighting.org/ola/developer-documentation/python-api/)
Python API. It will also run a WebSocket server using [ws3py](https://ws4py.readthedocs.org/en/latest/).

There are a variety of simple commands that control the server's output. These include standard theatrical
lighting console commands like `Channel 1 @ 100`, and also has the ability to save scenes/sequences
containing certain channels that can be recalled later.

The system is designed to run on a Raspberry Pi, and will be tested on that platform in addition to OSX. 
My goal is to write unit tests for all major classes, and the system as a whole. 