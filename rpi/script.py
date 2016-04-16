#!/usr/bin/python

from subprocess import Popen, PIPE
import sys, getopt, socket, time, datetime

SLEEP = 60
MSGLEN = 25
TCP_PORT = 8000
FILENAME = 'temp.log'
COMANDO = 'echo "$(date +\%Y\%m\%d\%H\%M\%S)","$(cputemp)","$(gputemp)"'

ip = ''
port = 0
fileName = ''


try:
   myopts, args = getopt.getopt(sys.argv[1:],"p:f:i:")
except getopt.GetoptError as e:
   print(str(e))
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


def initSocket():
   global s
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((ip, port))
   s.settimeout(5) # should be enough
	

def mysend(msg):
   global s
   totalsent = 0
   while totalsent < MSGLEN:
      sent = s.send(msg[totalsent:])
      #if sent == 0:
         #raise RuntimeError("socket connection broken")
      totalsent = totalsent + sent


def myreceive():
   global s
   chunks = []
   bytes_recd = 0
   while bytes_recd < MSGLEN:
      chunk = s.recv(MSGLEN - bytes_recd)
      #if chunk == '':
         #raise RuntimeError("socket connection broken")
      chunks.append(chunk)
      bytes_recd = bytes_recd + len(chunk)
   return ''.join(chunks)


def readTemp():
   global s
   while True:
      c = Popen(COMANDO, shell=True, stdout=PIPE)
      data = c.communicate()[0]

      try:
         mysend(data)
         dataOver = myreceive()
         if data != dataOver:
            raise Exception('ERROR compare data') # server must be down!!!
      except:
         print "ERROR starting save localy " + datetime.datetime.now().time()
         saveLocal(data)
      time.sleep(SLEEP)


def saveLocal(msg):
   global s
   fd = open(fileName, 'w+')
   fd.write(msg)
   time.sleep(SLEEP)

   while True:
      c = Popen(COMANDO, shell=True, stdout=PIPE)
      data = c.communicate()[0]

      try: # reuse the same socket
         initSocket()

         # at this point safe to send, one shot only
         fd.seek(0)
         for line in fd:
            mysend(line)
            s.recv(MSGLEN) # ignore => fast-forward
         mysend(data) # our fresh data
         s.recv(MSGLEN)
         fd.close()

         print "Back to client to send data " + datetime.datetime.now().time()
         return
      except:
         fd.write(data)
         time.sleep(SLEEP)

initSocket()
readTemp()
