#!/bin/sh

sleep 5
httpd -c /storage/www/httpd.conf
(python /storage/www/script.py)&
exit 0
