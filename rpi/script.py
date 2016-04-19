#!/usr/bin/python

from sys import argv
from time import sleep
from datetime import datetime
from subprocess import Popen, PIPE
from getopt import getopt, GetoptError

import socket, logging

SLEEP = 60
MSGLEN = 25
COMANDO = 'echo "$(date +\%Y\%m\%d\%H\%M\%S)","$(cputemp)","$(gputemp)"'

ip = ''
port = 8000
logger = False
fileName = "temp.log"


def printUsage():
   print("Usage: %s -i serverIP [OPTIONS...]\n" % argv[0])
   print("	-i ip		Server IP address")
   print("	-p port		Server port to use")
   print("	-f fileName	Local backup file with data")
   print("	-l 		To log some actions on 'script.log' to read")
   print("	-h 		Print this menu\n")
   return


def initScript():
   global ip, port, fileName, logger

   try:
      myopts, args = getopt(argv[1:], "p:f:i:lh")
   except GetoptError as e:
      print(str(e))
      exit(2)

   for o, a in myopts:
      if o == '-i':
         ip = a
      elif o == '-p':
         port = int(a)
      elif o == '-f':
         fileName = a
      elif o == '-l':
         logger = True
         logging.basicConfig(filename="script.log", level=logging.DEBUG)
      else:
         printUsage()
         exit(0)

   if ip == '':
      print("\nERROR: missing OpenWRT server IP\n")
      printUsage()
      exit(2)

   try:
      initSocket()
   except Exception as e:
      if logger:
         logging.warning("Fail to create connection start = " + str(e) + " => " + str(datetime.now()))
      pass # fail to init, then start saving local

   return


def initSocket():
   global s
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((ip, port))
   s.settimeout(5) # should be enough
   return
	

def mySend(msg):
   global s
   totalsent = 0
   
   while totalsent < MSGLEN:
      sent = s.send(msg[totalsent:])
      #if sent == 0:
         #raise RuntimeError("socket connection broken")
      totalsent = totalsent + sent
   return


def myReceive():
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
   global s, logger
   
   while True:
      c = Popen(COMANDO, shell=True, stdout=PIPE)
      data = c.communicate()[0]

      try:
         try:
            mySend(data)
         except Exception as e:
            if logger:
               logging.warning("Fail to send = " + str(e) + " => " + str(datetime.now()))
            raise # simple re-raise
         
         try:
            dataOver = myReceive()
         except Exception as e:
            if logger:
               logging.warning("Fail to receive = " + str(e) + " => " + str(datetime.now()))
            raise # simple re-raise

         if data != dataOver:
            raise Exception("ERROR") # error data didn't match
      
      except:
         if logger:
            logging.warning("Starting to save localy => " + str(datetime.now()))
         saveLocal(data)

      sleep(SLEEP)

   return # should never reach


def saveLocal(msg):
   global s, logger
   
   fd = open(fileName, 'w+')
   fd.write(msg)
   sleep(SLEEP)

   while True:
      c = Popen(COMANDO, shell=True, stdout=PIPE)
      data = c.communicate()[0]

      try:
         initSocket() # reuse the same socket

         # at this point safe to send, one shot only
         fd.seek(0)
         for line in fd:
            mySend(line)
            s.recv(MSGLEN) # ignore => fast-forward
         mySend(data) # our fresh data
         s.recv(MSGLEN)
         fd.close()

         if logger:
            logging.warning("Back to client to send data => " + str(datetime.now()))
         return

      except:
         fd.write(data)
         sleep(SLEEP)
   return


def main():
   initScript()
   readTemp()


if __name__ == "__main__":
    main()
