import threading


class StopThread(Exception):
  pass


class StoppableThread(threading.Thread):

  '''Thread with a stopped() flag.'''

  def __init__(self, *args, **kwargs):
    super(StoppableThread, self).__init__(*args, **kwargs)
    self._stopped = threading.Event()

  def stop(self):
    self._stopped.set()

  @property
  def stopped(self):
    return self._stopped.isSet()

  def check_stopped(self):
    if self.stopped:
      raise StopThread

  def run(self):
    try:
      self._target(self, *self._args, **self._kwargs)
    except StopThread:
      pass
