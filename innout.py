from itertools import count
from itertools import takewhile
from queue import Queue
from stoppablethread import StopThread
from stoppablethread import StoppableThread
import logging
import random
import string
import time


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(message)s',
                    datefmt="%H:%M:%S:%N")


class Port(object):

  def read(self):
    '''Waits until and returns next input char available.'''
    wait_sec = random.choice([0.1] * 16 + [0.5] * 8 + [2] * 2 + [5] * 1)
    val = random.choice(string.ascii_letters + '\n' * 15)
    logging.debug(f'waiting for new input {repr(val)} for {wait_sec}s')
    time.sleep(wait_sec)
    return val


def serOpen():
  return Port()


GREEN=32
YELLOW=33
def highlight(txt, color):
  return f'\033[{color}m{txt}\033[0m'


# Result does NOT include '\n'.
def readline_from_port(port):
  return ''.join(takewhile(lambda c: c != '\n',
                           (port.read() for _ in count())))


def handle_input(thread, inport, q):
  for _ in range(5):
    thread.check_stopped()
    data = readline_from_port(inport)
    logging.info(f'enqueuing {repr(data)}')
    print(highlight(f'I PUT {repr(data)}', YELLOW))
    q.put(data)


def handle_output(thread, q):
  while True:
    thread.check_stopped()
    data = q.get()
    if data is None:
      return
    logging.info(f'received {repr(data)}')
    logging.info(f'performing complicated algorithm on {repr(data)}')
    time.sleep(3)
    print(highlight(f'YOU GOT {data or "nothing"}', GREEN))
    q.task_done()


if __name__ == '__main__':
  try:
    inport = serOpen()
    q = Queue()

    input_thread = StoppableThread(
      target=handle_input, args=(inport, q), daemon=True)
    output_thread = StoppableThread(
      target=handle_output, args=(q,), daemon=True)

    input_thread.start()
    output_thread.start()

    input_thread.join()
    logging.info(f'input_thread done')
    q.join()
    logging.info(f'queue joined')
    q.put(None)
    output_thread.join()
    logging.info(f'output_thread done')

  except (KeyboardInterrupt, SystemExit):
    logging.info('Keyboard intterruption detected.')
    logging.info('Waiting for threads to stop...')

    input_thread.stop()
    output_thread.stop()

    input_thread.join()
    logging.info(f'input_thread done')
    output_thread.join()
    logging.info(f'output_thread done')

  logging.info('bye bye')
