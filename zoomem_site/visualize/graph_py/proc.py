from subprocess import Popen, PIPE
import non_blocking_stream
import time
import subprocess

class nbsr_process:
    def __init__(self, name):
        self.proc = Popen(name,stdin = PIPE, stdout = PIPE, stderr = PIPE, shell = True)
        self.proc_nbsr = non_blocking_stream.NonBlockingStreamReader(self.proc.stdout)

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
        while True:
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

    def clean(self):
        return self.read()
