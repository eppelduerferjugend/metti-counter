#!/usr/bin/env python3

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import constants
import threading, requests, time, os, math, signal

class Display_Thread(threading.Thread):

  def __init__(self):
    threading.Thread.__init__(self)
    self.stop_flag = threading.Event()
    self.count = 0

  def run(self):
    print('[Display] Display thread started.')

    # Configure matrix options
    options = RGBMatrixOptions()
    options.hardware_mapping    = constants.matrix_hardware_mapping
    options.rows                = constants.matrix_rows
    options.cols                = constants.matrix_cols
    options.brightness          = constants.matrix_brightness
    options.pwm_bits            = constants.matrix_pwm_bits
    options.pwm_lsb_nanoseconds = constants.matrix_pwm_lsb_nanoseconds

    # Init matrix and canvas
    matrix = RGBMatrix(options = options)
    canvas = matrix.CreateFrameCanvas()

    # Configure font and colors
    font = graphics.Font()
    font.LoadFont('assets/IBMPlexMono-Regular.bdf')
    primaryColor = graphics.Color(255, 255, 255)
    secondaryColor = graphics.Color(0, 255, 0)

    # Init loop
    update_time = 0
    count = 0

    # Loop until the stop flag is raised
    while not self.stop_flag.is_set():
      # Animate counting
      if self.count != count:
        update_time = time.time()
        delta = self.count - count
        count = count + \
          int(math.ceil(abs(delta) * constants.count_speed)) * \
          (delta < 0 and -1 or 1)

      # Select color
      cooldown = update_time > time.time() - constants.highlight_cooldown
      color = secondaryColor if cooldown else primaryColor

      # Draw digits to canvas
      canvas.Clear()
      graphics.DrawText(canvas, font, 2, 25, color, str(count).zfill(4))
      canvas = matrix.SwapOnVSync(canvas)

      # Wait for next cycle
      time.sleep(0.1)

  def stop(self):
    print('[Display] Stopping display thread.')
    self.stop_flag.set()

  def setCount(self, count):
    if self.count != count:
      print('[Display] Set count to {}.'.format(count))
      self.count = count

class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass

def shutdown_handler(signum, frame):
  """ Raise an exception to gracefully end the process """
  print('Caught signal {}'.format(signum))
  raise ServiceExit

def fetch_completed_item_quantity(supplier_id):
  """ Fetch completed item count for the given destination """
  try:
    response = requests.request(
      'GET',
      constants.service_root + '/suppliers/{}'.format(str(supplier_id)),
      headers={"Authorization": "Bearer " + constants.service_auth_token})

    if response.status_code == 200:
      data = response.json()
      # This may throw an 'AttributeError'
      return data['statistics']['completedItemQuantity']

  except Exception as err:
    print('Fetching completed item count failed: {}'.format(str(err)))

  return False

def main():
  # Register shutdown handlers
  signal.signal(signal.SIGTERM, shutdown_handler)
  signal.signal(signal.SIGINT, shutdown_handler)

  try:
    # Start the printing thread
    display_thread = Display_Thread()
    display_thread.start()

    # Daemon loop
    while True:

      # Update count
      count = fetch_completed_item_quantity(constants.supplier_id)
      if count != False:
        display_thread.setCount(count)

      # Wait until next poll
      time.sleep(constants.polling_interval)

  except ServiceExit as e:
    display_thread.stop()

# Main call
if __name__ == '__main__':
  main()
