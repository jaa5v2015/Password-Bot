from pyad import *
import rpyc
from rpyc.utils.server import ThreadedServer
import datetime
import subprocess
import os
import win32com.client as win32



date_time  = datetime.datetime.now()

class MonitorService(rpyc.Service):
    def on_connect(self,conn):
        print('conncected on {}'.format(date_time))
    def on_disconnect(self,conn):
        print('disconnect on {}\n'.format(date_time))
    def exposed_run_commands(self, commmand):
        try:
            output = subprocess.check_output(commmand, shell=True)
            print(output)
        except subprocess.CalledProcessError as Error:
            print(Error.returncode)
            print(Error.output)




if __name__ == '__main__':
    t = ThreadedServer(MonitorService, port=19961)
    t.start()


