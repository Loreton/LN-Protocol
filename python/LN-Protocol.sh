#!/bin/bash

isActive=$(ps -ef | grep pigiod | wc -l)
[[ "$isActive" != "1" ]] && sudo pigpiod -a1
python3 ./__main__.py ttyUSB2
