#!/bin/bash

export PATH="$HOME/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

echo "=========================================================="
echo "Setting up for esp32 build"
echo "Using esp-idf-551"
export IDF_PATH="$HOME/disk/esp/esp-idf-551"
echo "MCU type esp32"
export IDF_TARGET="esp32"
source $IDF_PATH/export.sh

# clean-up last build
rm -rf build-ESP32_AP_NAT

# NAT
cp esp32_common.cmake-NAT esp32_common.cmake
cp mpconfigport.h-AP-NAT mpconfigport.h
make BOARD=ESP32_AP_NAT
# restore files
cp esp32_common.cmake-ORIG esp32_common.cmake
cp mpconfigport.h-ORIG mpconfigport.h

echo "=========================================================="

