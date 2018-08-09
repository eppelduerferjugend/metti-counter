#!/usr/bin/env python

from config import config
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import urllib2, base64, json, time, os, math

class KichenCounter():

  def run(self):
    # configure matrix options
    options = RGBMatrixOptions()
    options.hardware_mapping    = config['matrix_hardware_mapping']
    options.rows                = config['matrix_rows']
    options.cols                = config['matrix_cols']
    options.brightness          = config['matrix_brightness']
    options.pwm_bits            = config['matrix_pwm_bits']
    options.pwm_lsb_nanoseconds = config['matrix_pwm_lsb_nanoseconds']

    # init matrix and canvas
    matrix = RGBMatrix(options = options)
    canvas = matrix.CreateFrameCanvas()

    # configure font and colors
    font = graphics.Font()
    font.LoadFont('font.bdf')
    primaryColor = graphics.Color(255, 255, 255)
    secondaryColor = graphics.Color(255, 0, 0)

    # init loop
    fetchTime = 0
    updateTime = 0
    actualCount = 0
    displayCount = 0

    # loop
    while True:
      # animate counting
      if actualCount != displayCount:
        updateTime = time.time()
        delta = actualCount - displayCount
        displayCount = displayCount + \
          int(math.ceil(abs(delta) * config['count_speed'])) * \
          (delta < 0 and -1 or 1)

      # select color
      cooldown = updateTime > time.time() - config['highlight_cooldown']
      color = secondaryColor if cooldown else primaryColor

      # draw digits to canvas
      canvas.Clear()
      graphics.DrawText(canvas, font, 0, 25, color, str(displayCount).zfill(4))
      canvas = matrix.SwapOnVSync(canvas)

      # fetch count
      if fetchTime < time.time() - config['fetch_lifetime']:
        actualCount = self.fetchCount()
        fetchTime = time.time()

      # wait for next cycle
      time.sleep(0.1)

  def fetchCount(self):
    # compose basic auth token
    auth_token = \
      base64.encodestring("%s:%s" % (
        config['auth_username'],
        config['auth_password']
      )) \
      .replace("\n", "")

    # try to fetch count from the stats api endpoint
    try:
      request = urllib2.Request('https://kichen.spaghettisfest.lu/api/stats')
      request.add_header('Authorization', 'Basic %s' % auth_token)
      response = urllib2.urlopen(request)
      data = json.loads(response.read())
      response.close()
      return data['deliveredItems']

    except Exception as e:
      return 0

# main function
if __name__ == '__main__':
  kichenCounter = KichenCounter()
  kichenCounter.run()
