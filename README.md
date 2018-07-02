[![Build Status](https://travis-ci.org/iz-sai/instrumental-assignment-iz.svg?branch=master)](https://travis-ci.org/iz-sai/instrumental-assignment-iz)
[![codecov](https://codecov.io/gh/iz-sai/instrumental-assignment-iz/branch/master/graph/badge.svg)](https://codecov.io/gh/iz-sai/instrumental-assignment-iz)

# EventCounter

Simple event counter with 1 second granularity. It provides ability to keep track of number of 
events happened within 1 second long bins, and retrieve number of events that happened over a 
user-specified amount of time until current time.

## Installation

To get the latest development version, use:

    pip install git+https://github.com/iz-sai/instrumental-assignment-iz.git -b develop


## Usage

In a shell with Python 2 or 3:

```python
from event_counter import EventCounter
t = EventCounter()
for _ in range(5):
    t.save()
t.read() # 5
```
