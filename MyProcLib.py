"""
My Process Execution Library
"""

import os
import time
import Queue
import platform
import threading
import subprocess


NewLine = '\n'

if platform.system() == 'Windows':
    NewLine = '\r\n'


def queue_output(out, queue):
    """Queue output"""
        
    for line in iter(out.readline, b''):
        queue.put(line)
        
    out.close()


def retrieve_output(queue):
    """Retrieve output"""

    output = ''

    try:
        data = queue.get_nowait()
        while data != '':
            output += data
            data = queue.get_nowait()
    except Queue.Empty:
        pass

    return output
    

class MyProc:

    def __init__(self, proc_name, debug = False):

        self.proc_name = proc_name
        self.debug = debug
        self.interactive = False
        self.proc = None
        self.out_queue = None
        self.err_queue = None

        self.__debug_print('[*] Process: ' + proc_name)
    

    def run_proc(self, param = None, no_wait = False):
        """Run process only"""

        cmd = [self.proc_name]

        if param is not None:
            cmd += param.split()

        self.__debug_print('[*] Run: ' + str(cmd))

        if no_wait:
            subprocess.Popen(cmd)
        else:
            subprocess.call(cmd)


    def run_proc_output(self, param = None):
        """Run process and return the output"""

        cmd = [self.proc_name]

        if param is not None:
            cmd += param.split()

        self.__debug_print('[*] Run: ' + str(cmd))
        
        output = subprocess.check_output(cmd)

        self.__debug_print('[*] Output:' + NewLine + output)

        return output


    def run_proc_interactive(self, param = None):
        """Interactive with process"""

        self.interactive = True

        cmd = [self.proc_name]

        if param is not None:
            cmd += param.split()

        self.__debug_print('[*] Run: ' + str(cmd))

        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.out_queue = Queue.Queue()
        self.err_queue = Queue.Queue()

        out_thread = threading.Thread(target=queue_output, args=(self.proc.stdout, self.out_queue))
        err_thread = threading.Thread(target=queue_output, args=(self.proc.stderr, self.err_queue))
        
        out_thread.daemon = True
        err_thread.daemon = True
        
        out_thread.start()
        err_thread.start()

        time.sleep(0.1)


    def send_input(self, input):
        """Send input to process"""

        if self.interactive:

            self.__debug_print('[*] Stdin: ' + input)

            self.proc.stdin.write(input + NewLine)
            time.sleep(0.1)


    def get_output(self):
        """Get output"""

        out_stdout = ''
        out_stderr = ''

        if self.interactive:
            out_stdout = retrieve_output(self.out_queue)
            out_stderr = retrieve_output(self.err_queue)

            if len(out_stdout) > 0:
                self.__debug_print('[*] Stdout: ' + NewLine + out_stdout)
                self.__debug_print('-' * 40)

            if len(out_stderr) > 0:
                self.__debug_print('[*] Stderr: ' + NewLine + out_stderr)
                self.__debug_print('-' * 40)

        return out_stdout, out_stderr


    def __debug_print(self, message):
        """Print debug info"""

        if self.debug:
            print message
    

def run_process():
    """Run process"""

    proc_name = 'c:\\Windows\\System32\\cmd.exe'
    proc = MyProc(proc_name, debug = True)
    
    param = ' /c notepad test.txt'
    proc.run_proc(param, no_wait = True)
    
    param = ' /c ping 127.0.0.1'
    output = proc.run_proc_output(param)
    print output
    
    proc.run_proc_interactive()
    
    while True:
        
        try:
            input = raw_input("Input: ")
            proc.send_input(input)
            
            out_stdout, out_stderr = proc.get_output()
        
            if out_stdout != '':
                print out_stdout
                
            if out_stderr != '':
                print out_stderr
            
        except Exception as e:
            print '[!] Error: ' + str(e)
            break
    

if __name__ == '__main__':

    run_process()