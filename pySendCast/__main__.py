def main(argv=None):
  def usage():
    print('usage : <send/recv> [arguments]')
    exit(1)
  if len(argv) == 1:
    usage()
  elif argv[1] == 'send':
    from .send import main as m
  elif argv[1] == 'recv':
    from .recv import main as m
  else:
    usage()
  exit(m(argv[1:]))

if __name__ == '__main__':
  from sys import argv
  main(argv)
