import tarfile
from .bcast import BroadCastCliSocket, BroadCastServSocket, BCAST_MAGIC
import socket
from os.path import basename
import glob

def mkpin(length=4):
  from random import choices
  from string import digits
  return ''.join(choices(digits, k=length))

def isurl(s):
  return s.startswith(('http://','https://'))

def main(argv):
  srv_addr, pin = None, ''
  if len(argv) > 1:
    if argv[1] in ('-up', '--userpin') and len(argv)>4:
      pin=argv[2]
      print('user PIN :', pin)
      argv = [argv[0]] + argv[3:]
    elif argv[1] in ('-p', '--pin'):
      pin=mkpin()
      print('generated PIN :', pin)
      argv = [argv[0]] + argv[2:]
    elif argv[1] in ('-r', '--recv', '--receiver'):
      srv_addr = (argv[2],)

  with BroadCastCliSocket(magic='sendfile'+pin) as s:
    while srv_addr is None:
      try:
        srv_addr = s.discovery()
      except socket.timeout:
        pass
      except KeyboardInterrupt:
        s.close()
        print('user canceled sending')
        return 1
  print('sending to :', (srv_addr[0], 18902))
  with socket.create_connection((srv_addr[0], 18902)) as s:
    try:
      with tarfile.open(fileobj=s.makefile('wb', buffering=0), mode='w|gz') as t:
        for a in argv[1:]:
          isMessage = isurl(a)
          if not isMessage:
            files = list(glob.iglob(a))
            isMessage |= 0 == len(files)
          if isMessage:
            t.addfile(tarfile.TarInfo(a))
          else:
            for f in files:
              print('sending %s' %f)
              t.add(f, arcname=basename(f))
    except KeyboardInterrupt:
      print('user canceled sending')
      s.close()
      return 1
  
if __name__ == '__main__':
  from sys import argv
  main(argv)
