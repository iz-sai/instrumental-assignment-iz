import time
from collections import deque


BUFFER_SIZE = 300 # seconds

# Python 2/3 tmp hack
try:
    xrange
except NameError:
    xrange = range


class EventCounter(object):
    """
    We employ double-ended queue here which has O(1) performance for append(). Trade-off is slower .read() which in the worst case is O(n**2), but that's still okay.

    Usage:

    > from event_counter import EventCounter
    > t = EventCounter()
    > [t.save() for _ in range(5)] # nasty, but one-liner
    > t.read()

    Parameters
    ----------
    TBW
    """

    def __init__(self, buffer_size=BUFFER_SIZE):
        self._buffer_size = buffer_size if type(buffer_size) is int and buffer_size > 0 else BUFFER_SIZE
        self._buffer = deque([0] * self._buffer_size, maxlen=self._buffer_size)
        self._timer = time.time()


    def _buffer_append_time(self):
        """
        """
        current_time = time.time()
        diff = current_time - self._timer
        if diff > 1:
            self._buffer.extend([0] * min(int(diff), self._buffer_size))
            self._timer = current_time


    def save(self):
        """Save event to counter

        Parameters
        ----------
        TBW
        """
        self._buffer_append_time()
        self._buffer[-1] += 1


    def read(self, n_seconds=None):
        """Read counter

        Parameters
        ----------
        TBW        
        """
        n_seconds = min(n_seconds, self._buffer_size) if type(n_seconds) is int else self._buffer_size

        self._buffer_append_time()

        total = 0
        for i in xrange(self._buffer_size - n_seconds, self._buffer_size):
            total += self._buffer[i]

        return total

