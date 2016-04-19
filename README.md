# rpi-openwrt-templog
Log Raspberry Pi temperature to server with OpenWRT and display via web


Table of contents
-----------------

- [Introduction](#introduction)
- [How to](#how-to)
- [Compatibility](#compatibility)
- [Example](#example)
- [Other](#other)
- [TODO](#todo)
- [License](#license)



Introduction
------------

Simple set of programs that logs the temperature of an Raspberry Pi running OpenELEC, send the data to an TP-Link MR3020 runnning OpenWRT as server and display de data on html page, to view from any browser.



How to
------------
Each side has it's configuration, see the following folders for more information:

- openwrt => Router acting as server, receiving rpi data, router can be exposed to the internet

- rpi => Raspberry pi acting as client in the same subnet, sending data to openwrt



Compatibility
------------
- Raspberry Pi 1 Model B running OpenELEC 6.0.3

- OpenELEC running Python 2.7.3

- TP-Link MR3020 v1, running OpenWrt GCC 5.3.0 r49161, without any hardware mod



Example
------------

- Example topology

![topology](http://s22.postimg.org/w823f013l/top.png "topology")

- Web page

![temp](https://cdn.pbrd.co/images/iWdao5i.png "temp")

  - Zoom in, and other functionalities

![temp-zoom](https://cdn.pbrd.co/images/iWgIpQP.png "temp-zoom")



Other
------------
Both machines **MUST** have fixed IP address.



TODO
------------
- Improve Python code



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


