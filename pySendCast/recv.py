import tarfile
from .bcast import BroadCastServSocket,BroadCastCliSocket, BCAST_MAGIC
import socket
import timeit

def openurl(url):
  import webbrowser
  try:
    if webbrowser.get():
      webbrowser.open(url)
  except webbrowser.Error:
    from shutil import which
    if which('termux-open-url'):
      from os import system
      system('termux-open-url '+url)

def main(argv):
  if len(argv)>1 and argv[1]:
    if argv[1] in ('n', 'new', 'g', 'gen'):
      from .send import mkpin
      pin = mkpin()
      print('generated PIN :', pin)
    else: pin = argv[1]
  else: pin = ''
  with socket.socket() as s:
    s.bind(('', 18902))
    s.setblocking(True)
    s.settimeout(1)
    s.listen(1)
    try:
      while True:
        with BroadCastServSocket(magic='sendfile'+pin) as sa:
          sa.announce()
        try:
          c, a = s.accept()
          print(a[0]) # ip address
          from .send import isurl
          with tarfile.open(fileobj=c.makefile('rb', buffering=0), mode='r|gz') as t:
            timeit.gc.disable()
            for ti in t:
              if ti.size == 0:
                if isurl(ti.name):
                  openurl(ti.name)
                else: # plain message
                  print(ti.name)
                continue
              print('extracting %s (%d bytes)'%(ti.name,ti.size))
              t0=timeit.default_timer()
              t.extract(ti)
              t0=timeit.default_timer()-t0
              print('extracting %s done (%d bytes, %f seconds, %f MB/s)'%(ti.name,ti.size, t0, ti.size/t0/10**6))
            timeit.gc.enable()
            break
        except socket.timeout:
          continue
    except KeyboardInterrupt:
      s.close()

if __name__ == '__main__':
  from sys import argv
  main(argv)
