# temp


Table of contents
-----------------

- [Introduction](#introduction)
- [How to](#how-to)
- [Different config](#different-config)
- [More info](#more-info)
- [License](#license)
- [Dygraphs License](#dygraphs-license)



Introduction
------------
Running uHTTPd tiny single threaded HTTP server, and this folder must be under the `/www` directory.



How to
------------
Open browser and go to `openwrtIP/temp`

- OpenWRT IP address is 192.168.1.50 => `192.168.1.50/temp`

- If diferent folder name => `openwrtIP/name`



Different config
------------
In case of different file name with the readings:

1. Open .html file
2. Line 11 change `var fileName = "temp.log"` to the correct name insted of "temp.log".


If want link that redirect from openwrtIP instead of redirecting to `/cgi-bin/luci`.

1. Open `/www/index.html`
2. comment `<meta http-equiv="refresh" content="0; URL=/cgi-bin/luci" />`
3. add something like `<a id="try" href="/temp">RaspberryPI Temperature</a>`



More info
------------
For more info about dygraphs [click](http://dygraphs.com) to see examples [click](http://dygraphs.com/gallery)



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


Dygraphs License
------------
http://dygraphs.com/legal.html
