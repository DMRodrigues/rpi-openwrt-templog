# openwrt


Table of contents
-----------------

- [Introduction](#introduction)
- [How to](#how-to)
- [Start Up](#start-up)
- [Web Folder](#web-folder)
- [Different config](#different-config)
- [License](#license)



Introduction
------------
This contains both the server code to run and the required html to see the graph of temperature.

I'm using pivot-overlay as extroot, for more info read [Rootfs on External Storage](https://wiki.openwrt.org/doc/howto/extroot).

- The server records the last 24 hours of temperature on the file that dygraph reads.
- The file is saved in circular way, which means, the first 4 bytes is the raw integer of the last position, plus '\n', and then starts the data with 25 bytes each line.
- When the limit of the data is achieved (24 hours recorded), it starts writing the file from the beginning, and so on.


How to
------------
There are two options to run the server:

- First method:

1. use the Makefile to compile the code: `make`
2. send the exec to the server with scp: `scp rpi-templog root@IP:/www/temp`
3. then ssh to server and run the exec: `/www/temp/rpi-templog &`

- Second method

1. ssh to server and download package from here: `wget https://github.com/DMRodrigues/rpi-openwrt-templog/blob/master/openwrt/package/rpi-templog_1_ar71xx.ipk`
2. install with opkg: `opkg install rpi-templog_1_ar71xx.ipk`
3. the run with: `rpi-templog &`



Start Up
------------
The run the server automatically at start up, must edit `/etc/rc.local` and add one of the previous type:

- `/www/temp/rpi-templog &`
- `rpi-templog &`



Different config
------------
It's possible to chose a diferent folder to save the logs and different port

- Different file name: `rpi-templog -f /tmp/temp.txt &`
- Different port: `rpi-templog -p port &`


Web folder
------------
The default folder used for display the temperature is: `/www/temp/`

However, it's possible to change the folder name or location



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

