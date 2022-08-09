
# metti-counter

## Provisioning

Follow the instructions to build and run an [Adafruit RGB Matrix + Real Time Clock HAT on a Raspberry Pi](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/overview). This project tuns on a 64x32 LED matrix powered by a Raspberry Pi 3.

Run install script:

```bash
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/rgb-matrix.sh >rgb-matrix.sh
sudo bash rgb-matrix.sh
```

And configure it with:

```
Interface board type: Adafruit RGB Matrix HAT + RTC
Install RTC support: NO
Optimize: Convenience (sound on, no soldering)
```

Configure `src/constants.py`:

```bash
cp src/constants.py.example src/constants.py
```

Upload repostory to the Raspberry Pi:

```bash
rsync -aP --delete . pi@hostname:/srv/metti-counter/
```

Install Python3 dependencies for the `root` user:

```bash
pip3 install requests
```

To make the python counter server start at boot time as a daemon, install it as a service like so:

```bash
# Configure service
sudo ln -s /srv/metti-counter/provisioning/metti-counter.service /etc/systemd/system/metti-counter.service

# Enable service
sudo systemctl enable metti-counter
sudo systemctl daemon-reload

# (Re-)start service
sudo systemctl start metti-counter
sudo systemctl restart metti-counter

# Show service status
sudo systemctl status metti-counter
```

## Prepare a new font

Create BDF font file using [otf2bdf](http://sofia.nmsu.edu/~mleisher/Software/otf2bdf/):

```bash
otf2bdf font.ttf -p 25 -o font.bdf
```
