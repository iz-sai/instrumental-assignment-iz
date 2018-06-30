# EventCounter

Simple event counter with 1-second granularity.

### Example

In a shell with Python 2 or 3:

```python
from event_counter import EventCounter
t = EventCounter()
for _ in range(5):
    t.save()
t.read() # 5
```
