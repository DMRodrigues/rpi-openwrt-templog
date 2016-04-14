# export PATH=$PATH:/www/temp

CC = mips-openwrt-linux-gcc
CFLAGS = -Wall -O3

all:
	$(CC) $(CFLAGS) rpi-templog.c -o rpi-templog

clean:
	rm -rf rpi-templog
