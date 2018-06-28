### Usage

In a shell with Python 2 or 3:

```
from event_counter import EventCounter
t = EventCounter()
[t.save() for _ in range(5)] # nasty, but one-liner
t.read() # 5
```
