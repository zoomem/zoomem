from threading import Thread
from Queue import Queue, Empty
from time import sleep

class NonBlockingStreamReader:

    def __init__(self, stream):
        self._s = stream
        self._q = Queue()

        def _populateQueue(stream, queue):
            while True:
                line = stream.readline()
                if line:
                    lastIndex = line.find("(gdb) ")
                    if lastIndex != -1:
                        line = line[lastIndex+6:]
                    queue.put(line)
                else:
                    break

        self._t = Thread(target = _populateQueue,
                args = (self._s, self._q))
        self._t.daemon = True
        self._t.start()

    def readline(self, timeout = None):
        try:
            return self._q.get(block = timeout is not None,
                    timeout = timeout)
        except Empty:
            return None
