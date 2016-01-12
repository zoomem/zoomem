from subprocess import Popen, PIPE
import time
import subprocess
from threading import Thread
import fcntl
import os

class TimeLimitError(Exception):
    def __init__(self, message, errors):
        super(TimeLimitError, self).__init__(message)
        self.errors = errors


class nbsr_process:
    def __init__(self, name):
        self.proc = Popen(name,stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
        self.time_limit = 15
        self.start = time.time()

        fd = self.proc.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        def limitExecuting(timeout, proc):
            while True:
                now = time.time()
                if(now - self.start >= timeout):
                    self.exitProc()
                    break
                time.sleep(0.5)

        self._t = Thread(target = limitExecuting,args = (60*60,self.proc))
        self._t.daemon = False
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
            try :
                output = self.proc.stdout.readline()
            except:
                time.sleep(0.1)
                continue
            output = self.removeHeader(output.strip())
            start = time.time()
            if output == end:
                break
            output_lines.append(output)
        return output_lines

    def readError(self, end = ""):
        output_lines = []
        start = time.time()
        while True:
            now = time.time()
            if now - start > self.time_limit:
                raise TimeLimitError("","TimeLimitError")
            try :
                output = self.proc.stderr.readline()
                print output
            except:
                time.sleep(0.1)
                continue
            output = self.removeHeader(output.strip())
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
