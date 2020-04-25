GREEN=32
YELLOW=33

def highlight(txt, color):
  return f'\033[{color}m{txt}\033[0m'
