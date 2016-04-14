#!/usr/bin/python

import sys, getopt
import threading, socket, time
from subprocess import Popen, PIPE

TCP_PORT = 8000
BUFFER_SIZE = 30
FILENAME = 'temp.log'
COMANDO = 'echo "$(date +\%Y\%m\%d\%H\%M\%S)","$(cputemp)","$(gputemp)"'

ip = ''
port = 0
fileName = ''

try:
   myopts, args = getopt.getopt(sys.argv[1:],"p:f:i:")
except getopt.GetoptError as e:
   print (str(e))
   print("Usage: %s -i serverIP [-p port -f temporaryFile]" % sys.argv[0])
   sys.exit(2)

for o, a in myopts:
    if o == '-i':
        ip = a
    elif o == '-p':
        port = int(a)
    elif o == '-f':
        fileName =a

if ip == '':
   print("\nERROR: missing OpenWRT server IP\n")
   print("Usage: %s -i serverIP [-p port -f temporaryFile]\n" % sys.argv[0])
   sys.exit(2)
if port == 0:
   port = TCP_PORT
if fileName == '':
   fileName = FILENAME

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
s.settimeout(3) # should be enough

def readTemp():
   while True:
      c = Popen(COMANDO, shell=True, stdout=PIPE)
      data = c.communicate()[0]
      #print data[:-1]

      try:
         s.send(data)
         dataOver = s.recv(BUFFER_SIZE)
         if data != dataOver:
            raise Exception('ERROR compare data') # server must be down!!!
      except:
         print "ERROR starting save localy"
         saveLocal(data)
      time.sleep(60)


def saveLocal(msg):
   global s
   fd = open(fileName, 'w+')
   fd.write(msg)
   time.sleep(60)

   while True:
      c = Popen(COMANDO, shell=True, stdout=PIPE)
      data = c.communicate()[0]
      fd.write(data)
      #print data[:-1]

      try:
         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         s.connect((ip, port))

         # at this point safe to send, one shot all
         fd.seek(0)
         for line in fd:
            s.send(line)
            s.recv(BUFFER_SIZE) # ignore => fast-forward
         fd.close()

         print "Back to client to send data"
         return
      except:
         #print "some sleep"
         time.sleep(60)
   return

readTemp()
