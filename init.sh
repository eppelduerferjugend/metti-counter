#!/bin/bash
### BEGIN INIT INFO
# Provides:          Metti Counter
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Description:       Start metti-counter daemon at boot time
### END INIT INFO

# Navigate to the working directory
cd /opt/metti-counter

# Wait for the raspberry pi to finish stuff first
sleep 10

# Run service
python3 src/index.py > log.txt 2>&1
