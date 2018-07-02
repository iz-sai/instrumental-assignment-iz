# -*- coding: utf-8 -*-
import time
from collections import deque

from .compat import xrange


BUFFER_SIZE = 300 # seconds


class EventCounter(object):
    """Simple event counter with 1 second granularity.

    Use it to keep track of number of events happened within 1 second long bins, and retrieve number 
    of events that happened over a user-specified amount of time until current time.

    Parameters
    ----------
    buffer_size : int, optional
        Total time range of counter in seconds. If not given or malformed, default `BUFFER_SIZE` is
        used.

    Notes
    -----
    Events happened more than `buffer_size` seconds ago are discarded.

    Example
    -------
    >>> from event_counter import EventCounter
    >>> t = EventCounter()
    >>> for _ in range(5):
    ...     t.save()
    >>> t.read()
    5
    >>> import time
    >>> time.sleep(1)
    >>> t.save()
    >>> t.read(1)
    1
    >>> t.read()
    6
    """

    def __init__(self, buffer_size=BUFFER_SIZE):
        self._buffer_size = buffer_size if type(buffer_size) is int and buffer_size > 0 \
                                        else BUFFER_SIZE
        self._buffer = deque([0] * self._buffer_size, maxlen=self._buffer_size)
        self._timer = time.time()


    def _buffer_append(self):
        """Buffer housekeeping.

        Append to the circular buffer new bin(s) with counter(s) set to zero, and set last 
        (active) bin edge timestamp. Called from each `save()` and `read()`.
        """
        current_time = time.time()
        diff = current_time - self._timer
        # `if` here is faster than extending buffer with an empty list
        if diff > 1:
            n_bins = min(int(diff), self._buffer_size)
            self._buffer.extend([0] * n_bins)
            self._timer += n_bins


    def save(self):
        """Save event to counter."""
        self._buffer_append()
        self._buffer[-1] += 1


    def read(self, n_seconds=None):
        """Read event counter.

        Return number of events recorded in the counter during specified time interval.

        Parameters
        ----------
        n_seconds : int, optional
            Time interval in seconds until current time, i.e. count events occured within last 
            `n_seconds` bins of the counter, each 1 second long (except for the last bin which 
            most often has been exposed for less than 1 second at the read moment). If not given or 
            malformed, time interval is set to the full time range of the counter.

        Returns
        -------
        int
            Number of recorded events.
        """
        n_seconds = min(n_seconds, self._buffer_size) if type(n_seconds) is int and n_seconds > 0 \
                                                        else self._buffer_size

        self._buffer_append()

        total = 0
        for i in xrange(self._buffer_size - n_seconds, self._buffer_size):
            total += self._buffer[i]

        return total
