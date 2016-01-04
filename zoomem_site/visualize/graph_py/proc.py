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
        self.proc_nbsr = non_blocking_stream.NonBlockingStreamReader(self.proc.stdout)
        self.time_limit = 5
        def limitExecuting(timeout, proc,proc_nbsr):
            start = time.time()
            while True:
                now = time.time()
                if(now - start >= timeout):
                    self.exitProc(proc,proc_nbsr)
                    break
                time.sleep(0.5)

        self._t = Thread(target = limitExecuting,args = (60*60,self.proc,self.proc_nbsr))
        self._t.daemon = True
        self._t.start()

    def exitProc(self,proc,proc_nbsr):
        proc.kill()
        proc_nbsr.done = True

    def read(self, timeout = 0.5):
        output_lines = ""
        while True:
            output = self.proc_nbsr.readline(timeout)
            if output == None:
                break
            idx = output.find("(gdb)")
            if idx != -1:
                output = output[idx + len("(gdb)"):]
            output_lines += output
        return output_lines.strip()

    def readTill(self, end = ""):
        output_lines = []
        start = time.time()
        while True:
            now = time.time()
            if now - start > self.time_limit:
                raise TimeLimitError("","TimeLimitError")

            output = self.proc_nbsr.readline()
            if output == None:
                time.sleep(0.1)
                continue;
            idx = output.find("(gdb)")
            if idx != -1:
                output = output[idx + len("(gdb)"):]
            output = output.strip()
            if output == end:
                break
            output_lines.append(output)
        return output_lines

    def write(self, command):
        command+="\n"
        self.proc.stdin.write(command.encode())
    def clean(self,t = 0.5):
        return self.read(t)
