# rpi


Table of contents
-----------------

- [Introduction](#introduction)
- [How to](#how-to)
- [Start Up](#start-up)
- [Different config](#different-config)
- [License](#license)


Introduction
------------
Simple python script that creates connection to server and every minute executes command to get temperatures and sends it.

If the server goes down, for any reason, it starts saving data in local backup file. Then tries to create new connection to the server to send all the backup data once.



How to
------------

**IMPORTANT:** Must know the server IP (OpenWRT)

1. send the script to the RPi with scp: `scp script root@IP:/storage`
2. ssh to RPi and run the script: `python script.py -i serverIP &`



Start Up
------------
To run the script at startup do [more info](http://wiki.openelec.tv/index.php/Autostart.sh):

1. ssh to RPi
2. the execute `nano /storage/.config/autostart.sh`
3. paste ``(
 python /storage/script.py -i serverIP;
) &``



Different config
------------
It's possible to chose a diferent folder to save the logs and different port

- Different backup file name: `python script.py -i serverIP -f /tmp/tmp.txt &`
- Different port: `python script.py -i serverIP -p port &`
- Log in file 'script.log' what happens : `python script.py -i serverIP -l &`



License
------------

The MIT License (MIT)

Copyright (c) 2016 Diogo Miguel Rodrigues

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

