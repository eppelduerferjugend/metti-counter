# kichen-counter

## Deployment

Follow the instructions to build and run an [Adafruit RGB Matrix + Real Time Clock HAT on a Raspberry Pi](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/overview). This project tuns on a 64x32 LED matrix powered by a Raspberry Pi 3.

Create `config.py` using the `config.py.example` template.

Create BDF font file using [otf2bdf](https://www.math.nmsu.edu/%7Emleisher/Software/otf2bdf/):

```bash
otf2bdf RobotoMono-Bold.ttf -p 25 -o font.bdf
```

Upload repostory to the Raspberry Pi:

```bash
rsync -aP --delete . pi@hostname:/home/pi/kichen-counter
```

Install service:

```bash
sudo ln -s /home/pi/kichen-counter/init.sh /etc/init.d/kichen-counter
sudo update-rc.d kichen-counter defaults
```
