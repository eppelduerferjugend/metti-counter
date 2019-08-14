
# metti-counter

## Deployment

Follow the instructions to build and run an [Adafruit RGB Matrix + Real Time Clock HAT on a Raspberry Pi](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/overview). This project tuns on a 64x32 LED matrix powered by a Raspberry Pi 3.

Configure `src/constants.py`:

```bash
cp src/constants.py.example src/constants.py
```

Create BDF font file using [otf2bdf](https://www.math.nmsu.edu/%7Emleisher/Software/otf2bdf/):

```bash
otf2bdf RobotoMono-Bold.ttf -p 25 -o font.bdf
```

Upload repostory to the Raspberry Pi:

```bash
rsync -aP --delete . pi@hostname:/opt/metti-counter/
```

Install Python3 dependencies for the `root` user:

```bash
sudo pip3 install requests
sudo pip3 install --upgrade requests[security]
```

Install service:

```bash
sudo ln -s /opt/metti-counter/init.sh /etc/init.d/metti-counter
sudo update-rc.d metti-counter defaults
```

Uninstall service:

```bash
sudo update-rc.d metti-counter remove
```
