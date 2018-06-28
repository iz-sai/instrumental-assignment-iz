import unittest
import time

from event_counter import EventCounter


# Python 2/3 tmp hack
try:
    xrange
except NameError:
    xrange = range


class TestAll(unittest.TestCase):

    def test_buffer_contents_simple(self):
        """
        """
        n_events = 100

        t = EventCounter(3)

        for _ in xrange(n_events):
            t.save()

        self.assertEqual(list(t._buffer), [0, 0, n_events])


    def test_buffer_contents_with_sleep(self):
        """
        """
        n_events = 100

        t = EventCounter(3)

        for _ in xrange(n_events):
            t.save()

        time.sleep(2)
        t.save()

        self.assertEqual(list(t._buffer), [n_events, 0, 1])


    def test_write_speed(self):
        """Testing saving events at a rate greater than 1M/s"""
        buffer_size = 3
        max_rate = 1e6 # events/s
        n_events = int(buffer_size * max_rate)

        t = EventCounter(buffer_size) # each buffer element has to take at least `max_rate` events

        for _ in xrange(n_events):
            t.save()

        self.assertEqual(t.read(), n_events)


if __name__ == '__main__':
    unittest.main()
    