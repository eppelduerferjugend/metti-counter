#!/bin/bash
### BEGIN INIT INFO
# Provides:          Kichen Counter
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       Start kichen-counter daemon at boot time
### END INIT INFO

# navigate to the repository folder
cd /home/pi/kichen-counter

# wait for the raspberry pi to finish stuff first
sleep 10

# run script
python kichen-counter.py > log.txt
