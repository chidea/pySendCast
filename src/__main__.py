def main(argv=None):
  if argv is None:
    from sys import argv
  def usage():
    print('usage : <send|s|recv|r> [arguments]')
    exit(1)
  if len(argv) == 1:
    usage()
  elif argv[1] in ('send', 's'):
    from .send import main as m
  elif argv[1] in ('recv', 'r'):
    from .recv import main as m
  else:
    usage()
  exit(m(argv[1:]))

if __name__ == '__main__':
  from sys import argv
  main(argv)
