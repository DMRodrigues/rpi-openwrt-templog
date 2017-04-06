#!/usr/bin/python

from sys import argv
from time import sleep
from datetime import datetime
from subprocess import Popen, PIPE
from getopt import getopt, GetoptError

import logging

SLEEP = 60
COMANDO = 'echo "$(date +\%Y\%m\%d\%H\%M\%S)","$(cputemp)","$(gputemp)"'

# Limit the lines so that show last 24 hours
# one line is 1 minute, 60min*24h, plus 1 for error, 0 => offset last */
LINES = 1441
MSGLEN = 25
LINESOFF = LINES * MSGLEN

logger = False
fileName = "/storage/www/temp.log"


def printUsage():
   print("Usage: %s [OPTIONS...]\n" % argv[0])
   print("	-f fileName	Local backup file with data")
   print("	-l		To log actions on 'script.log' to read")
   print("	-h		Print this menu\n")
   return


def initScript():
   global fileName, logger

   try:
      myopts, args = getopt(argv[1:], "f:lh")
   except GetoptError as e:
      print(str(e))
      exit(2)

   for o, a in myopts:
      if o == '-f':
         fileName = a
      elif o == '-l':
         logger = True
         logging.basicConfig(filename="script.log", level=logging.DEBUG)
      else:
         printUsage()
         exit(0)

   if logger:
      logging.info("Parsed input => " + str(datetime.now()))

   # truncate/clean file
   try:
      fd = open(fileName, 'w+')
      fd.close()
   except:
      pass # ignore

   if logger:
      logging.info("Cleaned file => " + str(datetime.now()))

   return


def readSaveTemp():
   global logger
   position = 0 # beginning script is 0

   if logger:
      logging.info("Starting temperature logging => " + str(datetime.now()))   

   while True:
      c = Popen(COMANDO, shell=True, stdout=PIPE)
      data = c.communicate()[0] # get data

      if position >= LINESOFF: # max 24h reached
         position = 0

      fd = open(fileName, 'r+')
      fd.seek(position, 0)   # go to last position
      fd.write(data)        # save data
      position = fd.tell(); # save current position
      fd.close()            # close file for web update

      sleep(SLEEP) # sleep for 1 minute
   
   if logger:
       logging.error("Error, program exited => " + str(datetime.now()))
   return # should never reach


def main():
   initScript()
   if logger:
       logging.info("Startup done => " + str(datetime.now()))
   readSaveTemp()
   return


if __name__ == "__main__":
    main()
