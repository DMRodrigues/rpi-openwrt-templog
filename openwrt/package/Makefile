#
# Copyright (C) 2013-2016 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=rpi-templog
PKG_RELEASE:=1

include $(INCLUDE_DIR)/package.mk

define Package/rpi-templog
  SECTION:=utils
  CATEGORY:=Utilities
  TITLE:=RPi Server temperature logger
  MAINTAINER:=DMRodrigues <github.com/DMRodrigues>
endef

define Package/rpi-templog/description
 This package provides the server so that RaspberryPi
 can connect and save temperature readings.
endef

define Build/Prepare
    $(INSTALL_DIR) $(PKG_BUILD_DIR)
	$(INSTALL_DATA) ./src/rpi-templog.c $(PKG_BUILD_DIR)/
endef

define Build/Compile
	$(TARGET_CC) $(TARGET_CFLAGS) -Wall -O3 \
		-o $(PKG_BUILD_DIR)/rpi-templog $(PKG_BUILD_DIR)/rpi-templog.c
endef

define Package/rpi-templog/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/rpi-templog $(1)/usr/bin/
endef

$(eval $(call BuildPackage,rpi-templog))
