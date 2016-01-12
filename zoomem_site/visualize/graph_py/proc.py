from subprocess import Popen, PIPE
import non_blocking_stream
import time
import subprocess
from threading import Thread

class TimeLimitError(Exception):
    def __init__(self, message, errors):
        super(TimeLimitError, self).__init__(message)
        self.errors = errors


class nbsr_process:
    def __init__(self, name):
        self.proc = Popen(name,stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
        self.time_limit = 15
        self.start = time.time()
        def limitExecuting(timeout, proc):
            while True:
                now = time.time()
                if(now - self.start >= timeout):
                    self.exitProc()
                    break
                time.sleep(0.5)

        self._t = Thread(target = limitExecuting,args = (60*60,self.proc))
        self._t.daemon = True
        self._t.start()

    def exitProc(self):
        self.proc.kill()

    def readTill(self, end = ""):
        output_lines = []
        start = time.time()
        while True:
            now = time.time()
            if now - start > self.time_limit:
                raise TimeLimitError("","TimeLimitError")
            output = self.proc.stdout.readline()
            if output == None:
                time.sleep(0.1)
                continue;
            output = self.removeHeader(output)
            start = time.time()
            if output == end:
                break
            output_lines.append(output)
        return output_lines

    def write(self, command):
        command+="\n"
        self.proc.stdin.write(command.encode())

    def removeHeader(self,str):
        idx = 0
        i = 0
        while i < len(str):
            if str[i:i+len("(gdb)")] == "(gdb)":
                idx = i+len("(gdb)") + 1
                i = idx
            else:
                break
        return str[idx:].strip()
